# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embutils',
 'embutils.serial',
 'embutils.serial.core',
 'embutils.serial.data',
 'embutils.utils']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['docs = scripts.poetry:run_docs',
                     'html = scripts.poetry:run_html',
                     'test = scripts.poetry:run_test',
                     'version = scripts.poetry:run_version']}

setup_kwargs = {
    'name': 'embutils',
    'version': '0.2.1',
    'description': 'Python utilities for embedded projects',
    'long_description': '# Embutils [![PyPI version](https://badge.fury.io/py/embutils.svg)](https://badge.fury.io/py/embutils) [![License](https://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://badges.mit-license.org)\n\nPython utilities for embedded projects. \n\n## Installation \nYou can get the packaged version from [PyPI](https://pypi.org/project/embutils/):\n```\npip install embutils\n```',
    'author': 'Christian Wiche',
    'author_email': 'cwichel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cwichel/embutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
