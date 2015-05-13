import os
from setuptools import setup, find_packages

setup(
    name = "django-candidator",
    version = "0.1",
    packages = find_packages(),
    test_suite="runtests.runtests",
    install_requires = [
        'django-popolo'
    ],
    dependency_links=[
        'http://github.com/openpolis/django-popolo/tarball/master#egg=django-popolo'
    ],
)
