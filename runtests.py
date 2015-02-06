#!/usr/bin/env python

import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django_nose',
            'django.contrib.contenttypes',
            'popolo',
            'candidator',
        ),
        SITE_ID=1,
        TEST_RUNNER = 'django_nose.NoseTestSuiteRunner',
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF='popolo.urls',
    )

from django.test.utils import get_runner


def runtests():
    test_runner_klass = get_runner(settings)
    test_runner = test_runner_klass(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['candidator', ])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
