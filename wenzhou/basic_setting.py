#encoding=utf-8
"""
Django settings for wenzhou project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=8inqcu$p1=yu*a9%!h75q13i8f28hqdtbt1!_obsy=s7%j4+k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    "grappelli",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "south",
    "cohost",
    "wzauth",
    "crispy_forms",
)

GRAPPELLI_ADMIN_TITLE='后台管理系统'


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #管理界面显示为中文
    "django.middleware.locale.LocaleMiddleware",
)

TEMPLATE_LOADER = (
    "django.template.loaders.filesystem.Loader",
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "cohost.context_processors.common",
    "django.core.context_processors.request",
    )

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)


ROOT_URLCONF = 'wenzhou.urls'

WSGI_APPLICATION = 'wenzhou.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'bing.db'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    'cohost/statics',
    'wzauth/statics',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


#User Custom
CRISPY_TEMPLATE_PACK = 'bootstrap3'
#设置登陆的url  -- login_require
LOGIN_URL = '/login'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TASK_RESULT_EXPIRES=3600

from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #     'task': 'tasks.add',
    #     'schedule': timedelta(seconds=3),
    #     'args': (16, 16)
    # },
    'bing-every-0.5-hour': {
        'task': 'tasks.ip_bing',
        'schedule': crontab(day_of_month='2'),
    },


}

CELERY_TIMEZONE = 'UTC'


