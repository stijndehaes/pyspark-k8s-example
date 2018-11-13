#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='PysparkExample',
      version='1.0',
      description='Python Distribution Utilities',
      author='Stijn De Haes',
      author_email='stijndehaes@gmail.co,',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=['pyspark==2.4.0'],
      scripts=['bin/run.py']
      )
