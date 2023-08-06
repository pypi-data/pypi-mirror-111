# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dashed']

package_data = \
{'': ['*']}

install_requires = \
['PyNaCl>=1.4.0,<2.0.0', 'aiohttp>=3.7.4,<4.0.0', 'httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'dashed',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'andrei',
    'author_email': 'b1naryth1ef@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
