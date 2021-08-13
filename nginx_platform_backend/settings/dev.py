"""
Django settings for nginx_platform_backend project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import sys

sys.path.insert(0, BASE_DIR)
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(1, APPS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nb9y@ir9$v*7@o^agni6ly8*c6)xi7o(ter@h$*#fe5(%h5l9)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'user',
    'nginx',
    'monitor',
# WebSocket
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nginx_platform_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(BASE_DIR), 'templates')]
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

WSGI_APPLICATION = 'nginx_platform_backend.wsgi.application'
import psutil
PROJECT_START_TIME = psutil.Process().create_time()
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

password = os.environ.get('password', 'Admin@123')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nginx_consul',
        'USER': 'nginx',
        'PASSWORD': password,
        'HOST': '1.116.65.90',
        'PORT': 20036
    }
}
import pymysql

pymysql.install_as_MySQLdb()

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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# 扩展user表
# AUTH_USER_MODEL = 'user.user'
AUTH_USER_MODEL = 'user.UserProfile'

# 真实项目上线后，日志文件打印级别不能过低，因为一次日志记录就是一次文件io操作
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            # 实际开发建议使用WARNING
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            # 实际开发建议使用ERROR
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小luffyapi
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", "ops.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 10,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# 支持跨域请求
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'authorization',
    'content-type',
)

# JWT 过期时间
import datetime

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),  # Token刷新有效时间
    'JWT_ALLOW_REFRESH': True,  # 允许刷新Token
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',  # 定义Token携带头信息, Authorization: Bearer ...
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.0.0.80:6379",
        "LOCATION": "redis://127.0.0.0.1:6379",
        # "LOCATION": "redis://1.116.65.90:20039",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "SOCKET_CONNECT_TIMEOUT": 5,
            # "PASSWORD": "123",
        }
    },
    'user_info': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://127.0.0.1:6379/2",
        # 'LOCATION': "redis://10.0.0.80:6379/2",

        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

# channels配置(配置ASGI, 用于实现WebSocket)
ASGI_APPLICATION = 'nginx_platform_backend.routing.application'

# django-channels配置
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': "channels_redis.core.RedisChannelLayer",
        'CONFIG': {
            'hosts': [f'redis://127.0.0.1:6379/4'],
            'symmetric_encryption_keys': [SECRET_KEY],
            'capacity': 1500,
            'expiry': 10
        },
    },
}
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'nginx_platform_backend.utils.exceptions.common_exception_handler',
    # 'DEFAULT_THROTTLE_RATES': {
    #     'mobile_throttle': '1/min'
    # }
}

REST_FRAMEWORK = {
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':
        (
            'rest_framework.permissions.IsAuthenticated',  # 登录验证
            'nginx_platform_backend.utils.permissions.RbacPermission',  # 自定义权限认证
        ),
    'EXCEPTION_HANDLER': 'nginx_platform_backend.utils.exceptions.exception_handler',
    # 分页
    # 'DEFAULT_PAGINATION_CLASS': 'libs.drf.myPagePagination.MyPagePagination',
    # # exception
    # 'EXCEPTION_HANDLER': 'libs.drf.my_rest_exception.custom_exception_handler',
    # # 文档
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}

BASE_API = 'api/'  # 项目BASE API, 如设置时必须以/结尾
WHITE_LIST = [f'/{BASE_API}system/user/login/', f'/{BASE_API}system/user/logout/',f'/{BASE_API}system/user/info/']  # 权限认证白名单
# WHITE_LIST = [f'/{BASE_API}system/user/login/', f'/{BASE_API}system/user/info/', f'/{BASE_API}swagger/.*']  # 权限认证白名单
REGEX_URL = '^{url}$'  # 权限匹配时,严格正则url
# PROJECT_START_TIME = psutil.Process().create_time()
### 用户自定义配置
from .user_settings import *
