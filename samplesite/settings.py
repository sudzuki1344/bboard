"""
Django settings for samplesite project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import re

from captcha.conf.settings import CAPTCHA_TIMEOUT, CAPTCHA_LENGTH
from django.conf.global_settings import STATICFILES_DIRS, ABSOLUTE_URL_OVERRIDES, MEDIA_URL, AUTH_USER_MODEL, \
    EMAIL_BACKEND, DEFAULT_FROM_EMAIL, EMAIL_HOST, CACHE_MIDDLEWARE_ALIAS, CACHE_MIDDLEWARE_SECONDS
from django.contrib import messages
from django_bootstrap5.core import BOOTSTRAP5

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=tmq^(flv8$!!=k(oo@xt-65ha*254nv%aoj10z$uk*wyk%*3o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'django.contrib.postgres',

    'captcha',
    'precise_bbcode',
    'django_bootstrap5',
    'easy_thumbnails',
    'rest_framework',
    'corsheaders',

    'bboard',  # 'bboard.apps.BboardConfig',
    'testapp',
    # 'todolist',

    'django_cleanup',  # всегда в самом низу!!!
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware',  # для кэша
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',  # для кэша

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'bboard.middleware.RubricMiddleware',
]

ROOT_URLCONF = 'samplesite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'bboard.middleware.rubrics',
            ],
        },
    },
]

WSGI_APPLICATION = 'samplesite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ATOMIC_REQUEST': True,  # False,
        # 'AUTOCOMMIT': False,     # True,
    }
    # "default": {
    #     "ENGINE": "django.db.backends.postgresql_psycopg2",
    #     "NAME": "django_db",
    #     "USER": "db_user",
    #     "PASSWORD": "12345",
    #     "HOST": "127.0.0.1",
    #     "PORT": "5432",
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # 'OPTIONS': {'min_length': 10}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'bboard.validators.NoForbiddenCharsValidator',
        'OPTIONS': {'forbidden_chars': (' ', ',', '.', ':', ';')}
    },
]

# AUTH_USER_MODEL = 'testapp.models.AdvUser'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Almaty'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
# STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ABSOLUTE_URL_OVERRIDES = {
#     'bboard.rubric': lambda rec: f"{rec.pk}/"
# }

DEFAULT_CHARSET = 'utf-8'

# LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = 'bboard:index'
LOGOUT_REDIRECT_URL = 'bboard:index'
# PASSWORD_RESET_TIMEOUT = 60 * 60 * 24 * 3  # 259_200

# CAPTCHA
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'

# CAPTCHA_TIMEOUT = 5  # минут
CAPTCHA_LENGTH = 6  # 4 по умолчанию

# CAPTCHA_WORDS_DICTIONARY = BASE_DIR / 'static/bboard/words.txt'

# CAPTCHA_LETTER_ROTATION = (-95, 95)

# DATA_UPLOAD_MAX_MEMORY_SIZE = 2_621_440  # 2.5 Mb
# DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# BBCODE
# BBCODE_NEWLINE = '<br>'
# BBCODE_ALLOW_CUSTOM_TAGS = False

BOOTSTRAP5 = {
    'required_css_class': 'required',
    'success_css_class': 'has-success',
    'error_css_class': 'has-error',
}

# easy-thumbnails
THUMBNAIL_ALIASES = {
    'bboard.Bb.img': {
        'default': {
            'size': (500, 300),
            'crop': 'scale',
        },
    },
    'testapp': {
        'default': {
            'size': (400, 300),
            'crop': 'smart',
            'bw': True,
        },
    },
    '': {
        'default': {
            'size': (180, 240),
            'crop': 'scale',
        },
        'big': {
            'size': (480, 640),
            'crop': '10,10',
        },
    },
}

THUMBNAIL_DEFAULT_OPTIONS = {
    'quality': 90,
    'subsampling': 1,
}

# THUMBNAIL_MEDIA_URL = '/media/thumbnail/'
# THUMBNAIL_MEDIA_ROOT = BASE_DIR / 'media/thumbnail'
THUMBNAIL_SUBDIR = 'thumbs'
# THUMBNAIL_PREFIX = 'thumb_'
# THUMBNAIL_EXTENSION = 'jpg'
# THUMBNAIL_TRANSPARENCY_EXTENSION = 'png'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)


# SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # по умолчанию
# SESSION_ENGINE = 'django.contrib.sessions.backends.file'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
# SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
# SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

# SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
# MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# MESSAGE_LEVEL = 20
# MESSAGE_LEVEL = messages.DEBUG

# CRITICAL = 50
# MESSAGE_TAGS = {
#     CRITICAL: 'critical'
# }

#######################
######## Email ########
#######################

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

DEFAULT_FROM_EMAIL = 'webmaster@localhost'

### 'django.core.mail.backends.smtp.EmailBackend' ###
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""

EMAIL_USE_LOCALTIME = True

### 'django.core.mail.backends.filebased.EmailBackend' ###
# EMAIL_FILE_PATH = BASE_DIR / 'email'

# ADMINS = [
#     ('admin', 'admin@supersite.kz'),
#     ('admin2', 'admin2@supersite.kz'),
#     ('admin3', 'admin3@supersite.kz'),
# ]
#
# MANAGERS = [
#     ('manager', 'manager@supersite.kz'),
#     ('manager2', 'manager2@supersite.kz'),
#     ('manager3', 'manager3@supersite.kz'),
# ]


#######################
#######  Cache  #######
#######################

CACHES = {
    # 'default': {
    #     # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
    #     # 'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #     # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #     'LOCATION': 'cache1',
    # },
    # 'special': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #     'LOCATION': 'cache2',
    # },
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
        'TIMEOUT': 120,  # по умолчанию 300 сек.
        'OPITIONS': {
            'MAX_ENTRIES': 200,
        }
    },
    'redis': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379/0',
    },
}

# CACHE_MIDDLEWARE_ALIAS = "default"
# CACHE_MIDDLEWARE_SECONDS = 10



CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
# ]
# CORS_ALLOWED_ORIGINS_REGEX = [
#     r"^https://.*\.example\.com$",
# ]
# CORS_ALLOW_METHODS = [
#     "DELETE",
#     "GET",
#     "OPTIONS",
#     "PATCH",
#     "POST",
# ]

CORS_URLS_REGEX = re.compile(r'^/api/.*$')


# CORS_ALLOW_CREDENTIALS = True

