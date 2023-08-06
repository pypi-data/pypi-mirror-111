# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rtmilk']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1', 'requests>=2.23.0']

setup_kwargs = {
    'name': 'rtmilk',
    'version': '0.0.1',
    'description': 'RTM API wrapper',
    'long_description': None,
    'author': 'Rehan Khwaja',
    'author_email': 'rehan@khwaja.name',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
