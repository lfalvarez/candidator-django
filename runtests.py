#!/usr/bin/env python

import sys

from django.conf import settings
import django

if not settings.configured:
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = 'testing_settings'
    from distutils.version import StrictVersion
    if not StrictVersion(django.get_version()) < StrictVersion("1.8"):
        django.setup()

from django.test.utils import get_runner


def runtests():
    test_runner_klass = get_runner(settings)
    test_runner = test_runner_klass(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['candidator', ])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
