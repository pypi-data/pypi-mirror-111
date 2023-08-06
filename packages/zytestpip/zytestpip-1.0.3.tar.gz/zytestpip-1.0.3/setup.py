#!/usr/bin/env python

import re

import setuptools

version = "1.0.3"


setuptools.setup(
    name="zytestpip",
    version=version,
    author="bwz0328",
    author_email="bwz0328@126.com",
    description="This is the SDK for example.",
    long_description="",
    long_description_content_type="text/markdown",
    url="http://example.com",
    install_requires=[
        'requests!=2.9.0',
        'lxml>=4.2.3',
        'monotonic>=1.5',
    ],
    packages=setuptools.find_packages(exclude=("test"))
)