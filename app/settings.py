
from ms_identity_web.configuration import AADConfig
from ms_identity_web import IdentityWebPython

import os

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("SECRET_KEY","ERROR: `SECRET_KEY` NOT FOUND IN ENVIRONMENT VARIABLES")

DEBUG = os.getenv("DEBUG","ERROR: `DEBUG` NOT FOUND IN ENVIRONMENT VARIABLES")

ALLOWED_HOSTS = []


# Application definition
AAD_CONFIG = AADConfig.parse_json(file_path='aad.config.json')
AAD_CONFIG.client.client_id = os.getenv("AAD_CLIENT_ID","ERROR: `AAD_CLIENT_ID` NOT FOUND IN ENVIRONMENT VARIABLES")
AAD_CONFIG.client.client_credential = os.getenv("AAD_CLIENT_CREDENTIAL","ERROR: `AAD_CLIENT_CREDENTIAL` NOT FOUND IN ENVIRONMENT VARIABLES")
AAD_CONFIG.client.authority = f"https://login.microsoftonline.com/{os.getenv('AAD_TENANT_ID','ERROR: `AAD_TENANT_ID` NOT FOUND IN ENVIRONMENT VARIABLES')}"

MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
ERROR_TEMPLATE = 'auth/{}.html' # for rendering 401 or other errors from msal_middleware

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_twin_2d'
]

MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
    # Add whitenoise middleware after the security middleware             
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  
    'ms_identity_web.django.middleware.MsalMiddleware'       
]

ROOT_URLCONF = 'app.urls'

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
                'app.context_processors.context'
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "./logs/app_log.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

AZURE_STORAGE_KEY = os.environ.get('AZURE_STORAGE_KEY', False)+"==" # wierd env string issue
AZURE_ACCOUNT_NAME = os.environ.get('AZURE_ACCOUNT_NAME', False)
AZURE_STATIC_CONTAINER = os.environ.get('AZURE_STATIC_CONTAINER', 'static')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'  # CDN URL
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{AZURE_STATIC_CONTAINER}/'
STATIC_ROOT = os.path.join("app", "static")
DEFAULT_FILE_STORAGE = 'web.backend.AzureMediaStorage'
STATICFILES_STORAGE  = 'web.backend.AzureStaticStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
