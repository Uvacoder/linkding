"""
Django settings for linkding webapp.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kgq$h3@!!vbb6*nzfz(dbze=*)zsroqa8gvc0#1gx$3cd8z99^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'bookmarks.apps.BookmarksConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sass_processor',
    'widget_tweaks',
    'django_generate_secret_key',
    'rest_framework',
    'rest_framework.authtoken',
    'background_task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'siteroot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bookmarks.context_processors.toasts',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

WSGI_APPLICATION = 'siteroot.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data', 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Website context path.
LD_CONTEXT_PATH = os.getenv('LD_CONTEXT_PATH', '')

LOGIN_URL = '/' + LD_CONTEXT_PATH + 'login'
LOGIN_REDIRECT_URL = '/' + LD_CONTEXT_PATH + 'bookmarks'
LOGOUT_REDIRECT_URL = '/' + LD_CONTEXT_PATH + 'login'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/' + LD_CONTEXT_PATH + 'static/'

# Collect static files in static folder
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Turn off SASS compilation by default
SASS_PROCESSOR_ENABLED = False
# Location where generated CSS files are saved
SASS_PROCESSOR_ROOT = os.path.join(BASE_DIR, 'tmp', 'build', 'styles')

# Add SASS preprocessor finder to resolve generated CSS
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# Include SASS styles into static path, otherwise they can not be found by the SASS preprocessor
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build'),
    os.path.join(BASE_DIR, 'bookmarks', 'styles'),
]

# REST framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

# Registration switch
ALLOW_REGISTRATION = False

# URL validation flag
LD_DISABLE_URL_VALIDATION = os.getenv('LD_DISABLE_URL_VALIDATION', False) in (True, 'True', '1')

# Background task enabled setting
LD_DISABLE_BACKGROUND_TASKS = os.getenv('LD_DISABLE_BACKGROUND_TASKS', False) in (True, 'True', '1')

# django-background-tasks
MAX_ATTEMPTS = 5
# How many tasks will run in parallel
# We want to keep this low to prevent SQLite lock errors and in general not to consume too much resources on smaller
# specced systems like Raspberries. Should be OK as tasks are not time critical.
BACKGROUND_TASK_RUN_ASYNC = True
BACKGROUND_TASK_ASYNC_THREADS = 2

# Enable authentication proxy support if configured
LD_ENABLE_AUTH_PROXY = os.getenv('LD_ENABLE_AUTH_PROXY', False) in (True, 'True', '1')
LD_AUTH_PROXY_USERNAME_HEADER = os.getenv('LD_AUTH_PROXY_USERNAME_HEADER', 'REMOTE_USER')
LD_AUTH_PROXY_LOGOUT_URL = os.getenv('LD_AUTH_PROXY_LOGOUT_URL', None)

if LD_ENABLE_AUTH_PROXY:
    # Add middleware that automatically authenticates requests that have a known username
    # in the LD_AUTH_PROXY_USERNAME_HEADER request header
    MIDDLEWARE.append('bookmarks.middlewares.CustomRemoteUserMiddleware')
    # Configure auth backend that does not require a password credential
    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.RemoteUserBackend',
    ]
    # Configure logout URL
    if LD_AUTH_PROXY_LOGOUT_URL:
        LOGOUT_REDIRECT_URL = LD_AUTH_PROXY_LOGOUT_URL
