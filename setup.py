#!/usr/bin/env python
import codecs
import os.path
import re
import sys
from setuptools import find_packages, setup
from spotr import version

setup(
    name = 'spotr',
    version = version.VERSION,
    description = 'AWS spot instance management for development workflows',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url = 'https://github.com/samuelreh/spotr',
    author = 'Samuel Reh',
    author_email = 'samuelreh@gmail.com',
    license = 'UNLICENSE',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Environment :: Console',
    ],
    keywords = 'aws ec2 spot instances development devops cloud cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['docopt', 'boto3'],
    test_require=['coverage', 'pytest', 'pytest-cov', 'mock'],
    entry_points = {
        'console_scripts': [
            'spotr=spotr.spotr:main',
        ],
    },
)
