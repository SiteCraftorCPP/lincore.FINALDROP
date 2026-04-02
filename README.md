# Engineering Site — сайт инженерно-сервисной компании

Веб-сайт на Django для компании, занимающейся обслуживанием инженерных систем.

## Возможности

- Адаптивная вёрстка
- Несколько страниц услуг
- Админка Django для контента и заявок
- Галереи и загрузка изображений через админку

## Стек

- Django 3.2
- HTML, CSS, JavaScript
- SQLite (по умолчанию)

## Запуск локально

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # по желанию
python manage.py runserver
```

Сайт: `http://127.0.0.1:8000/`

## Переменные окружения

Необязательно: можно скопировать `env_example.txt` в `.env` и задать `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`. Иначе используются значения из `engineering_site/settings.py`.

## Структура

- `engineering_site/` — настройки проекта и URL
- `website/` — приложение (модели, шаблоны, представления)
- `static/` — CSS, JS, изображения
- `media/` — загружаемые файлы (создаётся при работе, в git не коммитится)

## Лицензия

Проект для инженерно-сервисной компании «Линкор».
