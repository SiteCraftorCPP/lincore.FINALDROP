#!/bin/bash
# Скрипт для автоматической установки SSL сертификата Let's Encrypt
# Использование: sudo bash setup_ssl.sh

set -e  # Остановка при ошибке

echo "======================================"
echo "Установка SSL сертификата Let's Encrypt"
echo "======================================"
echo ""

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка прав root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Ошибка: Этот скрипт должен быть запущен с правами root${NC}"
    echo "Используйте: sudo bash setup_ssl.sh"
    exit 1
fi

# Домен (Punycode версия для кириллического домена)
DOMAIN="xn----otbhblio.xn--p1ai"
DOMAIN_RU="лин-кор.рф"
WWW_DOMAIN="www.xn----otbhblio.xn--p1ai"

echo -e "${YELLOW}Домен: ${DOMAIN_RU} (${DOMAIN})${NC}"
echo ""

# Проверка установки Nginx
if ! command -v nginx &> /dev/null; then
    echo -e "${RED}Ошибка: Nginx не установлен!${NC}"
    exit 1
fi

# Установка Certbot
echo -e "${YELLOW}Установка Certbot...${NC}"
apt update
apt install -y certbot python3-certbot-nginx

# Проверка конфигурации Nginx
echo -e "${YELLOW}Проверка конфигурации Nginx...${NC}"
nginx -t

if [ $? -ne 0 ]; then
    echo -e "${RED}Ошибка: Конфигурация Nginx содержит ошибки!${NC}"
    exit 1
fi

# Перезапуск Nginx
echo -e "${YELLOW}Перезапуск Nginx...${NC}"
systemctl restart nginx

# Получение SSL сертификата
echo -e "${YELLOW}Получение SSL сертификата от Let's Encrypt...${NC}"
echo ""
echo -e "${YELLOW}ВАЖНО: Убедитесь, что домен ${DOMAIN_RU} направлен на этот сервер!${NC}"
echo ""

certbot --nginx \
    -d "$DOMAIN" \
    -d "$WWW_DOMAIN" \
    --non-interactive \
    --agree-tos \
    --redirect \
    --email admin@${DOMAIN} \
    --keep-until-expiring

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}======================================"
    echo -e "SSL сертификат успешно установлен!"
    echo -e "======================================${NC}"
    echo ""
    echo -e "${GREEN}Ваш сайт теперь доступен по HTTPS:${NC}"
    echo -e "${GREEN}https://${DOMAIN_RU}${NC}"
    echo -e "${GREEN}https://${DOMAIN}${NC}"
    echo ""
    
    # Проверка автоматического обновления
    echo -e "${YELLOW}Проверка автоматического обновления сертификата...${NC}"
    certbot renew --dry-run
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Автоматическое обновление настроено корректно!${NC}"
    else
        echo -e "${YELLOW}Предупреждение: Возможны проблемы с автоматическим обновлением${NC}"
    fi
    
    # Проверка статуса таймера
    echo ""
    echo -e "${YELLOW}Статус таймера обновления сертификата:${NC}"
    systemctl status certbot.timer --no-pager
    
else
    echo ""
    echo -e "${RED}======================================"
    echo -e "Ошибка при получении SSL сертификата!"
    echo -e "======================================${NC}"
    echo ""
    echo -e "${YELLOW}Возможные причины:${NC}"
    echo "1. Домен не направлен на этот сервер"
    echo "2. Порт 80 заблокирован файрволом"
    echo "3. Nginx не запущен или настроен неправильно"
    echo ""
    echo -e "${YELLOW}Проверьте:${NC}"
    echo "- DNS записи домена"
    echo "- Доступность порта 80: sudo ufw status"
    echo "- Статус Nginx: sudo systemctl status nginx"
    exit 1
fi

echo ""
echo -e "${YELLOW}Рекомендации:${NC}"
echo "1. Сертификат будет автоматически обновляться"
echo "2. Проверить обновление можно командой: sudo certbot renew --dry-run"
echo "3. Настройте .env файл: SECURE_SSL_REDIRECT=True"
echo ""

