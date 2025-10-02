# 🏢 Engineering Site - Сайт инженерно-сервисной компании

[![Deploy Status](https://img.shields.io/badge/Deploy-Ready-brightgreen)](https://лин-кор.рф)
[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-3.2.25-green)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-blue)](https://postgresql.org)
[![SSL](https://img.shields.io/badge/SSL-Let's%20Encrypt-orange)](https://letsencrypt.org)

> **🎯 Все проблемы с деплоем решены! Проект готов к production!**

Корпоративный сайт инженерно-сервисной компании на Django с полной автоматизацией деплоя на VPS.

**🌐 Домен:** [лин-кор.рф](https://лин-кор.рф) (5.129.251.41)

---

## ✅ Решенные проблемы

- **🗄️ База данных:** Настроена полная поддержка PostgreSQL вместо SQLite
- **🚀 Gunicorn:** Создана корректная конфигурация и systemd сервис
- **🔒 HTTPS/SSL:** Автоматическая установка Let's Encrypt сертификата
- **🌍 Домен:** Поддержка кириллического домена лин-кор.рф
- **📸 Медиа:** Исправлено отображение фотографий и данных из БД

---

## 🚀 Быстрый старт

### 1️⃣ Начните отсюда
```
📖 Откройте файл: НАЧАТЬ_ОТСЮДА.txt
```

### 2️⃣ Выберите руководство
- **Новичок?** → `DEPLOY_GUIDE_FULL.md` (подробно)
- **Опытный?** → `QUICK_DEPLOY.md` (только команды)
- **Контроль** → `DEPLOY_CHECKLIST.txt` (чеклист)

### 3️⃣ Автоматический деплой
```bash
# На сервере (один раз)
bash setup_server.sh      # Настройка VPS
bash deploy.sh            # Деплой приложения  
bash setup_ssl.sh         # Установка SSL
```

---

## 📦 Что включено

### 🔧 Скрипты автоматизации
- `setup_server.sh` - первичная настройка VPS
- `deploy.sh` - автоматический деплой Django
- `setup_ssl.sh` - установка SSL сертификата
- `migrate_to_postgresql.sh` - перенос данных из SQLite

### ⚙️ Конфигурационные файлы
- `gunicorn_config.py` - настройки WSGI сервера
- `nginx_config.conf` - конфигурация веб-сервера
- `engineering_site.service` - systemd сервис
- `env_production_example.txt` - пример .env файла

### 📚 Документация
- `✅_ВСЕ_ГОТОВО.txt` - статус проекта
- `НАЧАТЬ_ОТСЮДА.txt` - главная инструкция
- `DEPLOY_GUIDE_FULL.md` - полное руководство
- `QUICK_DEPLOY.md` - быстрый деплой
- `DEPLOY_CHECKLIST.txt` - чеклист проверки

---

## 🏗️ Архитектура

```
Production Stack:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Nginx       │────│    Gunicorn     │────│     Django      │
│   (Web Server)  │    │  (WSGI Server)  │    │   (Framework)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐    ┌─────────────────┐
         └──────────────│  Static Files   │    │   PostgreSQL    │
                        │   (WhiteNoise)  │    │   (Database)    │
                        └─────────────────┘    └─────────────────┘
```

---

## 🎯 Возможности сайта

- 🏠 **Главная страница** с информацией о компании
- 📋 **9 страниц услуг** (отопление, вентиляция, монтаж и др.)
- 📸 **Управление фотографиями** через админ-панель
- 📝 **Система заявок** от клиентов
- 🎯 **Приглашения в тендеры**
- 📱 **Адаптивный дизайн**
- 🔐 **Защищенная админ-панель**

---

## 🛠️ Технологии

| Компонент | Технология | Версия |
|-----------|------------|--------|
| **Framework** | Django | 3.2.25 |
| **Language** | Python | 3.8+ |
| **Database** | PostgreSQL | Latest |
| **Web Server** | Nginx | Latest |
| **WSGI Server** | Gunicorn | 21.2.0 |
| **SSL** | Let's Encrypt | Auto |
| **Static Files** | WhiteNoise | 6.5.0 |

---

## 📋 Требования

### Локальная разработка
- Python 3.8+
- pip
- virtualenv

### Production (VPS)
- Ubuntu 20.04/22.04
- 1GB RAM минимум
- 20GB SSD
- Доступ root

---

## 🚀 Деплой на VPS

### Супер-быстрая версия
```bash
# 1. На локальной машине
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 2. На сервере (root)
bash setup_server.sh

# 3. На сервере (django пользователь)
bash deploy.sh

# 4. На сервере (root)
# Настройка systemd и Nginx (команды в НАЧАТЬ_ОТСЮДА.txt)
bash setup_ssl.sh
```

### Подробная инструкция
👉 **Смотрите файлы документации в репозитории!**

---

## 📊 Статистика проекта

- **📁 Файлов:** 100+
- **📝 Строк кода:** 3000+
- **🆕 Новых файлов:** 17
- **📚 Документации:** 7 файлов
- **🔧 Скриптов:** 4 автоматизированных

---

## 🔒 Безопасность

- ✅ HTTPS/SSL сертификат (Let's Encrypt)
- ✅ Файрвол (UFW) 
- ✅ Fail2Ban защита от брутфорса
- ✅ Автоматические обновления безопасности
- ✅ Отключение root доступа по SSH
- ✅ Безопасные настройки Django

---

## 📈 Мониторинг

### Логи
```bash
# Gunicorn
tail -f ~/projects/engineering_site/logs/gunicorn_error.log

# Nginx  
sudo tail -f /var/log/nginx/engineering_site_error.log

# systemd
sudo journalctl -u engineering_site -f
```

### Статус сервисов
```bash
sudo systemctl status engineering_site nginx postgresql
```

---

## 🔄 Обновление проекта

```bash
cd ~/projects/engineering_site
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart engineering_site
```

---

## 📞 Поддержка

### При проблемах:
1. 📖 Откройте `DEPLOY_GUIDE_FULL.md` → раздел "Решение проблем"
2. 📋 Используйте `DEPLOY_CHECKLIST.txt` для проверки
3. 🔍 Проверьте логи (команды выше)

### Типичные проблемы:
- **502 Bad Gateway** → Проверьте Gunicorn
- **Статика не загружается** → `collectstatic` + права доступа
- **Фото не отображаются** → Права на папку media
- **SSL не работает** → Проверьте DNS домена

---

## 📄 Лицензия

Проект разработан для инженерно-сервисной компании.

---

## 🎉 Результат

После деплоя:
- ✅ **Сайт:** https://лин-кор.рф
- ✅ **Админка:** https://лин-кор.рф/admin/
- ✅ **SSL сертификат** (зеленый замочек 🔒)
- ✅ **Все фото отображаются**
- ✅ **PostgreSQL** для надежного хранения
- ✅ **Автозапуск** при перезагрузке сервера

---

## 🚀 Начать деплой

```bash
git clone https://github.com/Beiseek/lincore.rfFINAL.git
cd lincore.rfFINAL
```

**👉 Откройте файл `НАЧАТЬ_ОТСЮДА.txt` и следуйте инструкциям!**

---

<div align="center">

**🎯 Все готово для production деплоя! 🎯**

[🌐 Сайт](https://лин-кор.рф) • [📚 Документация](./НАЧАТЬ_ОТСЮДА.txt) • [🚀 Быстрый старт](./QUICK_DEPLOY.md)

</div>
