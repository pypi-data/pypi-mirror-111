# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_views']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0', 'pandas>=1.2.5,<2.0.0']

setup_kwargs = {
    'name': 'fast-views',
    'version': '0.1.0',
    'description': 'Fast operations on time-unit indexed dataframes',
    'long_description': None,
    'author': 'peder2911',
    'author_email': 'pglandsverk@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
