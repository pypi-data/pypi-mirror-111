# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['clustercheck']
install_requires = \
['pyyaml>=5.4.1,<6.0.0',
 'requests>=2.25.1,<3.0.0',
 'websocket-client>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['clustercheck = clustercheck:main']}

setup_kwargs = {
    'name': 'clustercheck',
    'version': '0.1.0',
    'description': 'check a cluster of services',
    'long_description': None,
    'author': 'erik aronesty',
    'author_email': 'erik@q32.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
