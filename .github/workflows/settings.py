"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import environ
import os
import sys

# env = environ.Env()
# environ.Env.read_env()

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent

# BASE_DIR 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수 로드
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

OPENAI_API_KEY = env("OPENAI_API_KEY", default="")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# 장고 시크릿 키가 설정되어 있는 부분
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# 디버그 모드 설정
DEBUG = env.bool("DEBUG", default=True)
# DEBUG = True

# ALLOWED_HOSTS = ['onrecord.kr', 'www.onrecord.kr', '223.130.132.219', '127.0.0.1', 'localhost']
# ALLOWED_HOSTS를 .env에서 가져오기
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'diaries',
    'replies',
    'communities',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount', # 소셜 로그인 사용 시 필요
    'allauth.socialaccount.providers.naver', # 네이버
    'allauth.socialaccount.providers.kakao', # 카카오
    'allauth.socialaccount.providers.google', # 구글
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # allauth 미들웨어 추가
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # templates 폴더 경로 설정
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DB 설정 부분
DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE", default="django.db.backends.postgresql"),
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
         # 빈 문자열("") 대신 PostgreSQL의 기본 포트 5432를 사용
        'PORT': env.int("DB_PORT", default=5432),
    }
}

if 'test' in sys.argv:
        DATABASES['default'] = {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:', # 메모리 DB 사용
        }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# static 파일 설정
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
        '/root/On-Record/static'
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Media 파일 설정
MEDIA_URL = '/media/' # 각 모델의 ImageField에 업로드된 파일의 URL 고정 값
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # 실제 파일이 저장되는 경로

# 인증 백엔드 설정(기본 Django 인증 방식 + allauth 인증 방식)
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# from decouple import config

SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'APP': {
            'client_id': env('NAVER_CLIENT_ID'),
            'secret': env('NAVER_SECRET'),
        },
    },
    'kakao': {
        'APP': {
            'client_id': env('KAKAO_CLIENT_ID'),
            'secret': env('KAKAO_SECRET'),
        },
        'SCOPE': [
            'account_email',
            'profile_nickname',
        ],
    },
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),
            'secret': env('GOOGLE_SECRET'),
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
    },
}

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True # 이메일 필수 입력
ACCOUNT_EMAIL_VERIFICATION = 'optional' # 회원가입 시 이메일 인증을 하도록 설정
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  # 이메일 확인 링크 클릭 시 자동 인증(SMTP 서버 설정 필요)
ACCOUNT_AUTHENTICATION_METHOD = 'email' # 이메일을 아이디처럼 사용
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # username 필드를 사용하지 않도록 설정
ACCOUNT_USERNAME_REQUIRED = False

LOGIN_REDIRECT_URL = '/' # 로그인 후 연결될 URL

ACCOUNT_ADAPTER = 'users.adapters.MyAccountAdapter'

SOCIALACCOUNT_QUERY_EMAIL = True # 소셜 로그인 시 이메일 정보를 가져오도록 설정
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_ADAPTER = 'users.adapters.CustomSocialAccountAdapter'

ACCOUNT_LOGOUT_REDIRECT_URL = '/' # 로그아웃 후 연결될 URL
ACCOUNT_LOGOUT_ON_GET = True # 로그아웃 요청 시 즉시 로그아웃
SOCIALACCOUNT_LOGIN_ON_GET = True # 소셜 로그인 요청 시 즉시 로그인

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CSRF_TRUSTED_ORIGINS = [
    'https://onrecord.kr',
    'http://onrecord.kr',
    'https://www.onrecord.kr',
    'http://www.onrecord.kr',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
