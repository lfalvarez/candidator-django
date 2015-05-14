import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
INSTALLED_APPS = (
    'django_nose',
    'django.contrib.contenttypes',
    'popolo',
    'candidator',
)
SITE_ID = 1
SECRET_KEY = 'this-is-just-for-tests-so-not-that-secret'
ROOT_URLCONF = 'popolo.urls'
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
#LOGGING
LOGGING = {'version': 1,
           'disable_existing_loggers': True,
           'formatters': {'simple': {'format': '%(asctime)s %(levelname)s %(message)s'}},
           'handlers': {'console': {'level': 'DEBUG',
                                    'class': 'logging.StreamHandler',
                                    'formatter': 'simple'},
                        'null': {'level': 'DEBUG',
                                 'class': 'logging.NullHandler'
                                 },
                        },
           'loggers': {'django.db.backends': {'level': 'DEBUG',
                                              'handlers': ['null'],
                                              'propagate': False
                                              },
                       }
           }
#END LOGGING
