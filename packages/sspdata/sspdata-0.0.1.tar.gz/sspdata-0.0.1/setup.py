# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sspdata', 'sspdata.base', 'sspdata.datasets']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'pandas>=1.2.3,<2.0.0',
 'requests>=2.25.1,<3.0.0',
 'setuptools>=57.0.0,<58.0.0']

entry_points = \
{'console_scripts': ['fmt = scripts.code_quality:do_code_formatting',
                     'fmt-check = scripts.code_quality:check_code_formatting',
                     'isort-check = scripts.code_quality:check_import_order',
                     'isort-fmt = scripts.code_quality:sort_import_order',
                     'linter = scripts.code_quality:linter',
                     'tests = scripts.code_quality:run_tests']}

setup_kwargs = {
    'name': 'sspdata',
    'version': '0.0.1',
    'description': 'Aquisição de dados abertos de segurança pública do estado de São Paulo.',
    'long_description': None,
    'author': 'Alexandre Farias',
    'author_email': '0800alefarias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
