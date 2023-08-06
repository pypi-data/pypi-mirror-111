# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['acdc']
install_requires = \
['memory-profiler>=0.58.0,<0.59.0']

setup_kwargs = {
    'name': 'acdc',
    'version': '0.1.0',
    'description': 'Wanna-be fast string search',
    'long_description': None,
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
