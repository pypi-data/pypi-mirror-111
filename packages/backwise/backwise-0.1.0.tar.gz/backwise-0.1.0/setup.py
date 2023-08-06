# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backwise',
 'backwise.constants',
 'backwise.exceptions',
 'backwise.exchanges',
 'backwise.indicators',
 'backwise.mixins',
 'backwise.tools']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.2.0,<2.0.0',
 'arctic>=1.79.4,<2.0.0',
 'ccxt>=1.51.98,<2.0.0',
 'pandas==1.0.3',
 'pytz>=2021.1,<2022.0']

setup_kwargs = {
    'name': 'backwise',
    'version': '0.1.0',
    'description': 'A Python 3 interface for the Backwise algo-trading software',
    'long_description': None,
    'author': 'khunspoonzi',
    'author_email': 'khunspoonzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
