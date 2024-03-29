"""
Django settings for TeferetPROJECT project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

#Load .env path
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')  

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["teferet-production.up.railway.app","teferet.pythonanywhere.com","localhost","127.0.0.1"]
CSRF_TRUSTED_ORIGINS = ["https://teferet-production.up.railway.app"]

# Application definition

INSTALLED_APPS = [
    
    #Custom Admin Platform
    'jazzmin',

    #Load more feature
    'django_htmx',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #Custom APP
    'CoreAPP',
    'UserAuthsAPP',
    'ShopAPP',
    'OrderAPP',
    'BlogAPP',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'TeferetPROJECT.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'Templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ShopAPP.context_processors.counter',
                'UserAuthsAPP.context_processors.loggedUser',
            ],
        },
    },
]

WSGI_APPLICATION = 'TeferetPROJECT.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
prod = os.environ.get('PROD_MODE')  
if prod == "True":
   
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ["PGDATABASE"],
        'USER': os.environ["PGUSER"],
        'PASSWORD': os.environ["PGPASSWORD"],
        'HOST': os.environ["PGHOST"],
        'PORT': os.environ["PGPORT"],
        }
    }
    print("Using Postgresql database -- Production")

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("Using Sqlite database -- Dev")


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True







SESSION_EXPIRE_SECONDS = 900  # 1 hour
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_ENGINE  = "django.contrib.sessions.backends.signed_cookies"
# SESSION_TIMEOUT_REDIRECT = 'accounts/login'




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL       = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT      = os.path.join(BASE_DIR,'staticfiles')

# Media files (mp4, mp3, Images)
MEDIA_URL        = '/media/'
MEDIA_ROOT       = os.path.join(BASE_DIR,'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




#Jazzmin settings

JAZZMIN_SETTINGS = {    
    'site_logo'  : 'images/icons/logo.png',
    'site_brand' : 'TEFERET',
    'copyright': "TEFERET",
    "welcome_sign": "Welcome to TEFERET Admin Interface",
    "site_title": "TEFERET Admin",



}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'stronguy.peter.allogho@gmail.com'
EMAIL_HOST_PASSWORD = 'oakwdnebxthtxnfu'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
# DEFAULT_FROM_EMAIL = 'Teferet Customer Team <noreply@Teferet.com>'


SECURE_CROSS_ORIGIN_OPENER_POLICY='same-origin-allow-popups'