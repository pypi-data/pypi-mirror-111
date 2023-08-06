# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacy_detok']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0',
 'torch>=1.9.0,<2.0.0',
 'tqdm>=4.61.1,<5.0.0',
 'transformers>=4.8.2,<5.0.0']

setup_kwargs = {
    'name': 'spacy-detok',
    'version': '0.3.0',
    'description': 'Invert spaCy detokenization',
    'long_description': None,
    'author': 'melisa',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
