Папка bundled_media — копии media/str1, str2, … для деплоя через Git.

Один раз на машине, где уже лежат фотографии в media/:
  python manage.py bundle_site_media

Затем добавьте в коммит:
  git add static/bundled_media
  git commit -m "Site photos for production"

На VPS после git pull выполните collectstatic (если статика собирается в staticfiles).

Приоритет на сайте: сначала файл из media/ (админка), если нет — из bundled_media/.
