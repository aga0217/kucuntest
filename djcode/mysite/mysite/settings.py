# -*- coding: utf-8 -*-
"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.contrib.messages import constants as message_constants
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xaff_$x*^!27!xn&@2acsa@waai0gzxfh87df%3c-w3^gf6h7w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'braces',
    'books',
    'kucuntest',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #change local Language test(fang fa bu cheng gong ti shi "mei you localemiddleware")
    #'django.middleware.locale.LocaleMiddleware'
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'kucuntestdb',
        'USER': 'aga0217',
        'PASSWORD': '155257aga',
        'HOST': '116.113.44.166',
        'PORT': '3306',


    }
}

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'kucuntestdb',
        'USER': 'aga0217',
        'PASSWORD': '155257aga',
        'HOST': '162.243.159.81',
        'PORT': '3306',


    }
}

"""
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'kucuntestdb',
        'USER': 'aga0217',
        'PASSWORD': '155257aga',
        'HOST': '127.0.0.1',
        'PORT': '3306',


    }
}
"""
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/home/python/staticdd/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/home/python/djcode/mysite/mysite/template',
    '/home/python/djcode/mysite/kucuntest/template/',
)

STATICFILES_DIRS = (
	                  '/home/python/djcode/mysite/kucuntest/static',
	               )
#因为bootstrap中没有ERROR属性，故没有办法为ERROR提供相应颜色，所以将ERROR指定为danger属性（实现根据属性自动更改颜色的功能）
MESSAGE_TAGS = {message_constants.DEBUG: 'debug',
                message_constants.INFO: 'info',
                message_constants.SUCCESS: 'success',
                message_constants.WARNING: 'warning',
                message_constants.ERROR: 'danger',}


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1209600
LOGIN_REDIRECT_URL = "/hetong/hetonglist/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
