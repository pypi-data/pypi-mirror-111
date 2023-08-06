# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakewsserver']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'fakewsserver',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'uigctaw',
    'author_email': 'uigctaw@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
