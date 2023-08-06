# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gazoo']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['gazoo = gazoo:main']}

setup_kwargs = {
    'name': 'gazoo',
    'version': '0.0.0b0',
    'description': 'Wrap Minecraft bedrock server to make proper backups.',
    'long_description': None,
    'author': 'John Schroeder',
    'author_email': 'john@schroedernet.software',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
