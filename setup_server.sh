#!/bin/bash
# Скрипт для первичной настройки VPS сервера
# Использование: sudo bash setup_server.sh

set -e  # Остановка при ошибке

echo "======================================"
echo "Настройка VPS для Engineering Site"
echo "======================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Ошибка: Этот скрипт должен быть запущен с правами root${NC}"
    echo "Используйте: sudo bash setup_server.sh"
    exit 1
fi

print_step() {
    echo ""
    echo -e "${BLUE}==> $1${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# 1. Обновление системы
print_step "Шаг 1: Обновление системы"

apt update
apt upgrade -y

print_success "Система обновлена"

# 2. Установка необходимых пакетов
print_step "Шаг 2: Установка базовых пакетов"

apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    git \
    nginx \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    curl \
    wget \
    ufw \
    htop \
    ncdu \
    unzip

print_success "Базовые пакеты установлены"

# 3. Создание пользователя django
print_step "Шаг 3: Создание пользователя для приложения"

if id "django" &>/dev/null; then
    print_warning "Пользователь django уже существует"
else
    useradd -m -s /bin/bash django
    usermod -aG www-data django
    print_success "Пользователь django создан"
fi

# 4. Настройка PostgreSQL
print_step "Шаг 4: Настройка PostgreSQL"

# Запуск PostgreSQL
systemctl start postgresql
systemctl enable postgresql

print_success "PostgreSQL запущен"

# Создание базы данных и пользователя
echo "Создание базы данных и пользователя..."

# Генерация случайного пароля
DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-25)

sudo -u postgres psql << EOF
-- Создание базы данных
CREATE DATABASE engineering_site_db;

-- Создание пользователя
CREATE USER django_user WITH PASSWORD '$DB_PASSWORD';

-- Настройка параметров
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'Europe/Moscow';

-- Выдача прав
GRANT ALL PRIVILEGES ON DATABASE engineering_site_db TO django_user;

\q
EOF

print_success "База данных создана"

# Сохранение данных подключения
echo ""
echo -e "${YELLOW}======================================"
echo -e "СОХРАНИТЕ ЭТИ ДАННЫЕ!"
echo -e "======================================${NC}"
echo ""
echo "База данных: engineering_site_db"
echo "Пользователь: django_user"
echo "Пароль: $DB_PASSWORD"
echo ""
echo "DATABASE_URL для .env файла:"
echo "DATABASE_URL=postgresql://django_user:$DB_PASSWORD@localhost:5432/engineering_site_db"
echo ""
echo -e "${YELLOW}======================================"
echo ""

# Сохранение в файл
cat > /root/db_credentials.txt << EOF
База данных PostgreSQL для Engineering Site
Создано: $(date)

База данных: engineering_site_db
Пользователь: django_user
Пароль: $DB_PASSWORD

DATABASE_URL для .env файла:
DATABASE_URL=postgresql://django_user:$DB_PASSWORD@localhost:5432/engineering_site_db
EOF

chmod 600 /root/db_credentials.txt
echo -e "${GREEN}Данные сохранены в /root/db_credentials.txt${NC}"
echo ""

# 5. Настройка Nginx
print_step "Шаг 5: Настройка Nginx"

systemctl start nginx
systemctl enable nginx

# Удаление дефолтного сайта
rm -f /etc/nginx/sites-enabled/default

print_success "Nginx настроен"

# 6. Настройка файрвола
print_step "Шаг 6: Настройка файрвола (UFW)"

ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw --force enable

print_success "Файрвол настроен"

# 7. Создание директорий проекта
print_step "Шаг 7: Создание структуры директорий"

mkdir -p /home/django/projects
chown django:django /home/django/projects

print_success "Директории созданы"

# 8. Настройка автоматических обновлений безопасности
print_step "Шаг 8: Настройка автоматических обновлений"

apt install -y unattended-upgrades
dpkg-reconfigure -plow unattended-upgrades

print_success "Автоматические обновления настроены"

# 9. Установка Fail2Ban (защита от брутфорса)
print_step "Шаг 9: Установка Fail2Ban"

apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

print_success "Fail2Ban установлен"

# 10. Итоговая информация
echo ""
echo -e "${GREEN}======================================"
echo -e "Настройка сервера завершена!"
echo -e "======================================${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo ""
echo "1. Переключитесь на пользователя django:"
echo -e "   ${BLUE}su - django${NC}"
echo ""
echo "2. Создайте директорию проекта:"
echo -e "   ${BLUE}mkdir -p ~/projects/engineering_site${NC}"
echo -e "   ${BLUE}cd ~/projects/engineering_site${NC}"
echo ""
echo "3. Загрузите проект на сервер:"
echo -e "   ${BLUE}# На вашем компьютере:${NC}"
echo -e "   ${BLUE}scp -r /путь/к/проекту/* django@5.129.251.41:~/projects/engineering_site/${NC}"
echo ""
echo "4. На сервере запустите скрипт деплоя:"
echo -e "   ${BLUE}cd ~/projects/engineering_site${NC}"
echo -e "   ${BLUE}bash deploy.sh${NC}"
echo ""
echo -e "${YELLOW}Важная информация:${NC}"
echo "- Данные PostgreSQL сохранены в /root/db_credentials.txt"
echo "- Используйте их для настройки .env файла"
echo ""
echo -e "${GREEN}Готово! 🚀${NC}"
echo ""

