from datetime import timedelta

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    'doberman',
)

SECRET_KEY = 'secret-for-test-secret-secret'

ROOT_URLCONF = 'doberman.tests.test_urls'

TEMPLATE_DIRS = (
    "doberman/tests/templates",
)


DOBERMAN_MAX_FAILED_ATTEMPTS = 5
DOBERMAN_LOCKOUT_TIME = 60*10  # 10 minutos
