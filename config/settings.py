"""Project-wide Django settings for the Daymark learning application."""

import os
from pathlib import Path

# BASE_DIR is the project root; build portable paths from it.
BASE_DIR = Path(__file__).resolve().parent.parent

# This fallback key is only for local learning. Set DJANGO_SECRET_KEY outside source control.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-local-learning-key-change-before-deployment',
)

# Debug pages are useful locally and unsafe for public deployment.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').strip().lower() in {'1', 'true', 'yes', 'on'}

# Comma-separated hosts come from the environment; these defaults support local runserver use.
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost'
    ).split(',')
    if host.strip()
]

# Django's built-in apps provide admin, authentication, sessions, messages, and static handling.
# AppConfig paths register the three feature apps inside the apps Python package.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts.apps.AccountsConfig',
    'apps.projects.apps.ProjectsConfig',
    'apps.tasks.apps.TasksConfig',
]

# Middleware wraps request/response processing. Order matters: requests travel top-down,
# and responses return bottom-up. The timing middleware is a small local teaching example.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'config.middleware.RequestTimingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT_URLCONF points Django at the website's top-level URL map.
ROOT_URLCONF = 'config.urls'

# DIRS contains shared templates; APP_DIRS also discovers templates within installed apps.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# SQLite is a portable file database included with Python; it is appropriate for this tutorial.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Built-in validators reject common and weak passwords in Django authentication forms.
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# STATIC_URL is the browser URL prefix; STATICFILES_DIRS lists our source assets.
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Named destinations used by Django's authentication decorators and views.
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'projects:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Console email keeps development email output in the terminal.
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}
