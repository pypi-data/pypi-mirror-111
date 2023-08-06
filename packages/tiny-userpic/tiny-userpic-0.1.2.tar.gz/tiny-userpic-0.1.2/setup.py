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
    'version': '0.1.2',
    'description': 'A small Python module for userpics creation',
    'long_description': '# Userpic Generator\n\n## Installation\n\n```bash\npip install tiny-userpic\n```\n\n## Usage\n\n```bash\npython -m userpic --output img.png\n```\n\nor\n\n```python\nfrom userpic import make_userpic\ndata = make_userpic(\n    cells_count=7,\n    cell_size=32,\n    offset=16,\n    data_format="svg",\n)\nwith open("output.svg", "wb") as file:\n    file.write(data)\n```\n',
    'author': 'Aleksandr Shpak',
    'author_email': 'shpaker@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shpaker/tiny-userpic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
