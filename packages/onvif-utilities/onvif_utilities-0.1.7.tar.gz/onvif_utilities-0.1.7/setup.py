# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onvif_utilities']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'onvif-utilities',
    'version': '0.1.7',
    'description': '',
    'long_description': None,
    'author': 'MohammadHossein',
    'author_email': 'hos1377@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
