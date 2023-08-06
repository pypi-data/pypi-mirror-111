# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['found']

package_data = \
{'': ['*']}

install_requires = \
['cffi>=1.14.5,<2.0.0',
 'foundationdb>=6.3.16,<7.0.0',
 'immutables>=0.15,<0.16',
 'six>=1.16.0,<2.0.0']

setup_kwargs = {
    'name': 'asyncio-foundationdb',
    'version': '0.9.0',
    'description': 'asyncio drivers for FoundationDB',
    'long_description': None,
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
