"""
Django settings for xfz_platform project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7frz$)_$4ano=8h66bl*9irkz*)xvdax)!o2jv8bzf%b5wneti'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'www.qianvipfei.club']

INTERNAL_IPS = ['127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'rest_framework',
    # 设置搜索引擎
    'haystack',

    'apps.cms.apps.CmsConfig',
    'apps.news.apps.NewsConfig',
    'apps.xfzauth.apps.XfzauthConfig',
    'apps.course.apps.CourseConfig',
    'apps.payinfo.apps.PayinfoConfig' ,
    'apps.ueditor.apps.UeditorConfig',
    # 'apps.search.apps.SearchConfig',
    'apps.testApi'
]


# 搜索引擎配置
HAYSTACK_CONNECTIONS = {
    'default': {
        # 设置haystack的搜索引擎
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        # 设置索引文件的位置
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    }
}


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEBUG_TOOLBAR_PANELS = [
    # 'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    # 'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 缓存
    'debug_toolbar.panels.templates.TemplatesPanel',
    # 信号
    # 'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'JQUERY_URL': ''
}




ROOT_URLCONF = 'xfz_platform.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'front/templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.templatetags.static',
            ]
        },
    },
]

WSGI_APPLICATION = 'xfz_platform.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xfz_platform',
        'HOST': '127.0.0.1',
        # 'HOST': '129.28.158.195',
        # 'PORT': 3306,
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': '123456'
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

AUTH_USER_MODEL = 'xfzauth.User'


LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# 静态文件
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'front/dist')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Qiniu配置
QINIU_ACCESS_KEY = 'd9W4xj9mndRr3ovMFBuzvHGhc13XjVdi2GzT8XsU'
QINIU_SECRET_KEY = 'eRf9a2qSfHd_4R8QHCh32AJr4szxu-pGC84KtH77'
QINIU_BUCKET_NAME = 'xfz_platfrom'
QINIU_DOMAIN = 'http://ps9lpfh8q.bkt.clouddn.com/'

# 七牛和自己的服务器，最少要配置一个
# UEditor配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN
#
#
UEDITOR_UPLOAD_TO_SERVER = False
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR,'front','dist','ueditor','config.json')


# 前台每页新闻显示的数量
ONE_PAGE_NEWS_COUNT = 2

# 前台每页新闻显示的数量
CMS_ONE_PAGE_NEWS_COUNT = 2


# 百度云的配置
# 控制台->用户中心->用户ID
BAIDU_CLOUD_USER_ID = 'dc687df49e3f4415abac79f56caca7f1'
# 点播VOD->全局设置->发布设置->安全设置->UserKey
BAIDU_CLOUD_USER_KEY = '55a4232774274403'

