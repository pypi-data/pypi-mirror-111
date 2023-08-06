# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neon_schemas']

package_data = \
{'': ['*']}

install_requires = \
['avro>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'neon-schemas',
    'version': '0.1.12',
    'description': 'Schemas for Neon Law',
    'long_description': None,
    'author': 'neon law',
    'author_email': 'support@neonlaw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
