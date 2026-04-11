"""
Продакшен-настройки. Включается через DJANGO_SETTINGS_MODULE=engineering_site.settings_production
и EnvironmentFile=.env в systemd.
"""
import os

from .settings import *  # noqa: F401,F403

# По умолчанию на проде DEBUG выключен (в .env можно задать DEBUG=True для отладки)
DEBUG = os.environ.get("DEBUG", "False").strip().lower() in ("1", "true", "yes")

# PostgreSQL: если в .env задан DB_NAME — используем его, иначе остаётся SQLite из settings.py
if os.environ.get("DB_NAME", "").strip():
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "USER": os.environ.get("DB_USER", "django"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "localhost"),
            "PORT": os.environ.get("DB_PORT", "5432"),
        }
    }

# За nginx / HTTPS
if os.environ.get("SECURE_PROXY_SSL_HEADER", "").strip():
    parts = os.environ["SECURE_PROXY_SSL_HEADER"].split(",")
    if len(parts) == 2:
        SECURE_PROXY_SSL_HEADER = (parts[0].strip(), parts[1].strip())

_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if _csrf:
    CSRF_TRUSTED_ORIGINS = [x.strip() for x in _csrf.split(",") if x.strip()]

# Только если явно в .env — иначе можно сломать Host за нестандартным прокси
if os.environ.get("USE_X_FORWARDED_HOST", "").strip().lower() in ("1", "true", "yes"):
    USE_X_FORWARDED_HOST = True

# Загрузка картинок из админки (по умолчанию Django режет крупные файлы в памяти)
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get("DATA_UPLOAD_MAX_MEMORY_SIZE", str(12 * 1024 * 1024)))
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get("FILE_UPLOAD_MAX_MEMORY_SIZE", str(12 * 1024 * 1024)))
