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
    'version': '0.1.2',
    'description': 'Python library for easy message broker handling using Pydantic',
    'long_description': "# pikantic\n\n[![PyPI](https://img.shields.io/pypi/v/pikantic)](https://pypi.org/project/pikantic/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pikantic)](https://pypi.org/project/pikantic/)\n[![PyPI License](https://img.shields.io/pypi/l/pikantic)](https://pypi.org/project/pikantic/)\n[![Code Style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black/)\n\nPython library for easy message broker handling using Pydantic\n\n### Basic Usage\n\n```python\nimport pikantic\nfrom pydantic import BaseModel\n\napp = pikantic.Pikantic(AMQP_URI)\n\n\nclass PersonModel(BaseModel):\n    name: str\n    age: int\n\n\n@app.on_rabbit('test_queue')\nasync def handle_message(msg: aio_pika.Message, person: PersonModel):\n    print(msg.body)\n    print(person.age)\n\n\nif __name__ == '__main__':\n    app.run()\n```\n",
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
