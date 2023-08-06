# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whale_revenue_projection']

package_data = \
{'': ['*']}

install_requires = \
['dbapi>=0.0.14,<0.0.15',
 'pandas==0.25.3',
 'plotly>=4.14.2,<5.0.0',
 'pymysql>=0.9.3,<0.10.0',
 'whale_back_bone>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'whale-revenue-projection',
    'version': '0.0.1',
    'description': 'Package using the in-house LTV and Churn data to project revenue depending on the source type (Campaign, Product, Sponsor)',
    'long_description': None,
    'author': 'Arnaud Pourchez',
    'author_email': 'arnaud.pourchez@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://test.pypi.org/simple/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
