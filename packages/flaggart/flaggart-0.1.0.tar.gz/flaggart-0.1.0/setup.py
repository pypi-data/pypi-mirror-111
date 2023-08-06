# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flaggart']

package_data = \
{'': ['*']}

install_requires = \
['wikipedia>=1.4.0,<2.0.0', 'wptools>=0.4.17,<0.5.0']

setup_kwargs = {
    'name': 'flaggart',
    'version': '0.1.0',
    'description': 'Retrieves place flags and performs useful operations on them',
    'long_description': None,
    'author': 'AlDacMac',
    'author_email': 'alasdairmacgdev@gmail.com',
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
