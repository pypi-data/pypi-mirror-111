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
    'version': '0.9.3',
    'description': 'asyncio drivers for FoundationDB',
    'long_description': "# [asyncio-foundationdb](https://github.com/amirouche/asyncio-foundationdb/)\n\n*early draft*\n\nasyncio drivers for foundationdb tested with CPython 3.9\n\n```\npip install asyncio-foundationdb\n```\n\n```python\n> import found\n> found.api_version(630)\n> db = await found.open()\n> await db.get(b'hello')\n> await db.set(b'hello', b'world')\n> await tr.get(b'hello')\nb'world'\n```\n\n## ChangeLog\n\n### v0.9.x\n\n- feature: bump to foundationdb 6.3.15 client API\n- feature: add hooks and states\n\n### v0.8.0\n\n- breaking change: replace ``get_rangefoo`` with ``rangefoo`` as async generator\n- new: add short syntax for querying `Nstore.query(tr, patterns)`\n- chore: remove pipenv, and pre-commit\n",
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
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
