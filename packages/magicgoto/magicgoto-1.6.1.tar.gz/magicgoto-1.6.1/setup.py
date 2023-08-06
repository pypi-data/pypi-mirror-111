# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['goto',
 'goto.commands',
 'goto.gotomagic',
 'goto.gotomagic.text',
 'goto.plugins',
 'goto.tests']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0',
 'future>=0.18.2,<0.19.0',
 'pyperclip>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'magicgoto',
    'version': '1.6.1',
    'description': 'Goto - Goto is a magic tool that takes you were you want to be, now.',
    'long_description': None,
    'author': 'technocake',
    'author_email': 'robin.garen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
