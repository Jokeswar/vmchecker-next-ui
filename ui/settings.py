import os
from pathlib import Path
from typing import Any

import ldap
from django_auth_ldap.config import LDAPSearch

from ui.util import string_to_bool

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "very-secret-key")

DEBUG = string_to_bool(os.environ.get("DJANGO_DEBUG", "false"))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ui",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ui.urls"

TEMPLATES: Any = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "ui" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ui.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DATABASE_NAME", ".data/db.sqlite"),
        "USER": os.environ.get("DATABASE_USER", ""),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("DATABASE_HOST", ""),
        "PORT": os.environ.get("DATABASE_PORT", ""),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] [{asctime}] [{module}] [P{process:d}] [T{thread:d}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "ui" / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login"

AUTH_LDAP_SERVER_URI = os.getenv("LDAP_SERVER_URI")
AUTH_LDAP_BIND_DN = os.getenv("LDAP_BIND_DN")
AUTH_LDAP_BIND_PASSWORD = os.getenv("LDAP_BIND_PASSWORD")
AUTH_LDAP_USER_SEARCH = LDAPSearch(
    os.getenv("LDAP_USER_TREE"),
    ldap.SCOPE_SUBTREE,
    os.getenv("LDAP_USER_FILTER"),
)

AUTH_LDAP_FIND_GROUP_PERMS = False

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_CACHE_TIMEOUT = 3600

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

if AUTH_LDAP_SERVER_URI and len(AUTH_LDAP_SERVER_URI) > 0:
    AUTHENTICATION_BACKENDS.insert(0, "django_auth_ldap.backend.LDAPBackend")

VMCK_BACKEND_URL = os.environ.get("VMCK_BACKEND_URL", "http://localhost:8000/api/v1/")

PAGINATION_SIZE = 25

DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
