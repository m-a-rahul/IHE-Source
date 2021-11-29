import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = ['http://34.96.210.147/']

ADMINS = [('Rahul', 'antorahul070@gmail.com'),
          ('Pritish', 'princepritish26@gmail.com'),
          ('Aditya', 'ms.adityaraj@gmail.com')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'admin_honeypot',

    'rest_framework',
    'rest_framework.authtoken',

    'rest_auth',
    'rest_auth.registration',

    'corsheaders',
    'django_rest_passwordreset',

    'django_countries',
    'phonenumber_field',

    'custom_auth',
    'user_details',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'src.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ['DATABASE_ENGINE'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': os.environ['DATABASE_PORT']
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'src.utils.my_jwt_response_handler'
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

if not DEBUG:
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer', ]


CORS_ORIGIN_WHITELIST = [
    os.environ['FRONTEND_URL'],
]

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'none'

EMAIL_BACKEND = os.environ['EMAIL_BACKEND']

EMAIL_USE_TLS = bool(os.environ['EMAIL_USE_TLS'])

EMAIL_HOST = os.environ['EMAIL_HOST']

EMAIL_PORT = int(os.environ['EMAIL_PORT'])

EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

EMAIL_HOST_USER = os.environ['EMAIL_ID']

DEFAULT_FROM_EMAIL = os.environ['EMAIL_ID']

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

FRONTEND_URL = os.environ['FRONTEND_URL']

ADMIN_URL = os.environ['ADMIN_URL']

BLOCK_CRYPTO_KEY = os.environ['BLOCK_CRYPTO_KEY']

BLOCK_ACCESS_KEY = os.environ['BLOCK_ACCESS_KEY']

BLOCK_NONCE = os.environ['BLOCK_NONCE']

BLOCK_NODES = set(os.environ['BLOCK_NODES'].split(','))
