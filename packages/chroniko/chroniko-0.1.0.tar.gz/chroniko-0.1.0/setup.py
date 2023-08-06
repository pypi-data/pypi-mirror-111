# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chroniko']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chroniko',
    'version': '0.1.0',
    'description': '',
    'long_description': '# for the kaiba tools\n\n\n[https://github.com/kaiba-tech/kaiba](https://github.com/kaiba-tech/kaiba)\n',
    'author': 'Thomas Borgen',
    'author_email': 'thomasborgen91@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
