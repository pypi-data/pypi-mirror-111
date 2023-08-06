# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maxcutpy', 'maxcutpy.rtr', 'maxcutpy.rtr.stiefel', 'maxcutpy.solvers']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.5.1,<3.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'tqdm>=4.61.1,<5.0.0']

setup_kwargs = {
    'name': 'maxcutpy',
    'version': '0.1.2',
    'description': 'A python Implementation of Graph Max Cut Solutions',
    'long_description': None,
    'author': 'trevorWieland',
    'author_email': 'trevor_wieland@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
