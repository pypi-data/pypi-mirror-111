# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_pycharm', 'django_pycharm.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.4,<4.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'django-pycharm',
    'version': '0.1.2',
    'description': 'App for Django to run any Python script within Django context',
    'long_description': "# django-pycharm\n\nApp for Django to run any Python script within Django context\n\n\n## Installation\n\nYou can install the plugin by running\n\n```shell\npip install django-pycharm\n```\n\nIn ``settings.py`` add  ``django-pycharm`` to your ``INSTALLED_APPS``\n```python\nINSTALLED_APPS += ['django_pycharm']\n```\n\n## Usage\n\n```shell\npython manage.py runscript <your_script.py>\n```\n\n```shell\npython manage.py install_pycharm_commands\n```\n",
    'author': 'nouseforacode',
    'author_email': '10090277+nouseforacode@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nouseforacode/django-pycharm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
