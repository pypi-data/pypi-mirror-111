# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['admincharts', 'admincharts.migrations']

package_data = \
{'': ['*'],
 'admincharts': ['static/admincharts/*', 'templates/admin/admincharts/*']}

setup_kwargs = {
    'name': 'django-admincharts',
    'version': '0.1.0',
    'description': 'Chart.js integration for Django admin models',
    'long_description': None,
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
