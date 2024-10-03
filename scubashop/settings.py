import os
from pathlib import Path
from dotenv import load_dotenv

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
# 加載 .env 文件中的環境變量
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 獲取環境變量
DJANGO_ENV = os.getenv('DJANGO_ENV', 'local')

# 通用設置
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = DJANGO_ENV == 'local'

ALLOWED_HOSTS = ['*'] if DEBUG else ['ec2-100-27-173-161.compute-1.amazonaws.com', 'penguindiving.com']
SITE_ID = 1

# CSRF_TRUSTED_ORIGINS = [
#     'https://767f-180-177-8-38.ngrok-free.app'
# ]

# aws boto3 sns service
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# 靜態文件和媒體文件配置
if DJANGO_ENV == 'local':
    # 本地開發環境配置
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # 部署環境配置
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # 在使用 S3 存儲媒體文件時，通常不需要設置 MEDIA_ROOT
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# 應用和中間件設置
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
    'api',
    # oauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'storages',
]

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django 的默認認證後台
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth 的認證後台
]

ROOT_URLCONF = 'scubashop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

# REST_FRAMEWORK = {
#     'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
# }

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

WSGI_APPLICATION = 'scubashop.wsgi.application'

# 數據庫配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 密碼驗證
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

# 國際化
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

TIME_ZONE = 'Asia/Taipei'
LANGUAGE_CODE = 'zh-hant'
USE_I18N = True
USE_TZ = True

# 默認的主鍵字段類型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

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

# msg tag
from django.contrib.messages import constants as message_constants
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

# settings.py
# APPEND_SLASH = False
CART_SESSION_ID = 'cart'  # 定義購物車在 session 中的鍵名

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/account_center/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'