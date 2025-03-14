"""
Django settings for bep_app project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from environ import FileAwareEnv
from dotenv import load_dotenv, find_dotenv
import warnings

env = FileAwareEnv()
load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Absolute upload file directory
# https://docs.djangoproject.com/en/4.2/ref/settings/#media-root
MEDIA_ROOT = '/media'

STATIC_ROOT = BASE_DIR / 'static/'

STATICFILES_DIRS = [
    ('bootstrap', BASE_DIR / "node_modules/bootstrap"),
    ('bootstrap-icons', BASE_DIR / "node_modules/bootstrap-icons"),
    ('@fortawesome', BASE_DIR / "node_modules/@fortawesome"),
    '/static-vite',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-0lgov2k26n+=bjocstuna-@888$&g3(xvxugltqd*xx+z=_p1=')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    'bep.apps.BepConfig',
    'admin_interface',
    'colorfield',
    'tinymce',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'health_check',
    'django_select2',
    'django_cleanup.apps.CleanupConfig',
    'modelclone',
    'django_vite',
    'ninja_extra',
    'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bep_app.urls'

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
                'bep.context_processors.get_git_info',
            ],
        },
    },
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/django_cache',
    }
}
CACHE_SECONDS = 1 if DEBUG else (60 * 15) # 1 second if debugging else 15 minutes

WSGI_APPLICATION = 'bep_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': env('DB_HOST', default=''),
        'NAME': env('DB_NAME', default=''),
        'USER': env('DB_USER', default=''),
        'PASSWORD': env('DB_PASSWORD', default=''),
        'PORT': env.int('DB_PORT', default=5432),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Uploaded files (Images)
# https://docs.djangoproject.com/en/4.2/ref/settings/#media-url
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# default upload permissions
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644

# email host
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env.int('EMAIL_PORT', default=1025)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')

# CSRF form settings
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['http://localhost:8080', 'http://localhost:5173'])

# iframe settings
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

DATA_UPLOAD_MAX_MEMORY_SIZE = 256 * 1024 * 1024 # 256MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 256 * 1024 * 1024 # 256MB

GIT_REPO = "https://github.com/sfu-dhil/bep-django"
GIT_COMMIT = env('GIT_COMMIT', default='')
GIT_COMMIT_SHORT = env('GIT_COMMIT_SHORT', default='')
GIT_BRANCH = env('GIT_BRANCH', default='')
GIT_TAG = env('GIT_TAG', default='')

# logout redirection
LOGIN_URL = 'admin:login'
LOGIN_REDIRECT_URL = 'admin:index'
LOGOUT_REDIRECT_URL = 'admin:login'

DJANGO_VITE = {
    "default": {
        "dev_mode": DEBUG,
        "static_url_prefix": "dist",
    }
}

# admin interface
warnings.filterwarnings("ignore", module="admin_interface.templatetags.admin_interface_tags")

# tinymce settings
TINYMCE_DEFAULT_CONFIG = {
    'height': '250px',
    'branding': False,
    'menubar': False,
    'plugins': 'autolink, code, link, anchor, lists, table, quickbars, wordcount, pagebreak, nonbreaking',
    'toolbar': 'undo redo | numlist bullist | fontsize | alignleft aligncenter alignright | link anchor | hr | removeformat',
    'quickbars_insert_toolbar': False,
    'quickbars_selection_toolbar': 'bold italic underline strikethrough | fontsize | forecolor | blockquote',
    'contextmenu': 'undo redo | inserttable | cell row column deletetable',
}

# django ninja api
NINJA_EXTRA={
    'PAGINATION_CLASS': 'ninja_extra.pagination.PageNumberPaginationExtra'
}
