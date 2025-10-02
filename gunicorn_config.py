"""
Конфигурация Gunicorn для Engineering Site
"""
import multiprocessing
import os

# Получаем путь к проекту
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Адрес и порт для прослушивания
bind = "127.0.0.1:8000"

# Количество рабочих процессов
# Рекомендуется: (2 x количество ядер) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Тип воркеров
worker_class = "sync"

# Максимальное количество одновременных подключений
worker_connections = 1000

# Таймаут для запросов (в секундах)
timeout = 30

# Keepalive соединения
keepalive = 2

# Максимальное количество запросов до перезапуска воркера
max_requests = 1000
max_requests_jitter = 100

# Предзагрузка приложения (экономит память)
preload_app = True

# Пути к лог-файлам
accesslog = os.path.join(BASE_DIR, "logs", "gunicorn_access.log")
errorlog = os.path.join(BASE_DIR, "logs", "gunicorn_error.log")

# Уровень логирования
loglevel = "info"

# Формат логов доступа
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Пользователь и группа (опционально)
# user = "django"
# group = "www-data"

# Настройки для продакшена
daemon = False  # systemd сам управляет демонизацией
pidfile = os.path.join(BASE_DIR, "gunicorn.pid")

# Настройки SSL (если нужно, но обычно используется Nginx)
# keyfile = None
# certfile = None

