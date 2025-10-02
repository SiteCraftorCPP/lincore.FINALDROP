#!/bin/bash
# Скрипт для миграции данных из SQLite в PostgreSQL
# Использование: bash migrate_to_postgresql.sh

set -e  # Остановка при ошибке

echo "======================================"
echo "Миграция данных из SQLite в PostgreSQL"
echo "======================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo -e "${RED}Ошибка: Виртуальное окружение не найдено!${NC}"
    echo "Создайте виртуальное окружение: python3 -m venv venv"
    exit 1
fi

# Активация виртуального окружения
echo -e "${YELLOW}Активация виртуального окружения...${NC}"
source venv/bin/activate

# Проверка наличия базы данных SQLite
if [ ! -f "db.sqlite3" ]; then
    echo -e "${RED}Ошибка: Файл db.sqlite3 не найден!${NC}"
    exit 1
fi

# Создание резервной копии SQLite
echo -e "${YELLOW}Создание резервной копии SQLite...${NC}"
BACKUP_FILE="db_backup_$(date +%Y%m%d_%H%M%S).sqlite3"
cp db.sqlite3 "$BACKUP_FILE"
echo -e "${GREEN}Резервная копия создана: $BACKUP_FILE${NC}"
echo ""

# Экспорт данных из SQLite
echo -e "${YELLOW}Экспорт данных из SQLite...${NC}"
python manage.py dumpdata \
    --natural-foreign \
    --natural-primary \
    --exclude auth.permission \
    --exclude contenttypes \
    --indent 2 \
    > datadump.json

echo -e "${GREEN}Данные экспортированы в datadump.json${NC}"
echo ""

# Проверка .env файла
if [ ! -f ".env" ]; then
    echo -e "${RED}Ошибка: Файл .env не найден!${NC}"
    echo "Создайте файл .env с настройками PostgreSQL"
    exit 1
fi

# Загрузка переменных окружения
export $(cat .env | grep -v '^#' | xargs)

# Проверка DATABASE_URL
if [ -z "$DATABASE_URL" ]; then
    echo -e "${RED}Ошибка: DATABASE_URL не задан в .env${NC}"
    exit 1
fi

echo -e "${YELLOW}Переключение на production настройки...${NC}"
export DJANGO_SETTINGS_MODULE=engineering_site.settings_production

# Применение миграций к PostgreSQL
echo -e "${YELLOW}Применение миграций к PostgreSQL...${NC}"
python manage.py migrate --noinput

# Импорт данных в PostgreSQL
echo -e "${YELLOW}Импорт данных в PostgreSQL...${NC}"
python manage.py loaddata datadump.json

echo ""
echo -e "${GREEN}======================================"
echo -e "Миграция успешно завершена!"
echo -e "======================================${NC}"
echo ""
echo "Резервная копия SQLite: $BACKUP_FILE"
echo "Экспортированные данные: datadump.json"
echo ""
echo -e "${YELLOW}Рекомендации:${NC}"
echo "1. Проверьте работу сайта с PostgreSQL"
echo "2. Убедитесь, что все данные перенесены корректно"
echo "3. После проверки можете удалить datadump.json"
echo ""

