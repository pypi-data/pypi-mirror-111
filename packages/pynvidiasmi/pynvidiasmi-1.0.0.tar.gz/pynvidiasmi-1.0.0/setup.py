#!/usr/bin/env python3

from distutils.core import setup

setup(
    name="pynvidiasmi",
    version="1.0.0",
    description="Query nvidia-smi and return list of dictionaries with queried attributes",
    long_description=open("README.md").read(),
    author="Dario Balboni",
    author_email="dario.balboni.96+pynvidiasmi@gmail.com",
    url="https://gitlab.com/trenta3/pynvidiasmi",
    py_modules=["pynvidiasmi"],
    license="LICENSE",
    install_requires=[],
)
