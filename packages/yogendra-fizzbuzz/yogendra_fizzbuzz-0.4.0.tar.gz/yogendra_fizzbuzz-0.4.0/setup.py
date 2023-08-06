# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yogendra_fizzbuzz']

package_data = \
{'': ['*']}

install_requires = \
['homepage', 'keywords', 'keywords', 'license', 'repository']

entry_points = \
{'console_scripts': ['test = scripts:test']}

setup_kwargs = {
    'name': 'yogendra-fizzbuzz',
    'version': '0.4.0',
    'description': 'Simple Fizz Buzz Game',
    'long_description': "\n# Yogendra/FizzBuzz Module\n\nThis is a simple demo module to understand python module publishing system.\n\nThis module uses\n\n- Python 3.x\n- Poetry\n- Pytest\n\n## Getting Started\n\n1. Add library to your project\n\n    ```bash\n    pip install yogendra_fizzbuzz\n    ```\n\n1. Use in your program. Following is an example in repl:\n\n    ```bash\n    >>> from yogendra_fizzbuzz import fizzbuzz_to\n    >>> print(fizzbuzz_to(16))\n    [ '1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz', '16']\n    ```\n\n## How to build\n\n1. Clone the project\n\n    ```bash\n    git clone https://github.com/yogendra/pypi-yogendra_fizzbuzz.git yogendra_fizzbuzz\n    cd yogendra_fizzbuzz\n    ```\n\n1. Install dependencies\n\n    ```bash\n    poetry install \n    ```\n\n1. Build project\n\n    ```bash\n    poetry build\n    ```\n\n1. (Optional) Publish to Test PyPI\n\n    ```bash\n    poetry publish -r testpypi\n    ```\n\n1. Publish to PyPI\n\n    ```bash\n    poetry publish\n    ```\n",
    'author': 'Yogendra Rampuria (Yogi)',
    'author_email': 'yogendrarampuria@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
