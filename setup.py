import os
from setuptools import setup, find_packages

setup(
    name = "Candideitorg",
    version = "0.1",
    packages = find_packages(),
    test_suite="runtests.runtests",
)
