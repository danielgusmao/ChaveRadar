from pathlib import Path
import os

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Em producao, o Render fornece SECRET_KEY como variavel de ambiente.
# O valor padrao abaixo existe apenas para desenvolvimento local.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "chaveradar-chave-local-desenvolvimento-trocar-em-producao",
)

DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# O Render informa automaticamente o hostname publico do Web Service.
render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

# Permite adicionar outros hosts depois, por exemplo chaveradar.com.br.
extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
for host in extra_hosts.split(","):
    host = host.strip()
    if host and host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "leads",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ChaveRadar.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ChaveRadar.wsgi.application"
ASGI_APPLICATION = "ChaveRadar.asgi.application"

# Banco:
# - localmente, sem DATABASE_URL: SQLite;
# - no Render, com DATABASE_URL: PostgreSQL do Supabase.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=60,
            ssl_require=True,
        )
    }
    DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
else:
    DATA_DIR = BASE_DIR / "dados"
    DATA_DIR.mkdir(exist_ok=True)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DATA_DIR / "chaveradar.db",
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Bahia"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
