#!/bin/bash
# Главный скрипт деплоя Engineering Site на VPS
# Использование: bash deploy.sh

set -e  # Остановка при ошибке

echo "======================================"
echo "Деплой Engineering Site"
echo "======================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
print_step() {
    echo ""
    echo -e "${BLUE}==> $1${NC}"
    echo ""
}

print_error() {
    echo -e "${RED}Ошибка: $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Проверка прав (НЕ root)
if [ "$EUID" -eq 0 ]; then 
    print_error "Этот скрипт НЕ должен запускаться от root!"
    echo "Запустите от пользователя django: bash deploy.sh"
    exit 1
fi

# Переменные
PROJECT_DIR="$HOME/projects/engineering_site"
VENV_DIR="$PROJECT_DIR/venv"

# 1. Подготовка окружения
print_step "Шаг 1: Подготовка окружения"

if [ ! -d "$PROJECT_DIR" ]; then
    print_error "Директория проекта не найдена: $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"
print_success "Рабочая директория: $(pwd)"

# 2. Создание необходимых директорий
print_step "Шаг 2: Создание необходимых директорий"

mkdir -p logs
mkdir -p media
mkdir -p staticfiles
mkdir -p backups

print_success "Директории созданы"

# 3. Создание виртуального окружения
print_step "Шаг 3: Виртуальное окружение"

if [ ! -d "$VENV_DIR" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    print_success "Виртуальное окружение создано"
else
    print_success "Виртуальное окружение уже существует"
fi

# Активация виртуального окружения
source venv/bin/activate
print_success "Виртуальное окружение активировано"

# 4. Обновление pip и установка зависимостей
print_step "Шаг 4: Установка зависимостей"

echo "Обновление pip..."
pip install --upgrade pip --quiet

echo "Установка пакетов из requirements.txt..."
pip install -r requirements.txt --quiet

print_success "Зависимости установлены"

# 5. Проверка .env файла
print_step "Шаг 5: Проверка конфигурации"

if [ ! -f ".env" ]; then
    print_error "Файл .env не найден!"
    echo ""
    echo "Создайте файл .env со следующими параметрами:"
    echo ""
    echo "SECRET_KEY=ваш-секретный-ключ"
    echo "DEBUG=False"
    echo "ALLOWED_HOSTS=xn----otbhblio.xn--p1ai,лин-кор.рф,5.129.251.41"
    echo "DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DB_NAME"
    echo "SECURE_SSL_REDIRECT=False  # Установите True после настройки SSL"
    echo ""
    echo "Для генерации SECRET_KEY выполните:"
    echo "python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
    exit 1
fi

# Загрузка переменных окружения
set -a
source .env
set +a

print_success "Файл .env найден и загружен"

# Проверка обязательных переменных
if [ -z "$SECRET_KEY" ] || [ -z "$DATABASE_URL" ] || [ -z "$ALLOWED_HOSTS" ]; then
    print_error "Не все обязательные переменные заданы в .env!"
    echo "Проверьте: SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS"
    exit 1
fi

# 6. Применение миграций
print_step "Шаг 6: Применение миграций базы данных"

export DJANGO_SETTINGS_MODULE=engineering_site.settings_production

echo "Выполнение миграций..."
python manage.py migrate --noinput

print_success "Миграции применены"

# 7. Сбор статических файлов
print_step "Шаг 7: Сбор статических файлов"

echo "Сбор статики..."
python manage.py collectstatic --noinput --clear

print_success "Статические файлы собраны"

# 8. Создание суперпользователя (если нужно)
print_step "Шаг 8: Суперпользователь"

echo "Проверка наличия суперпользователя..."
if python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(is_superuser=True).exists())" | grep -q "False"; then
    print_warning "Суперпользователь не найден!"
    echo ""
    echo "Создайте суперпользователя после деплоя:"
    echo "cd $PROJECT_DIR && source venv/bin/activate"
    echo "export DJANGO_SETTINGS_MODULE=engineering_site.settings_production"
    echo "python manage.py createsuperuser"
else
    print_success "Суперпользователь существует"
fi

# 9. Настройка прав доступа
print_step "Шаг 9: Настройка прав доступа"

chmod -R 755 staticfiles
chmod -R 755 media
chown -R $USER:www-data media

print_success "Права доступа настроены"

# 10. Тестирование конфигурации
print_step "Шаг 10: Тестирование"

echo "Проверка конфигурации Django..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    print_success "Конфигурация Django корректна"
else
    print_warning "Обнаружены предупреждения в конфигурации Django"
fi

# Проверка подключения к БД
echo "Проверка подключения к базе данных..."
if python manage.py showmigrations > /dev/null 2>&1; then
    print_success "Подключение к базе данных работает"
else
    print_error "Не удалось подключиться к базе данных!"
    exit 1
fi

# 11. Информация о следующих шагах
echo ""
echo -e "${GREEN}======================================"
echo -e "Деплой приложения завершен!"
echo -e "======================================${NC}"
echo ""
echo -e "${YELLOW}Следующие шаги:${NC}"
echo ""
echo "1. Установите systemd сервис для Gunicorn:"
echo -e "   ${BLUE}sudo cp $PROJECT_DIR/engineering_site.service /etc/systemd/system/${NC}"
echo -e "   ${BLUE}sudo systemctl daemon-reload${NC}"
echo -e "   ${BLUE}sudo systemctl enable engineering_site${NC}"
echo -e "   ${BLUE}sudo systemctl start engineering_site${NC}"
echo -e "   ${BLUE}sudo systemctl status engineering_site${NC}"
echo ""
echo "2. Настройте Nginx:"
echo -e "   ${BLUE}sudo cp $PROJECT_DIR/nginx_config.conf /etc/nginx/sites-available/engineering_site${NC}"
echo -e "   ${BLUE}sudo ln -s /etc/nginx/sites-available/engineering_site /etc/nginx/sites-enabled/${NC}"
echo -e "   ${BLUE}sudo nginx -t${NC}"
echo -e "   ${BLUE}sudo systemctl restart nginx${NC}"
echo ""
echo "3. Установите SSL сертификат:"
echo -e "   ${BLUE}sudo bash $PROJECT_DIR/setup_ssl.sh${NC}"
echo ""
echo "4. После установки SSL обновите .env:"
echo -e "   ${BLUE}SECURE_SSL_REDIRECT=True${NC}"
echo -e "   ${BLUE}sudo systemctl restart engineering_site${NC}"
echo ""
echo "5. Проверьте работу сайта:"
echo -e "   ${BLUE}http://лин-кор.рф${NC}"
echo -e "   ${BLUE}http://5.129.251.41${NC}"
echo ""
echo "6. Если были данные в SQLite, перенесите их:"
echo -e "   ${BLUE}bash $PROJECT_DIR/migrate_to_postgresql.sh${NC}"
echo ""
echo -e "${GREEN}Готово! Удачного деплоя! 🚀${NC}"
echo ""

