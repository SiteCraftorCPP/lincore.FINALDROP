"""
Конфиг Gunicorn для systemd (engineering_site.service).
Путь к сокету должен совпадать с proxy_pass в nginx (или замените bind на 127.0.0.1:8000).
"""
import multiprocessing
import os

# Каталог проекта (рабочий каталог задаёт systemd)
_chdir = os.path.dirname(os.path.abspath(__file__))
chdir = _chdir

bind = f"unix:{_chdir}/gunicorn.sock"
workers = min(multiprocessing.cpu_count() * 2 + 1, 5)
worker_class = "sync"
timeout = 120
graceful_timeout = 30
keepalive = 5

# Логи в journald (systemd)
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True

# Удобнее для nginx + unix: сокет с доступом группы www-data
umask = 0o007

# DJANGO_SETTINGS_MODULE задаётся в systemd (Environment= / EnvironmentFile).
