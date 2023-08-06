# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioarango']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.1.0,<3.0.0',
 'httpx>=0.18.2,<0.19.0',
 'requests-toolbelt>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'aioarango',
    'version': '1.0.0',
    'description': 'Asynchronous driver for ArangoDB',
    'long_description': None,
    'author': 'Alexey Tylindus',
    'author_email': 'a.tylindus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mirrorrim/aioarango',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
