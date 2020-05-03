import os
from setuptools import setup, find_packages

setup(
    name = "django-candidator",
    version = "0.1",
    packages = find_packages(),
    test_suite="runtests.runtests",
    install_requires = [
        'mysociety-django-popolo',
        'six',
        'django-autoslug'
    ],
    dependency_links=[
        'https://github.com/mysociety/django-popolo/tarball/master#egg=mysociety-django-popolo',

    ],
)
