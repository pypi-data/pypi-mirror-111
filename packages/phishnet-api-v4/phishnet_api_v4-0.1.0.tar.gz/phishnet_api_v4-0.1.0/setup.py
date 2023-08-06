# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phishnet_api_v4']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.18.0,<0.19.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'phishnet-api-v4',
    'version': '0.1.0',
    'description': 'Python3 client to interface with v4 of the api.phish.net REST endpoints.',
    'long_description': None,
    'author': 'Jay Flaherty',
    'author_email': 'jayflaherty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
