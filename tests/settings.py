import json
import os

from . import utils

test_db_vendor = os.environ.get("DJPADDLE_TEST_DB_VENDOR", "sqlite")
test_db_name = os.environ.get("DJPADDLE_TEST_DB_NAME", "djpaddle")
test_db_user = os.environ.get("DJPADDLE_TEST_DB_USER", test_db_vendor)
test_db_pass = os.environ.get("DJPADDLE_TEST_DB_PASS", "")
test_db_host = os.environ.get("DJPADDLE_TEST_DB_HOST", "localhost")
test_db_port = os.environ.get("DJPADDLE_TEST_DB_PORT", "")

DEBUG = True
SECRET_KEY = os.environ.get("DJPADDLE_TEST_DJANGO_SECRET_KEY", "djpaddle")
SITE_ID = 1
TIME_ZONE = "UTC"
USE_TZ = True
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

ALLOWED_HOSTS = json.loads(os.environ.get("DJPADDLE_TEST_ALLOWED_HOSTS_JSON", "[]"))

if test_db_vendor == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": test_db_name,
            "USER": test_db_user,
            "PASSWORD": test_db_pass,
            "HOST": test_db_host,
            "PORT": test_db_port,
        }
    }
elif test_db_vendor == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": test_db_name,
            "USER": test_db_user,
            "PASSWORD": test_db_pass,
            "HOST": test_db_host,
            "PORT": test_db_port,
        }
    }
elif test_db_vendor == "sqlite":
    # sqlite is not officially supported, but useful for quick testing.
    # may be dropped if we can't maintain compatibility.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            # use a on-disk db for test so --reuse-db can be used
            "TEST": {"NAME": os.path.join(BASE_DIR, "test_db.sqlite3")},
        }
    }
else:
    raise NotImplementedError("DJPADDLE_TEST_DB_VENDOR = {}".format(test_db_vendor))


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = "tests.urls"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "djpaddle",
    "tests",
]

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

STATIC_URL = "/static/"

DJPADDLE_VENDOR_ID = "test-vendor-id"
DJPADDLE_KEY = utils.generate_private_key()
DJPADDLE_PUBLIC_KEY = utils.export_pubkey_as_pem(DJPADDLE_KEY)
DJPADDLE_API_KEY = "test-api-key"
