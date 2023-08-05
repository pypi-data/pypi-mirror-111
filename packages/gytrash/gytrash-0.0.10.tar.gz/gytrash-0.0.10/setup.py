#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

repo_path = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(exclude=("examples",))

with open("requirements.txt") as f:
    install_requires = [line for line in f if "==" in line]

about = {}
with open(os.path.join(repo_path, "gytrash", "__about__.py"), "r", "utf-8") as f:
    exec(f.read(), about)
with open("README.md", "r", "utf-8") as f:
    readme = f.read()

setup(
    name=about["__title__"],
    version="0.0.10",
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=packages,
    package_dir={"gytrash": "gytrash"},
    package_data={"": ["*.cwl", "*.yaml"]},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=install_requires,
    setup_requires=install_requires,
    license=about["__license__"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    tests_require=[],
    project_urls={"Source": "https://github.com/trejas/gytrash"},
)
