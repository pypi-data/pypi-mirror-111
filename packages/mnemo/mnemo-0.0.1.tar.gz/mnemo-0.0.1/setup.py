# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mnemo', 'mnemo.bottled', 'mnemo.scripts']

package_data = \
{'': ['*'],
 'mnemo': ['autocomplete/*'],
 'mnemo.bottled': ['css/*',
                   'db/.gitignore',
                   'js/*',
                   'templates/*',
                   'templates/buttons/*',
                   'templates/forms/*',
                   'templates/includes/*',
                   'templates/pages/*',
                   'templates/responses/*']}

install_requires = \
['bottle>=0.12.19,<0.13.0',
 'click>=8.0.1,<9.0.0',
 'passlib>=1.7.4,<2.0.0',
 'paste>=3.5.0,<4.0.0',
 'rich>=10.4.0,<11.0.0',
 'tinydb>=4.5.0,<5.0.0']

entry_points = \
{'console_scripts': ['mnemo = mnemo.scripts.assistant:__main',
                     'mnemo-autocomplete = mnemo.scripts.autocomplete:__main']}

setup_kwargs = {
    'name': 'mnemo',
    'version': '0.0.1',
    'description': 'Notebook and assistant.',
    'long_description': '# mnemo-assistant',
    'author': 'Gabriele Girelli',
    'author_email': 'gigi.ga90@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ggirelli/mnemo-assistant',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
