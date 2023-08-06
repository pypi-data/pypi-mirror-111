# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['acdc']
setup_kwargs = {
    'name': 'acdc',
    'version': '0.1.1',
    'description': 'Wanna-be fast string search',
    'long_description': '# acdc\n\n## Wanna-be fast string searcher\n\n**beta**\n\n[![Two planes joined with electric arcs](https://images.unsplash.com/photo-1534224039826-c7a0eda0e6b3?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80)](https://unsplash.com/photos/ImcUkZ72oUs)',
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~amirouche/python-acdc',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
