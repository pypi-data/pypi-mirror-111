#!/usr/bin/env python3

from distutils.core import setup
import os

setup(
    name="pynvidiasmi",
    version="1.0.1",
    description="Query nvidia-smi and return list of dictionaries with queried attributes",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Dario Balboni",
    author_email="dario.balboni.96+pynvidiasmi@gmail.com",
    url="https://gitlab.com/trenta3/pynvidiasmi",
    py_modules=["pynvidiasmi"],
    license="GPL-3.0",
    install_requires=[],
)
