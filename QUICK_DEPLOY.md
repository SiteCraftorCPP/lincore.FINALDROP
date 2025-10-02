# 🚀 Быстрый деплой Engineering Site

## Информация о домене

- **Домен:** лин-кор.рф (xn----otbhblio.xn--p1ai)
- **IP сервера:** 5.129.251.41

---

## Пошаговая инструкция

### 1. Генерация SECRET_KEY (на вашем компьютере)

```powershell
cd "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21"
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Сохраните полученный ключ!**

### 2. Подключение к серверу

```powershell
ssh root@5.129.251.41
```

### 3. Загрузка скрипта настройки (с вашего компьютера)

```powershell
scp "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\setup_server.sh" root@5.129.251.41:/tmp/
```

### 4. Запуск настройки сервера (на сервере)

```bash
cd /tmp
chmod +x setup_server.sh
bash setup_server.sh
```

**ВАЖНО:** Сохраните данные PostgreSQL из вывода!

### 5. Загрузка проекта на сервер (с вашего компьютера)

Создайте архив:

```powershell
cd "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21"
Compress-Archive -Path * -DestinationPath engineering_site.zip -Force
```

Загрузите на сервер:

```powershell
scp engineering_site.zip django@5.129.251.41:~/
```

### 6. Распаковка и деплой (на сервере)

```bash
# Переключитесь на пользователя django
su - django

# Распакуйте проект
mkdir -p ~/projects
cd ~/projects
unzip ~/engineering_site.zip -d engineering_site
cd engineering_site

# Создайте .env файл
nano .env
```

Вставьте в .env:

```env
SECRET_KEY=ваш-секретный-ключ-из-шага-1
DEBUG=False
ALLOWED_HOSTS=xn----otbhblio.xn--p1ai,лин-кор.рф,www.xn----otbhblio.xn--p1ai,5.129.251.41
DATABASE_URL=postgresql://django_user:пароль-из-шага-4@localhost:5432/engineering_site_db
SECURE_SSL_REDIRECT=False
```

Сохраните: `Ctrl+X`, `Y`, `Enter`

Запустите деплой:

```bash
bash deploy.sh
```

### 7. Создание суперпользователя

```bash
cd ~/projects/engineering_site
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production
python manage.py createsuperuser
```

Введите имя пользователя, email и пароль.

### 8. Настройка systemd и Nginx (под root)

```bash
exit  # Выход из пользователя django
su -  # Или ssh root@5.129.251.41

# Установка systemd сервиса
cp /home/django/projects/engineering_site/engineering_site.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable engineering_site
systemctl start engineering_site
systemctl status engineering_site

# Настройка Nginx
cp /home/django/projects/engineering_site/nginx_config.conf /etc/nginx/sites-available/engineering_site
ln -s /etc/nginx/sites-available/engineering_site /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### 9. Проверка работы

Откройте браузер: http://5.129.251.41 или http://лин-кор.рф

Должен открыться сайт!

### 10. Установка SSL

```bash
cd /home/django/projects/engineering_site
bash setup_ssl.sh
```

После успешной установки:

```bash
su - django
cd ~/projects/engineering_site
nano .env
```

Измените: `SECURE_SSL_REDIRECT=True`

Сохраните и перезапустите:

```bash
exit
systemctl restart engineering_site
```

### 11. Перенос данных и медиа (если есть)

```powershell
# С вашего компьютера
scp "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\db.sqlite3" django@5.129.251.41:~/projects/engineering_site/
scp -r "C:\Users\MOD PC COMPANY\Desktop\kwork.aaaaa21\media\*" django@5.129.251.41:~/projects/engineering_site/media/
```

На сервере:

```bash
su - django
cd ~/projects/engineering_site
bash migrate_to_postgresql.sh

# Настройка прав на медиа
sudo chmod -R 755 media
sudo chown -R django:www-data media
```

---

## ✅ Готово!

Ваш сайт теперь доступен по адресу: **https://лин-кор.рф**

### Проверьте:

1. ✅ Сайт открывается по HTTPS
2. ✅ Админка работает: https://лин-кор.рф/admin/
3. ✅ Фото отображаются
4. ✅ Номер телефона отображается

---

## 🛠 Решение проблем

### Gunicorn не запускается

```bash
sudo journalctl -u engineering_site -n 50
```

Проверьте .env файл и DATABASE_URL.

### Фото не отображаются

```bash
su - django
cd ~/projects/engineering_site
sudo chmod -R 755 media
sudo chown -R django:www-data media
```

### 502 Bad Gateway

```bash
sudo systemctl status engineering_site
sudo systemctl restart engineering_site nginx
```

### SSL не устанавливается

Проверьте, что DNS настроен:

```bash
ping лин-кор.рф  # Должен показать 5.129.251.41
```

Убедитесь, что порты открыты:

```bash
sudo ufw status
```

---

## 📚 Полная документация

Смотрите: `DEPLOY_GUIDE_FULL.md`

---

**Удачи! 🚀**

