#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from os.path import dirname, join

from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, "__init__.py"), encoding="utf-8").read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    return [
        dirpath
        for dirpath, dirnames, filenames in os.walk(package)
        if os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]


def get_package_data(package):
    walk = [
        (dirpath.replace(package + os.sep, "", 1), filenames)
        for dirpath, dirnames, filenames in os.walk(package)
        if not os.path.exists(os.path.join(dirpath, "__init__.py"))
    ]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename) for filename in filenames])
    return {package: filepaths}


setup(
    name="webpay_be",
    version=get_version("webpay_be"),
    url="https://github.com/intsynko/webpay_be",
    license="MIT",
    description="Simple python client for webpay.by api",
    long_description_content_type="text/x-rst",
    long_description=open(join(dirname(__file__), "README.rst"), encoding="utf-8").read(),
    author="Intsyn Konstantin",
    author_email="intsyn@mail.ru",
    packages=get_packages("webpay_be"),
    package_data=get_package_data("webpay_be"),
    include_package_data=True,
    install_requires=[],
    python_requires=">=2.7",
    zip_safe=False,
    platforms="any",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],
)