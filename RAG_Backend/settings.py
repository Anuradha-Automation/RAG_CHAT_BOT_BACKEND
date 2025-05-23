"""
Django settings for RAG_Backend project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from datetime import datetime
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from django.conf.urls.static import static

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
import pymysql
pymysql.install_as_MySQLdb()
AUTH_USER_MODEL = 'RAG_CHATBOT_BACKEND_APIS.CustomUser'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4rui8%q0xhb&$s3ju5-yp^j0i5&@i(pyrople(9y^9g723q@5y'
# BASE_APP_URL = os.getenv("BASE_APP_URL", "http://127.0.0.1:8000")  # Default to localhost
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['3.96.160.107', '0.0.0.0','127.0.0.1','chatbot.exoticaitsolutions.com']


BASE_DIR = Path(__file__).resolve().parent.parent
CORS_ALLOW_ALL_ORIGINS = True  # Allows all domains to access your API
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS","fetch"]

CORS_ALLOW_HEADERS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'RAG_CHATBOT_BACKEND_APIS',
    'drf_yasg',
    'django.contrib.humanize',
    "corsheaders"    
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Add this at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]
DJANGO_SONAR = {
    "ENABLED": True,  # Ensure this is a boolean, not a dictionary
}


ROOT_URLCONF = 'RAG_Backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                 'django.template.context_processors.media',
                 'RAG_CHATBOT_BACKEND_APIS.context_processors.chatbot_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'RAG_Backend.wsgi.application'


# __import__('pysqlite3')
# import sys

# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')




DB_TYPE = os.getenv('DB_TYPE')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if DB_TYPE == 'sqlite3':
    print('Using SQLite3')
    DATABASES = {
    "default": { "ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3", }  }
else:
    print('Using MySQL')
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT =''
# This should be the directory where collectstatic will store files
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# These are directories where Django will look for static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),

]

# Application definition
APPEND_SLASH =False

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_ENGINE = "django.contrib.sessions.backends.db"  #  Ensure this is set
SESSION_COOKIE_AGE = 1209600  # adjust as needed
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
APPEND_SLASH = True
CSRF_TRUSTED_ORIGINS = [
]
EMAIL_HOST_USER = "pythonweb@exoticaitsolutions.com"
DEFAULT_FROM_EMAIL = "pythonweb@exoticaitsolutions.com"
SERVER_EMAIL = "pythonweb@exoticaitsolutions.com"
# Session expires after 30 minutes of inactivity
SESSION_COOKIE_AGE = 1800  # 30 minutes in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Logout on browser close
SESSION_SAVE_EVERY_REQUEST = True  # Reset session timer on activity


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.hostinger.com"
EMAIL_PORT = 465
EMAIL_USE_SSL = True  # Since we use port 465
EMAIL_USE_TLS = False  # Must be False when using SSL
EMAIL_HOST_USER = "pythonweb@exoticaitsolutions.com"
EMAIL_HOST_PASSWORD = "Webpython@123#"  # Ensure this is correct
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this line is present

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Your custom static files
]
MEDIA_URL = f'storage/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'storage/media')
COPY_ROOT = os.path.join(BASE_DIR, 'storage/Copy_Records/')
LOG_DIR = os.path.join(BASE_DIR, f'storage/logs/{datetime.now().strftime("%Y-%m-%d")}')
if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_INFO = os.path.join(LOG_DIR, f'django_info_{datetime.now().strftime("%Y-%m-%d")}.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()

class NoDebugFilter(logging.Filter):
    """Filter out DEBUG logs for specific handlers."""
    def filter(self, record):
        return record.levelno > logging.DEBUG  # Excludes DEBUG logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_INFO,  # Use LOG_FILE_INFO for file logs
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'myapp': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
DJANGO_SONAR = {
    'excludes': [
        STATIC_URL,
        MEDIA_URL,
        '/sonar/',
        '/admin/',
        '/__reload__/',
    ],
}