# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pikantic']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.8.0,<7.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pikantic',
    'version': '0.1.1',
    'description': 'Python library for easy message broker handling using Pydantic',
    'long_description': '# pikantic\n\n[![PyPI](https://img.shields.io/pypi/v/pikantic)](https://pypi.org/project/pikantic/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pikantic)](https://pypi.org/project/pikantic/)\n[![PyPI License](https://img.shields.io/pypi/l/pikantic)](https://pypi.org/project/pikantic/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nPython utility decorator and context manager for swapping exceptions.\n\n### Basic Usage\n\nAs a decorator:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({KeyError: ValueError("Incorrect value")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\nOr as a context manager:\n```python\nfrom swap_exceptions import swap_exceptions\n\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    with swap_exceptions({KeyError: ValueError("Incorrect value")}):\n        return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\n### Advanced Usage\n\nMapping key can also be a tuple:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({(KeyError, TypeError): ValueError("Incorrect value")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2, \'c\': \'not a number\'}\n    return d[key] + 10\n\nget_value(\'c\')  # ValueError: Incorrect value\n```\n\nMapping value can also be a factory that generates the exception:\n```python\nfrom swap_exceptions import swap_exceptions\n\n@swap_exceptions({KeyError: lambda e: ValueError(f"Incorrect value {e.args[0]}")})\ndef get_value(key: str):\n    d = {\'a\': 1, \'b\': 2}\n    return d[key]\n\nget_value(\'c\')  # ValueError: Incorrect value c\n```\n',
    'author': 'Tom Gringauz',
    'author_email': 'tomgrin10@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tomgrin10/pikantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
