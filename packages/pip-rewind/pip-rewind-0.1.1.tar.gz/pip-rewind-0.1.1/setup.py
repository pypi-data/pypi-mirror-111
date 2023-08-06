# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pip_rewind']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2021.1,<2022.0',
 'result>=0.6.0,<0.7.0',
 'rss-parser>=0.2.3,<0.3.0',
 'tzlocal>=2.1,<3.0']

entry_points = \
{'console_scripts': ['pip-rewind = pip_rewind.cli:main']}

setup_kwargs = {
    'name': 'pip-rewind',
    'version': '0.1.1',
    'description': 'Install python modules from pypi from a previous date in history',
    'long_description': '# pip-rewind\n\n`pip-rewind` is a command-line tool that can rewind pypi module versions (given as command-line arguments or read from a requirements.txt file) to a previous date in time.\n\nThis tool doesn\'t install any packages itself - rather, it generates output with modules constrained to specific versions, which can then be fed into `pip install`.\n\n## Usage\n\n```\n$ pip-rewind --date "09/01/2020" requests > new-requirements.txt\n$ pip install -r new-requirements.txt\n```\n\nOr give it a requirements file:\n\n```\n$ pip-rewind --date "07/01/2019" -r requirements.txt > new-requirements.txt\n$ pip install -r new-requirements.txt\n```\n\nYou can also pipe the output directly to pip if preferred:\n\n```\n$ pip-rewind --date "12/01/2020 -r requirements.txt | pip install -r /dev/stdin\n```\n\nCurrently, this package only parses a simple subset of valid requirements lines:\n\n```\nmodulename\nmodulename<=5.0.0\nmodulename==4.0.0\n```\n\nAny line that describes a pypi dependency named `modulename`, possibly with a version identifier after, is valid - this tool simply cares about `modulename` since the version will be rewound anyway. Other lines (such as git dependencies) are ignored.\n\n## Motivation\n\nStarting to work on old projects that don\'t have **all** their dependencies listed and version-constrained can be difficult (especially when some of those dependencies interact with specific versions of OS packages). The simple existence of a line specifying `redis` in a requirements.txt file without its version can lead to possible breakage when dealing with month- or year-old software.\n\n## LICENSE\n\nMIT\n',
    'author': 'Amar Paul',
    'author_email': 'amar.paul16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Amar1729/pip-rewind',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
