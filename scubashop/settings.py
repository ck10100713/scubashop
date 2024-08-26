from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
# DEBUG = True
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','ec2-100-27-173-161.compute-1.amazonaws.com', 'penguindiving.com']

CSRF_TRUSTED_ORIGINS = [
    'https://767f-180-177-8-38.ngrok-free.app'
]
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'drf_yasg',
    'rest_framework',
    'account_center',
    'shop',
    'cart',
    'orders',
    'payment',
    # oauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django 的默認認證後台
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth 的認證後台
]

SITE_ID = 1  # 這裡的 1 是預設的站點 ID

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'scubashop.urls'

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + '/templates'],
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

WSGI_APPLICATION = 'scubashop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
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

TIME_ZONE = 'Asia/Taipei'

LANGUAGE_CODE = 'zh-hant'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/account_center/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# STATIC_ROOT = '/home/ubuntu/scubashop/staticfiles'


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR,'static'),
#     os.path.join(BASE_DIR,'media'),
# ]

# settings.py

STATIC_URL = '/static/'

# 設置靜態文件的收集目錄
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 設置靜態文件的額外目錄
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# settings.py
# APPEND_SLASH = False
CART_SESSION_ID = 'cart'  # 定義購物車在 session 中的鍵名

from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

# 從 .env 檔案中讀取設定
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
FACEBOOK_CLIENT_ID = os.getenv('FACEBOOK_CLIENT_ID')
FACEBOOK_CLIENT_SECRET = os.getenv('FACEBOOK_CLIENT_SECRET')

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'APP': {
            'client_id': GOOGLE_CLIENT_ID,
            'secret': GOOGLE_CLIENT_SECRET,
            'key': ''
        }
    },
    'facebook': {
        'APP': {
            'client_id': FACEBOOK_CLIENT_ID,
            'secret': FACEBOOK_CLIENT_SECRET,
        },
        'SCOPE': [
            'email',
        ],
        'AUTH_PARAMS': {
            'auth_type': 'reauthenticate',
        },
        'FIELDS': [
            'id',
            'email',
            'name',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
    },
}

ACCOUNT_ADAPTER = 'account_center.adapter.CustomAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'account_center.adapter.CustomSocialAccountAdapter'

# that is a right way to redirect user to complete profile after signup in 3rd oauth.
# ACCOUNT_SIGNUP_REDIRECT_URL = '/account_center/complete_profile/'
# ACCOUNT_SIGNUP_REDIRECT_URL = '/shop/'
# ACCOUNT_LOGIN_REDIRECT_URL = '/shop/'
# SOCIALACCOUNT_AUTO_SIGNUP = False


# payment
PAYPAL_RECEIVER_EMAIL = 'ScubaShop_Paypal_Test@business.example.com'
PAYPAL_TEST = True  # 設為 True 使用沙箱環境，設為 False 使用實際環境

PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = 'sandbox'  # 'live' for production

# 限制登入次數
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
# ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# verification email
PASSWORD_RESET_TIMEOUT_HOURS = 24
EMAIL_VERIFICATION_TIMEOUT_HOURS = 24

# log
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/scubashop/django-error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
