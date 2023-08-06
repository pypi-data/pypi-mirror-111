from setuptools import setup, find_packages

import os

VERSION = '0.0.10'
DESCRIPTION = "LinkedList Package"

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


#Setting up
setup(
    name="py_linkedlist",
    version=VERSION,
    author="Rajesh Kumar Patnala",
    author_email="patnala04@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'dsa', 'data structures', 'linkedlist', 'linked list', 'algorithms'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
),

