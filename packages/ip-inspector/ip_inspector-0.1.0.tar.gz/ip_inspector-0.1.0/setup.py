# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ip_inspector']

package_data = \
{'': ['*'], 'ip_inspector': ['etc/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'SQLAlchemy>=1.4.19,<2.0.0',
 'argcomplete>=1.12.3,<2.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'geoip2>=4.2.0,<5.0.0',
 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ip-inspector = ip_inspector.cli:main']}

setup_kwargs = {
    'name': 'ip-inspector',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Sean McFeely',
    'author_email': 'mcfeelynaes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
