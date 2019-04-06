#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PysparkExample',
      version='1.0',
      description='Python Distribution Utilities',
      author='Stijn De Haes',
      author_email='stijndehaes@gmail.co,',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      scripts=['bin/run.py']
      )
