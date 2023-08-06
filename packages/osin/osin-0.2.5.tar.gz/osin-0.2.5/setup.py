# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['osin', 'osin.ui', 'osin.ui.toggle_list']

package_data = \
{'': ['*'],
 'osin.ui': ['www/*',
             'www/build/*',
             'www/build/static/css/*',
             'www/build/static/js/*',
             'www/public/*',
             'www/src/*'],
 'osin.ui.toggle_list': ['frontend/*',
                         'frontend/build/*',
                         'frontend/build/static/js/*',
                         'frontend/public/*',
                         'frontend/src/*']}

install_requires = \
['Flask>=2.0.1,<3.0.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.2,<4.0.0',
 'orjson>=3.5.4,<4.0.0',
 'pandas>=1.2.4,<2.0.0',
 'peewee>=3.14.4,<4.0.0',
 'plotly>=5.0.0,<6.0.0',
 'python-dotenv>=0.17.1,<0.18.0',
 'ruamel.yaml>=0.17.9,<0.18.0',
 'seaborn>=0.11.1,<0.12.0',
 'streamlit-callbacks>=0.0.5,<0.0.6',
 'streamlit>=0.82.0,<0.83.0',
 'tornado>=6.1,<7.0']

setup_kwargs = {
    'name': 'osin',
    'version': '0.2.5',
    'description': 'Rethink Experimenting',
    'long_description': None,
    'author': 'Binh Vu',
    'author_email': 'binh@toan2.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/binh-vu/osin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
