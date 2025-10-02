# 🚀 Полное руководство по деплою Engineering Site

## Содержание
1. [Подготовка проекта локально](#1-подготовка-проекта-локально)
2. [Настройка VPS сервера](#2-настройка-vps-сервера)
3. [Загрузка проекта на сервер](#3-загрузка-проекта-на-сервер)
4. [Деплой приложения](#4-деплой-приложения)
5. [Настройка systemd и Nginx](#5-настройка-systemd-и-nginx)
6. [Установка SSL сертификата](#6-установка-ssl-сертификата)
7. [Перенос данных из SQLite](#7-перенос-данных-из-sqlite)
8. [Проверка работоспособности](#8-проверка-работоспособности)
9. [Решение проблем](#9-решение-проблем)

---

## Информация о домене

- **Кириллический домен:** лин-кор.рф
- **Punycode (ASCII):** xn----otbhblio.xn--p1ai
- **IP адрес сервера:** 5.129.251.41

---

## 1. Подготовка проекта локально

### 1.1. Генерация SECRET_KEY

Откройте PowerShell и выполните:

```powershell
cd "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21"
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Сохраните полученный ключ!** Он понадобится для .env файла.

### 1.2. Создание архива проекта

```powershell
# Создайте zip архив всего проекта
Compress-Archive -Path .\* -DestinationPath .\engineering_site_deploy.zip -Update
```

Или вручную:
1. Откройте проводник
2. Перейдите в `C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21`
3. Выделите все файлы (кроме venv, если есть)
4. ПКМ → Отправить → Сжатая ZIP-папка
5. Назовите: `engineering_site_deploy.zip`

---

## 2. Настройка VPS сервера

### 2.1. Подключение к серверу

Откройте PowerShell или используйте PuTTY:

```powershell
ssh root@5.129.251.41
```

Введите пароль root пользователя.

### 2.2. Автоматическая настройка сервера

Выполните следующие команды на сервере:

```bash
# Создайте временную директорию
mkdir -p /tmp/deploy
cd /tmp/deploy

# Загрузите скрипт настройки
# (Скрипт setup_server.sh должен быть загружен на сервер)
```

С вашего компьютера загрузите скрипт:

```powershell
scp "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\setup_server.sh" root@5.129.251.41:/tmp/deploy/
```

Затем на сервере:

```bash
cd /tmp/deploy
chmod +x setup_server.sh
bash setup_server.sh
```

Этот скрипт автоматически:
- ✅ Обновит систему
- ✅ Установит Python, PostgreSQL, Nginx
- ✅ Создаст пользователя django
- ✅ Настроит базу данных PostgreSQL
- ✅ Настроит файрвол
- ✅ Установит систему безопасности

**ВАЖНО:** Сохраните данные подключения к PostgreSQL из вывода скрипта!

---

## 3. Загрузка проекта на сервер

### 3.1. Создание SSH ключа (опционально, но рекомендуется)

На вашем компьютере:

```powershell
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

Скопируйте публичный ключ на сервер:

```powershell
type $env:USERPROFILE\.ssh\id_rsa.pub | ssh django@5.129.251.41 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 3.2. Загрузка архива проекта

```powershell
scp "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\engineering_site_deploy.zip" django@5.129.251.41:~/
```

### 3.3. Распаковка на сервере

Подключитесь как пользователь django:

```bash
ssh django@5.129.251.41
```

Распакуйте проект:

```bash
cd ~
mkdir -p projects
cd projects
unzip ~/engineering_site_deploy.zip -d engineering_site
cd engineering_site
```

---

## 4. Деплой приложения

### 4.1. Создание .env файла

На сервере создайте файл `.env`:

```bash
cd ~/projects/engineering_site
nano .env
```

Вставьте следующее содержимое (замените значения):

```env
# SECRET_KEY - ключ, который вы сгенерировали на шаге 1.1
SECRET_KEY=ваш-сгенерированный-секретный-ключ

# DEBUG - ВСЕГДА False для продакшена
DEBUG=False

# ALLOWED_HOSTS - все домены и IP через запятую
ALLOWED_HOSTS=xn----otbhblio.xn--p1ai,лин-кор.рф,www.xn----otbhblio.xn--p1ai,5.129.251.41

# DATABASE_URL - строка подключения из /root/db_credentials.txt
DATABASE_URL=postgresql://django_user:ваш_пароль@localhost:5432/engineering_site_db

# SECURE_SSL_REDIRECT - False до установки SSL, затем True
SECURE_SSL_REDIRECT=False
```

Сохраните файл: `Ctrl+X`, затем `Y`, затем `Enter`.

### 4.2. Запуск скрипта деплоя

```bash
cd ~/projects/engineering_site
bash deploy.sh
```

Скрипт автоматически:
- ✅ Создаст виртуальное окружение
- ✅ Установит все зависимости
- ✅ Применит миграции к PostgreSQL
- ✅ Соберет статические файлы
- ✅ Настроит права доступа

### 4.3. Создание суперпользователя

```bash
cd ~/projects/engineering_site
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production
python manage.py createsuperuser
```

Введите:
- Username: admin (или любое другое имя)
- Email: ваш email
- Password: надежный пароль (не менее 8 символов)

---

## 5. Настройка systemd и Nginx

### 5.1. Установка systemd сервиса

Выйдите из пользователя django и подключитесь как root:

```bash
exit  # Выход из django пользователя
ssh root@5.129.251.41
```

Установите сервис:

```bash
cp /home/django/projects/engineering_site/engineering_site.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable engineering_site
systemctl start engineering_site
```

Проверьте статус:

```bash
systemctl status engineering_site
```

Вы должны увидеть: `Active: active (running)` 

Если есть ошибки, смотрите логи:

```bash
journalctl -u engineering_site -n 50
```

### 5.2. Настройка Nginx

```bash
cp /home/django/projects/engineering_site/nginx_config.conf /etc/nginx/sites-available/engineering_site
ln -s /etc/nginx/sites-available/engineering_site /etc/nginx/sites-enabled/
```

Проверьте конфигурацию:

```bash
nginx -t
```

Если всё OK, перезапустите Nginx:

```bash
systemctl restart nginx
```

### 5.3. Проверка работы

Откройте браузер и перейдите:
- http://5.129.251.41
- http://лин-кор.рф (если DNS уже настроен)

Вы должны увидеть сайт!

---

## 6. Установка SSL сертификата

### 6.1. Проверка DNS

Убедитесь, что домен направлен на сервер:

```bash
ping лин-кор.рф
# Должен показать IP: 5.129.251.41
```

На вашем компьютере в PowerShell:

```powershell
ping лин-кор.рф
```

Должен показать IP `5.129.251.41`.

### 6.2. Установка SSL

На сервере (под root):

```bash
cd /home/django/projects/engineering_site
bash setup_ssl.sh
```

Скрипт автоматически:
- ✅ Установит Certbot
- ✅ Получит SSL сертификат от Let's Encrypt
- ✅ Настроит автоматическое обновление
- ✅ Перенаправит HTTP на HTTPS

### 6.3. Обновление настроек

После успешной установки SSL, обновите `.env`:

```bash
su - django
cd ~/projects/engineering_site
nano .env
```

Измените:
```env
SECURE_SSL_REDIRECT=True
```

Сохраните и перезапустите сервис:

```bash
exit  # Выход из django
sudo systemctl restart engineering_site
```

### 6.4. Проверка HTTPS

Откройте браузер:
- https://лин-кор.рф ✅
- https://xn----otbhblio.xn--p1ai ✅

Должен появиться зеленый замочек 🔒

---

## 7. Перенос данных из SQLite

Если у вас есть данные в локальной базе SQLite, перенесите их:

### 7.1. Загрузка базы данных на сервер

С вашего компьютера:

```powershell
scp "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\db.sqlite3" django@5.129.251.41:~/projects/engineering_site/
```

### 7.2. Загрузка папки media

```powershell
scp -r "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\media\*" django@5.129.251.41:~/projects/engineering_site/media/
```

### 7.3. Запуск миграции

На сервере:

```bash
su - django
cd ~/projects/engineering_site
bash migrate_to_postgresql.sh
```

Скрипт автоматически:
- ✅ Создаст резервную копию SQLite
- ✅ Экспортирует все данные
- ✅ Импортирует их в PostgreSQL

### 7.4. Проверка медиа-файлов

```bash
ls -la ~/projects/engineering_site/media/
sudo chmod -R 755 ~/projects/engineering_site/media/
sudo chown -R django:www-data ~/projects/engineering_site/media/
```

---

## 8. Проверка работоспособности

### 8.1. Проверка сервисов

```bash
# Проверка Gunicorn
sudo systemctl status engineering_site

# Проверка Nginx
sudo systemctl status nginx

# Проверка PostgreSQL
sudo systemctl status postgresql
```

### 8.2. Проверка логов

```bash
# Логи Gunicorn
tail -f /home/django/projects/engineering_site/logs/gunicorn_error.log

# Логи Nginx
sudo tail -f /var/log/nginx/engineering_site_error.log

# Логи systemd
sudo journalctl -u engineering_site -f
```

### 8.3. Проверка админки

Откройте браузер:
- https://лин-кор.рф/admin/

Войдите с учетными данными суперпользователя.

Проверьте:
- ✅ Фото отображаются
- ✅ Можно загружать новые фото
- ✅ Все данные на месте

### 8.4. Проверка сайта

Откройте:
- https://лин-кор.рф/

Проверьте:
- ✅ Главная страница загружается
- ✅ Все фото отображаются
- ✅ Номер телефона отображается
- ✅ Галерея работает
- ✅ Все страницы доступны

---

## 9. Решение проблем

### Проблема: 502 Bad Gateway

**Причина:** Gunicorn не запущен или не может подключиться к PostgreSQL.

**Решение:**

```bash
# Проверьте статус
sudo systemctl status engineering_site

# Проверьте логи
sudo journalctl -u engineering_site -n 100

# Проверьте .env файл
su - django
cd ~/projects/engineering_site
cat .env

# Проверьте подключение к БД
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production
python manage.py check --database default
```

### Проблема: Статические файлы не загружаются

**Решение:**

```bash
su - django
cd ~/projects/engineering_site
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production
python manage.py collectstatic --noinput
sudo chmod -R 755 staticfiles
sudo systemctl restart nginx
```

### Проблема: Медиа-файлы (фото) не отображаются

**Решение:**

```bash
su - django
cd ~/projects/engineering_site
sudo chmod -R 755 media
sudo chown -R django:www-data media
ls -la media/  # Проверьте наличие файлов
```

Также проверьте конфигурацию Nginx:

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Проблема: SSL сертификат не устанавливается

**Причина:** DNS не настроен или порт 80 закрыт.

**Решение:**

```bash
# Проверьте DNS
ping лин-кор.рф

# Проверьте файрвол
sudo ufw status

# Проверьте, что Nginx слушает порт 80
sudo netstat -tulpn | grep :80

# Попробуйте вручную
sudo certbot --nginx -d xn----otbhblio.xn--p1ai -d www.xn----otbhblio.xn--p1ai
```

### Проблема: Ошибка "ALLOWED_HOSTS"

**Причина:** Неправильно настроен .env файл.

**Решение:**

```bash
su - django
cd ~/projects/engineering_site
nano .env
```

Убедитесь что есть:
```env
ALLOWED_HOSTS=xn----otbhblio.xn--p1ai,лин-кор.рф,www.xn----otbhblio.xn--p1ai,5.129.251.41
```

Затем:
```bash
exit  # Выход из django
sudo systemctl restart engineering_site
```

---

## 10. Полезные команды

### Управление сервисами

```bash
# Перезапуск всех сервисов
sudo systemctl restart engineering_site nginx postgresql

# Остановка
sudo systemctl stop engineering_site

# Запуск
sudo systemctl start engineering_site

# Проверка статуса
sudo systemctl status engineering_site nginx postgresql
```

### Обновление проекта

```bash
su - django
cd ~/projects/engineering_site
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production

# Обновление кода (если через git)
git pull

# Обновление зависимостей
pip install -r requirements.txt

# Применение новых миграций
python manage.py migrate

# Сбор статики
python manage.py collectstatic --noinput

# Перезапуск
exit
sudo systemctl restart engineering_site
```

### Резервное копирование

```bash
# Создание бэкапа БД
su - django
cd ~/projects/engineering_site
pg_dump engineering_site_db > backup_$(date +%Y%m%d).sql

# Создание бэкапа медиа
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

---

## 11. Контрольный чеклист

Перед завершением убедитесь:

- [ ] VPS сервер настроен (setup_server.sh выполнен)
- [ ] PostgreSQL создан и настроен
- [ ] Проект загружен на сервер
- [ ] .env файл создан и заполнен
- [ ] deploy.sh выполнен успешно
- [ ] Суперпользователь создан
- [ ] systemd сервис запущен
- [ ] Nginx настроен и запущен
- [ ] SSL сертификат установлен
- [ ] HTTPS работает (зеленый замочек)
- [ ] Данные из SQLite перенесены (если нужно)
- [ ] Медиа-файлы загружены и отображаются
- [ ] Админка доступна и работает
- [ ] Сайт открывается по домену лин-кор.рф
- [ ] Все фото и номер телефона отображаются

---

## 12. Поддержка и документация

### Логи для диагностики

```bash
# Gunicorn
sudo tail -f /home/django/projects/engineering_site/logs/gunicorn_error.log
sudo tail -f /home/django/projects/engineering_site/logs/gunicorn_access.log

# Nginx
sudo tail -f /var/log/nginx/engineering_site_error.log
sudo tail -f /var/log/nginx/engineering_site_access.log

# systemd
sudo journalctl -u engineering_site -f
```

### Мониторинг ресурсов

```bash
# Загрузка системы
htop

# Использование диска
df -h
ncdu /home/django

# Активные соединения
sudo netstat -tulpn
```

---

## 🎉 Готово!

Ваш сайт **лин-кор.рф** теперь работает на VPS с:
- ✅ PostgreSQL для надежного хранения данных
- ✅ Nginx для быстрой отдачи статики и медиа
- ✅ Gunicorn для обработки Django
- ✅ SSL сертификатом для безопасности
- ✅ Автоматическими обновлениями сертификата
- ✅ Настроенной системой безопасности

**Удачной работы! 🚀**

