# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucktrix']

package_data = \
{'': ['*']}

install_requires = \
['matrix-nio[e2e]>=0.16.0,<0.17.0']

setup_kwargs = {
    'name': 'bucktrix',
    'version': '0.1.5',
    'description': 'Matrix bot',
    'long_description': None,
    'author': 'Vincent Carlos',
    'author_email': 'git@finzzz.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/finzzz/bucktrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
