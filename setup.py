#!/usr/bin/python -u
# coding=utf-8
import sys
from setuptools import setup
reload(sys)
sys.setdefaultencoding("utf8")

# TODO see if this actually works
setup(name='companiadelagalleta',
      version='0.7.0',
      description='Tracking for cookie sales',
      url='http://github.com/JohnAZoidberg/companiadelagalleta',
      author='Daniel Schäfer',
      author_email='galletas@danielschaefer.me',
      packages=['companiadelagalleta', 'testing'],
      install_requires=[
          'flask',
      ],
)