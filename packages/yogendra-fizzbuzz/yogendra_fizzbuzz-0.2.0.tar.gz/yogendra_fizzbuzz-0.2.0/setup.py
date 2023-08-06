# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yogendra_fizzbuzz']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'yogendra-fizzbuzz',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Yogendra Rampuria (Yogi)',
    'author_email': 'yogendrarampuria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
