#! /usr/bin/env python
import os
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

README_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
with open(README_PATH, "r", encoding="utf8") as f:
    README = f.read()

setup(
    name='prices',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Python price handling for humans',
    long_description=README,
    long_description_content_type="text/markdown",
    license='BSD',
    version='1.1.1',
    url='https://github.com/mirumee/prices',
    packages=['prices'],
    install_requires=['babel>=2.5.0', 'typing>=3.6.0;python_version<"3.5"'],
    classifiers=CLASSIFIERS,
    platforms=['any'])
