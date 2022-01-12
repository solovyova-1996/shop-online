"""
Django settings for shoponline project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-alt!ol*b#g9!ai%7cg5(@&z75s4a1$2j#_!^jrcdvkq0qg0kkw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth',
                  'django.contrib.contenttypes', 'django.contrib.sessions',
                  'django.contrib.messages', 'django.contrib.staticfiles',
                  'mainapp', 'users', 'basket', 'admins', 'ordersapp', 'social_django', ]

MIDDLEWARE = ['django.middleware.security.SecurityMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware',
              'social_django.middleware.SocialAuthExceptionMiddleware',
              ]

ROOT_URLCONF = 'shoponline.urls'

TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {

        'context_processors': ['django.template.context_processors.debug',
                               'django.template.context_processors.request',
                               'django.contrib.auth.context_processors.auth',
                               'django.contrib.messages.context_processors.messages',
'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                               ], }, }, ]

WSGI_APPLICATION = 'shoponline.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': BASE_DIR / 'db.sqlite3', }}
# str(BASE_DIR / 'db.sqlite3'),

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', }, ]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR / 'static',)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'users.User'
# Для перенаправления незалогиненых пользвателей на страницу входа
LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/'
# DOMAIN_NAME = 'http:/localhost:8000'
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_SSL = True
# # отправка файла
# EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# EMAIL_FILE_PATH = 'tmp/emails'

# EMAIL_HOST_USER, EMAIL_HOST_PASSWORD = None, None
# команда для запуска
# python -m smtpd -n -c DebuggingServer localhost:25
# отправка yandex почты
DOMAIN_NAME = 'http:/localhost:8000'
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
# ID	8046914
# защищеггый ключ для вк 4STl9WQwoYosEC8T6aPw
# сервиснаф ключ 3f02362c3f02362c3f02362c903f78ff6e33f023f02362c5ede36633db89aefde5a19f7
# SOCIAL_AUTH_VK_OAUTH2_KEY = '7976841'
# SOCIAL_AUTH_VK_OAUTH2_SECRET = 'O70D18ptGnNi1VDjMOUs'
# SOCIAL_AUTH_VK_OAUTH2_API_VERSION = '5.131'

SOCIAL_AUTH_VK_OAUTH2_KEY = '8046914'
SOCIAL_AUTH_VK_OAUTH2_SECRET = '4STl9WQwoYosEC8T6aPw'
SOCIAL_AUTH_VK_OAUTH2_API_VERSION = '5.131'
SOCIAL_AUTH_VK_OAUTH2_IGNORE_DEFAULT_SCORE = True
SOCIAL_AUTH_VK_OAUTH2_SCORE = ['email']
AUTHENTICATION_BACKENDS = (
                          'django.contrib.auth.backends.ModelBackend',
                                'social_core.backends.vk.VKOAuth2',
                          )
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.create_user',
    'users.pipelines.save_user_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)