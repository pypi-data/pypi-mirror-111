# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logging_actions']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logging-actions',
    'version': '0.1.2',
    'description': 'For easy configuration of `logging.Logger`s with `argparse.Action`s.',
    'long_description': '# `logging-actions`\nFor easy configuration of `logging.Logger`s with `argparse.Action`s.\n',
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
