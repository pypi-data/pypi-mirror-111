#!/usr/bin/env python
# -*- coding: utf-8 -*

from __future__ import absolute_import

import os
from codecs import open

from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

readme = "Just Use yem"
history = "Nothing"

setup(name='abcdijklm.py',
      version='1.0.2',
      packages=find_packages('src', exclude=('tests', )),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      description='test',
      long_description=readme + '\n\n' + history,
      long_description_content_type='text/markdown',
      author='Me',
      author_email='albert@trashemail.in',
      license='Creative Commons Attribution-Noncommercial-Share Alike license',
      install_requires=install_requires,
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP',
      ])
