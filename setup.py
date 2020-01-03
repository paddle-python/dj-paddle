#!/usr/bin/env python
import os
import sys

from setuptools import setup

if sys.argv[-1] == "publish":
    os.system("python setup.py bdist_wheel upload --sign")
    sys.exit()

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(long_description=README)
