#! /usr/bin/env python
import prices

from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.5',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name='prices',
      author='Mirumee Software',
      author_email='hello@mirumee.com',
      description='Python price handling for humans',
      license='BSD',
      version='0.5.3',
      url='https://github.com/mirumee/prices',
      packages=['prices'],
      test_suite='prices.tests',
      include_package_data=True,
      classifiers=CLASSIFIERS,
      platforms=['any'])
