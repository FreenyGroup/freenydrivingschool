"""
Django settings for educa project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import os
import django_on_heroku
import dj_database_url
from dotenv import load_dotenv, find_dotenv
from decouple import config
from django.urls import reverse_lazy

load_dotenv(find_dotenv())
DEBUG=False

BASE_DIR = Path(__file__).resolve().parent.parent

SITE_ID = 1

INSTALLED_APPS = [
    'user',
    'clearcache',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'django_extensions',
    'courses.apps.CoursesConfig',
    'students.apps.StudentsConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'payment.apps.PaymentConfig',
    'coupons.apps.CouponsConfig',
    "info.apps.InfoConfig",
    'embed_video',
    'rest_framework',
    'durationwidget',
    'crispy_forms',
    "crispy_tailwind",
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.postgres',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'educa.urls'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'educa.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = reverse_lazy('student_course_list')

CART_SESSION_ID = 'cart'

INTERNAL_IPS = [
    '127.0.0.1',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
      'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

if DEBUG == True:
    ALLOWED_HOSTS = ['192.168.0.101', 'localhost', '127.0.0.1', '[::1]', '0.0.0.0']
    SECRET_KEY = config('SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET')
    STRIPE_API_VERSION = config('STRIPE_API_VERSION')
    EMAIL_BACKEND = config('EMAIL_BACKEND')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
    CELERY_BROKER_URL = config('CELERY_BROKER_URL')
    broker_url = config('broker_url')
    GOOGLE_MAPS_API_KEY=config('GOOGLE_MAPS_API_KEY')
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 60 * 15
    CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'
    STATIC_URL = 'static/'
    STATIC_ROOT = BASE_DIR / 'static'
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

if DEBUG == False:
    ALLOWED_HOSTS = [
        'https://freenydrivingschool.herokuapp.com/',
        'https://freenydrivingschool.herokuapp.com',
        'freenydrivingschool.herokuapp.com/',
        'freenydrivingschool.herokuapp.com',
        'https://www.freenydrivingschool.herokuapp.com/',
        'https://www.freenydrivingschool.herokuapp.com',
        'www.freenydrivingschool.herokuapp.com/',
        'www.freenydrivingschool.herokuapp.com',
        'https://freenydrivingschool.com/',
        'https://freenydrivingschool.com',
        'freenydrivingschool.com/',
        'freenydrivingschool.com',
        'https://www.freenydrivingschool.com/',
        'https://www.freenydrivingschool.com',
        'www.freenydrivingschool.com/',
        'www.freenydrivingschool.com'
        ]
    CSRF_TRUSTED_ORIGINS = [
        'https://freenydrivingschool.herokuapp.com/',
        'https://freenydrivingschool.herokuapp.com',
        'https://www.freenydrivingschool.herokuapp.com/',
        'https://www.freenydrivingschool.herokuapp.com',
        'https://freenydrivingschool.com/',
        'https://freenydrivingschool.com',
        'https://www.freenydrivingschool.com/',
        'https://www.freenydrivingschool.com',
        ]
    SECRET_KEY = config('SECRET_KEY')
    DEBUG_PROPAGATE_EXCEPTIONS = True
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt' : "%d/%b/%Y %H:%M:%S"
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'educa': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        }
    }

    django_on_heroku.settings(locals(), staticfiles=False)
    STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET')
    STRIPE_API_VERSION = config('STRIPE_API_VERSION')
    EMAIL_BACKEND = config('EMAIL_BACKEND')
    EMAIL_HOST = config('EMAIL_HOST')
    EMAIL_HOST_USER = config('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = config('SENDGRID_API_KEY')
    CELERY_BROKER_URL = config('CELERY_BROKER_URL')
    broker_url = config('broker_url')
    GOOGLE_MAPS_API_KEY=config('GOOGLE_MAPS_API_KEY')
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    #SECURE_SSL_REDIRECT = True
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 60 * 15  # 15 minutes
    CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_QUERYSTRING_AUTH = False
    AWS_DEFAULT_ACL='public-read'
    AWS_S3_FILE_OVERWRITE = False
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

def get_cache():
  import os
  try:
    servers = os.environ['MEMCACHIER_SERVERS']
    username = os.environ['MEMCACHIER_USERNAME']
    password = os.environ['MEMCACHIER_PASSWORD']
    return {
      'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'TIMEOUT': None,
        'LOCATION': servers,
        'OPTIONS': {
          'username': username,
          'password': password,
        }
      }
    }
  except:
    return {
      'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
      }
    }

CACHES = get_cache()

broker_pool_limit = 1 
broker_heartbeat = None 
broker_connection_timeout = 30  
result_backend = None 
event_queue_expires = 60 
worker_prefetch_multiplier = 1 
worker_concurrency = 50 

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

AUTH_USER_MODEL = 'user.User'

CONTACT_EMAIL='contact@freenydrivingschool.com'

ADMIN_EMAIL=['contact@freenydrivingschool.com']

