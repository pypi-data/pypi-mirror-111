# Copyright (c) 2021 Avery
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from os import path
from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='tribi',
      version='1.0.3',
      description='Prettier error handling for Python',
      author='starsflower',
      url='https://github.com/starsflower/python-tri',
      license="MIT",
      classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
      ],
      packages=['tri'],
      package_dir={'tri': './tri'},

      # Description
      long_description=long_description,
      long_description_content_type='text/markdown')
