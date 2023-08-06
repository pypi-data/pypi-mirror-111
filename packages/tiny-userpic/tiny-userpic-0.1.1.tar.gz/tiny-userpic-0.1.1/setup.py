# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['userpic']

package_data = \
{'': ['*']}

install_requires = \
['CairoSVG>=2.5.2,<3.0.0', 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'tiny-userpic',
    'version': '0.1.1',
    'description': 'A small Python module for userpics creation',
    'long_description': None,
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
