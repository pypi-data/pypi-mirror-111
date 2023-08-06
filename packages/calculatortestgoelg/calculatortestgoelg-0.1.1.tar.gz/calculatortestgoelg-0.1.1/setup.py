# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calculatortestgoelg']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'calculatortestgoelg',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'goelg',
    'author_email': 'goelg.goel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
