#! /usr/bin/env python
from setuptools import setup

CLASSIFIERS = [
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Topic :: Software Development :: Libraries :: Python Modules']

setup(
    name='prices',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Python price handling for humans',
    license='BSD',
    version='1.1.0',
    url='https://github.com/mirumee/prices',
    packages=['prices'],
    install_requires=['babel>=2.5.0', 'typing>=3.6.0;python_version<"3.5"'],
    classifiers=CLASSIFIERS,
    platforms=['any'])
