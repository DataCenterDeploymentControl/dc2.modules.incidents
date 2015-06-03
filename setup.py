#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='dc2.modules.statusmgmt',
    version='0.0.1',
    author="Stephan Adig",
    author_email="sh@sourcecode.de",
    namespace_packages=['dc2', 'dc2.modules'],
    url='http://gitlab.sourcecode.de/sadig/dc2.modules',
    package_dir={'': 'src'},
    packages=find_packages('src'),
)
