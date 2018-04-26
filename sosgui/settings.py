"""
Django settings for sosgui project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

log = open('log/settings.log', 'a', 0)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tgi*mct^mr^%d=@(e5ix#!elxk5q3i3(&zzbt-!5op-#%h3!h9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'testserver',
]

APPEND_SLASH = False

STATIC_ROOT = os.path.join(BASE_DIR, "assets")

AUTH_USER_MODEL = 'sosdb_auth.SosdbUser'

# Application definition

INSTALLED_APPS = [
    'httpproxy',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'component',
    'container',
    'plot',
    'jobs',
    'objbrowser',
    'sos_db',
    'sosdb_auth',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

try:
    import ldms_settings
    INSTALLED_APPS.extend(ldms_settings.INSTALLED_APPS)
except:
    pass

try:
    import grafana_settings
    INSTALLED_APPS.extend(grafana_settings.INSTALLED_APPS)
except:
    pass

try:
    import baler_settings
    INSTALLED_APPS.extend(baler_settings.INSTALLED_APPS)
    log.write("INFO: baler_settings loaded\n")
except:
    log.write("INFO: baler_settings NOT loaded\n")

MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

if DEBUG:
    MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'sosgui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
            '../ovis-baler-ui/templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sosgui.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#CACHES = {
#    'default': {
#	'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#	'LOCATION': '/var/www/tmp/django_cache',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

#SESSION_FILE_PATH = '/tmp/sessions'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
#    '/static/',
    'static',
    '../ovis-baler-ui/static',
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 86400
SOS_ROOT = "/home/narate/projects/baler/test/simple_test4/store"
LOG_FILE = "log/sosgui.log"
LOG_DATE_FMT = "%F %T"
ODS_LOG_FILE = "log/ods.log"
ODS_LOG_MASK = "255"
ODS_GC_TIMEOUT = 10
LDMS_SETTINGS = "ldms.cfg"
BSTORE_PLUGIN="bstore_sos"
#os.environ.setdefault("BSTORE_PLUGIN_PATH", "/opt/ovis/lib")
os.environ.setdefault("SET_POS_KEEP_TIME", "3600")
SYSLOG_SETTINGS = "syslog.cfg"
TIMEZONE=-(5*3600)


try:
    cfg_fp = open(LDMS_SETTINGS, 'r')
    LDMS_CFG = json.load(cfg_fp)
    log.write(repr(LDMS_CFG)+'\n')
except Exception, e:
    log.write("LDMS_SETTINGS ERROR: " + repr(e)+'\n')
    LDMS_CFG = { "aggregators" : [] }

try:
    cfg_fp = open(SYSLOG_SETTINGS, 'r')
    SYSLOG_CFG = json.load(cfg_fp)
except Exception as e:
    log.write('SYSLOG_SETTINGS ERR '+repr(e)+'\n')
    SYSLOG_CFG = { "stores" : [] }

# Django LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # The parent of all loggers
        '': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        }
    }
}
