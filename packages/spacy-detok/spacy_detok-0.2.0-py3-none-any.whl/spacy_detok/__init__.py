import argparse
import os
import sys
import time

import numpy as np
import torch
from tqdm import tqdm
from transformers import BertForTokenClassification, BertTokenizerFast


def parse_args():
    parser = argparse.ArgumentParser(description="Detokenize spaCy.")
    parser.add_argument("--model_dir", type=str, required=True, help="model dir path")
    parser.add_argument(
        "--model_type", type=str, default="bert-base-cased", help="model dir path"
    )
    parser.add_argument("--lowercase", type=bool, default=False, help="if do lowercase")
    parser.add_argument("--max_length", type=int, default=80, help="max length")
    parser.add_argument("--device", type=str, default="cpu", help="device: cpu or gpu")
    parser.add_argument("--batch_size", "-b", type=int, default=320)
    return parser.parse_args()


class BertTokenTaggerDetokenizer:
    def __init__(
        self,
        model_type,
        lowercase,
        model_dir,
        debug=False,
        max_length=80,
        device="cpu",
        batch_size=320,
    ):
        self.debug = debug
        self.message = "Insert a sentence or press Ctrl+C\n"

        if self.debug:
            print("Loading tokenizers and models...")

        self.tokenizer = BertTokenizerFast.from_pretrained(
            model_type, do_lower_case=lowercase
        )
        self.max_length = max_length
        self.model = BertForTokenClassification.from_pretrained(model_dir)

        self.tag_values = {0: "NONE", 1: "SPACE"}

        # disable gpu
        # for cpu batching only for sents > max_length
        if device == "cpu":
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            self.batch_size = 1
        else:
            self.batch_size = batch_size

    @staticmethod
    def detokenize_line(spacy_detok, bert_detok, labels):
        # bert tokenization output
        # bert_detok = _tokenize(spacy_detok)
        # bert offsets
        offsets = bert_detok.offset_mapping

        # iterate over bert tokens
        # add them to a sentence with spaces or not - labels

        output = ""
        for (start, end), label in zip(offsets, labels):
            if label == "NONE":
                output += spacy_detok[start:end]
            else:
                output += spacy_detok[start:end] + " "

        return output

    def zero_pad_to_max_length(self, l):
        diff = self.max_length - len(l)
        return l + [0] * diff

    def if_clip(self, input_ids):
        # check if the sentence is > tha max length
        # ie requires chunking with multiple preds
        return sum(list(filter(lambda x: x, input_ids))) > self.max_length

    def gen_split_overlap(self, input_ids, overlap=4):
        """
        why default overlap is 4:
        [[1, 2, 3, 4, 5, 6], [3, 4, 5, 6, 7, 8], [5, 6, 7, 8, 9, 10], [7, 8, 9, 10, 11, 12]]
        jump from 4 in list 1 to 5 in list 2
        ie. never consider fisrt and last 2 elements
        """
        assert overlap % 2 == 0, "use even overlap!"

        for i in range(0, len(input_ids) - overlap, self.max_length - overlap):
            yield input_ids[i : i + self.max_length]

    @staticmethod
    def merge_labels(label_indices, overlap=4):

        assert overlap % 2 == 0, "use even overlap!"
        margin = overlap // 2

        # drop last overlap/2 and first overlap/2
        merged_label_indices = list(label_indices[0][: -1 * margin])
        for li in label_indices[1:-1]:
            merged_label_indices.extend(list(li[margin : -1 * margin]))
        merged_label_indices.extend(list(label_indices[-1][margin:]))
        return merged_label_indices

    def _bert_tokenize_line(self, line):
        return self.tokenizer.encode_plus(
            line,
            add_special_tokens=True,
            truncation=False,
            padding="max_length",
            max_length=self.max_length,
            return_offsets_mapping=True,
        )

    def _get_sentence_input(self, tokenized_sentence):

        tokenized_sent_ids = tokenized_sentence.input_ids
        tokenized_sent_attention_mask = tokenized_sentence.attention_mask
        offsets = tokenized_sentence.offset_mapping

        chunked_ids = []
        chunked_attention = []

        if self.if_clip(tokenized_sent_ids):
            chunks_with_overlap = list(self.gen_split_overlap(tokenized_sent_ids))
            for chunk_with_overlap in chunks_with_overlap:
                chunk_ids = self.zero_pad_to_max_length(chunk_with_overlap)
                chunk_attention = self.zero_pad_to_max_length(
                    [1] * len(chunk_with_overlap)
                )
                chunked_ids.append(chunk_ids)
                chunked_attention.append(chunk_attention)
        else:
            chunked_ids = [tokenized_sent_ids]
            chunked_attention = [tokenized_sent_attention_mask]

        return chunked_ids, chunked_attention

    def _resolve_sentence_pred(self, sent, tokenized_sentence, label_indices):

        # join potentially split predictions
        if len(label_indices) > 1:
            label_indices = self.merge_labels(label_indices)[: len(tokenized_sent_ids)]
        else:
            label_indices = label_indices[0]

        # if nothing has changed
        if max(label_indices) == 0:
            return sent

        labels = [self.tag_values[label_idx] for label_idx in label_indices]

        result = self.detokenize_line(sent, tokenized_sentence, labels)

        return result

    def predict(self, sent):

        tokenized_sentence = self._bert_tokenize_line(sent)
        chunked_ids, chunked_attention = self._get_sentence_input(tokenized_sentence)

        # get labels
        input_ids = torch.tensor(chunked_ids)
        attention_mask = torch.tensor(chunked_attention)

        with torch.no_grad():
            output = self.model(input_ids=input_ids, attention_mask=attention_mask)
        label_indices = np.argmax(output[0].to("cpu").numpy(), axis=2)

        result = self._resolve_sentence_pred(sent, tokenized_sentence, label_indices)

        return result

    def __call__(self, line, if_strip=False):

        time_start = time.time()

        if if_strip:
            line = line.strip()

        result = self.predict(line)

        time_end = time.time()

        if self.debug:
            print(f"Result: {result}")
            print(f"Predicition took: {time_end - time_start} s.")
            print(f"\n{self.message}")
        return result

    @staticmethod
    def get_file_len(file_path):
        with open(file_path) as f:
            i = -1
            for i, l in enumerate(f):
                pass
        return i + 1

    def _get_batch(self, input_f, if_strip=False):
        count = 0

        batch_split = []
        sentences_batch = []
        tokenized_sentences_batch = []
        chunked_ids_batch = []
        chunked_attention_batch = []

        while count < self.max_length:
            try:
                sentence = next(input_f)

                if if_strip:
                    sentence = sentence.strip()

                tokenized_sentence = self._bert_tokenize_line(sentence)
                chunked_ids, chunked_attention = self._get_sentence_input(
                    tokenized_sentence
                )

                sentence_count = len(chunked_ids)

                # remember how to cut batch into sentences
                sentences_batch.append(sentence)
                batch_split.append([count, count + sentence_count])

                count += sentence_count

                tokenized_sentences_batch.append(tokenized_sentence)
                chunked_ids_batch.extend(chunked_ids)
                chunked_attention_batch.extend(chunked_attention)

            except StopIteration:
                return (
                    False,
                    batch_split,
                    sentences_batch,
                    tokenized_sentences_batch,
                    chunked_ids_batch,
                    chunked_attention_batch,
                )
        return (
            True,
            batch_split,
            sentences_batch,
            tokenized_sentences_batch,
            chunked_ids_batch,
            chunked_attention_batch,
        )

    def detokenize_file(self, input_path, output_path):
        total = self.get_file_len(input_path)

        with open(input_path, "r", encoding="utf8") as f_in, open(
            output_path, "w", encoding="utf8"
        ) as f_out:

            if_next = True

            with tqdm(total=total) as pbar:
                while if_next:

                    results = []

                    # fetch a batch from file
                    (
                        if_next,
                        batch_split,
                        sentences_batch,
                        tokenized_sentences_batch,
                        chunked_ids_batch,
                        chunked_attention_batch,
                    ) = self._get_batch(f_in, if_strip=True)

                    # get labels
                    input_ids = torch.tensor(chunked_ids_batch)
                    attention_mask = torch.tensor(chunked_attention_batch)

                    with torch.no_grad():
                        output = self.model(
                            input_ids=input_ids, attention_mask=attention_mask
                        )
                    label_indices_batch = np.argmax(output[0].to("cpu").numpy(), axis=2)

                    # resolve predictions for splits
                    for i, (start, end) in enumerate(batch_split):
                        tokenized_sentence = tokenized_sentences_batch[i]
                        sentence = sentences_batch[i]
                        label_indices = label_indices_batch[start:end]
                        chunked_ids = chunked_ids_batch[start:end]
                        result = self._resolve_sentence_pred(
                            sentence, tokenized_sentence, label_indices
                        )
                        results.append(result)

                    f_out.writelines([f"{r}\n" for r in results])

                    # update the progress bar
                    pbar.update(len(sentences_batch))


def main(args):

    btt_detok = BertTokenTaggerDetokenizer(
        model_type=args.model_type,
        lowercase=args.lowercase,
        model_dir=args.model_dir,
        max_length=args.max_length,
        debug=True,
        batch_size=1,
    )
    print(btt_detok.message)
    for line in sys.stdin:
        btt_detok(line)


if __name__ == "__main__":
    args = parse_args()
    main(args)
