from pathlib import Path


# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY
SECRET_KEY = 'django-insecure-test-key'

DEBUG = True

ALLOWED_HOSTS = []


# INSTALLED APPS
INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CORE APP
    'core',

]


# MIDDLEWARE
MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


# ROOT URL
ROOT_URLCONF = 'facerestore.urls'


# TEMPLATES
TEMPLATES = [

    {
        'BACKEND':
        'django.template.backends.django.DjangoTemplates',

        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {

            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                # MEDIA SUPPORT
                'django.template.context_processors.media',

            ],

        },

    },

]


# WSGI
WSGI_APPLICATION = 'facerestore.wsgi.application'


# DATABASE
DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = []


# LANGUAGE
LANGUAGE_CODE = 'en-us'


# TIMEZONE
TIME_ZONE = 'Asia/Kolkata'


# INTERNATIONALIZATION
USE_I18N = True

USE_TZ = True


# STATIC FILES
STATIC_URL = 'static/'

STATICFILES_DIRS = [

    BASE_DIR / 'static',

]


# MEDIA FILES
MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'