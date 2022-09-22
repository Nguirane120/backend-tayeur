"""
Django settings for fewnu_compta project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import dj_database_url
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yjbae$vgtfdjk3y1)er)m4n(*9)4f528owz8*vm6p*du3qj(+p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_rest_passwordreset',
    'drf_yasg',
    'drf_yasg2',
    'api_fewnu_compta.apps.ApiFewnuComptaConfig',
    'whitenoise.runserver_nostatic',
    "corsheaders",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django.middleware.common.CommonMiddleware",
]


# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
# ]

ROOT_URLCONF = 'fewnu_compta.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'fewnu_compta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# for herokuapp
# DATABASES = { 'default': dj_database_url.config() }


# for local 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'docker',
        'USER': 'sultan',
        'PASSWORD': 'jepasse',
        'HOST': 'db',
        # 'HOST': '127.0.0.1', for local
        'PORT': '5432',
    }
}

# for docker 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('POSTGRES_NAME'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# SESSION_COOKIE_HTTPONLY = True

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = 'static/'
AUTH_USER_MODEL = 'api_fewnu_compta.User'
MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') #le chemin du serveur pour stocker les fichiers sur l’ordinateur. 
MEDIA_URL = '/media/'# comment l’URL de référence permettant au navigateur d’accéder aux fichiers via Http.
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# for cors 
CSRF_HEADER_NAME = "HTTP_X_CSRFTOKEN"
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-csrf-token",
    "csrftoken",
    "x-requested-with",
    "http_x_csrftoken"
]

# CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1",
    "https://fewnu-compta.web.app",
    "http://fewnu-django.herokuapp.com",
    "http://*.herokuapp.com",
    "http://fewnu-compta.web.app",
    "http://*.web.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://127.0.0.1:3000",
    "http://fewnu-django.herokuapp.com",
    "http://*.herokuapp.com",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "http://fewnu-compta.web.app",
    "http://localhost:3000",
    "http://*.web.app",
    "https://fewnu-compta.web.app",
]
CORS_ALLOW_CREDENTIALS = True
MIDDLEWARE_CLASSES = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware"
]
# SESSION_COOKIE_DOMAIN = "*.herokuapp.com"
# CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_NAME = "XSRF-TOKEN"


REST_FRAMEWORK  ={
# anyone can visit it and input data
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
   ]
}

# SMTP Configuration 

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'projetbakeli@gmail.com'
EMAIL_HOST_PASSWORD ='xiuiqnmtkjhpzmtc'