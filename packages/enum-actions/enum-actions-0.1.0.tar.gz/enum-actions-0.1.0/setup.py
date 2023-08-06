# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['enum_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'enum-actions',
    'version': '0.1.0',
    'description': 'For easy selection command-line selection of an `enum.Enum` variant with `argparse.Action`s.',
    'long_description': '# `enum-actions`\nFor easy selection command-line selection of an `enum.Enum` variant with `argparse.Action`s.\n',
    'author': 'Aatif Syed',
    'author_email': 'aatifsyedyp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
