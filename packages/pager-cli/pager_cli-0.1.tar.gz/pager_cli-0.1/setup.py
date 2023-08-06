# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pager_cli', 'pager_cli.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'minilog>=2.0,<3.0',
 'requests-mock>=1.9.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'strictyaml>=1.4.4,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'types-requests>=2.25.0,<3.0.0',
 'types-setuptools>=57.0.0,<58.0.0',
 'types-tabulate>=0.1.1,<0.2.0',
 'yaspin>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['pager_cli = pager_cli.cli:main']}

setup_kwargs = {
    'name': 'pager-cli',
    'version': '0.1',
    'description': 'pagerduty cli to list/ack/resolve incidents',
    'long_description': '# Overview\n\npagerduty cli to list/ack/resolve incidents\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/com/frankiexyz/pager_cli.svg?label=unix)](https://travis-ci.com/frankiexyz/pager_cli)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/frankiexyz/pager_cli.svg?label=windows)](https://ci.appveyor.com/project/frankiexyz/pager_cli)\n[![Coverage Status](https://img.shields.io/codecov/c/gh/frankiexyz/pager_cli)](https://codecov.io/gh/frankiexyz/pager_cli)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/frankiexyz/pager_cli.svg)](https://scrutinizer-ci.com/g/frankiexyz/pager_cli)\n[![PyPI Version](https://img.shields.io/pypi/v/pager_cli.svg)](https://pypi.org/project/pager_cli)\n[![PyPI License](https://img.shields.io/pypi/l/pager_cli.svg)](https://pypi.org/project/pager_cli)\n\n# Setup\n\n## Requirements\n\n* Python 3.9+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install pager_cli\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add pager_cli\n```\n\n# Usage\n\ncreate a file to store your API key\n```text\ncat ~/.pager_cli -p\nuserid: YOUR_USER_ID(eg:PBZDORP)\napikey: YOUR_API_KEY\n```\n\nList and ACK the incident\n```bash\n # pager_cli --help\n Usage: pager_cli [OPTIONS]\n\n   Console script for pager_cli.\n\n   Options:\n   --action TEXT  Action list/ack/resolve\n   --config TEXT  config file default:~/.pager_cli\n   --help         Show this message and exit.\n # pager_cli\n ⠸ Loading...\n 🦾 No active incident\n```\n',
    'author': 'Frankie',
    'author_email': 'f@peering.sh',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pager_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
