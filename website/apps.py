from pathlib import Path

from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'website'

    def ready(self):
        # Каталоги под upload_to — иначе первая загрузка из админки падает с PermissionError/OSError.
        from django.conf import settings

        root = getattr(settings, 'MEDIA_ROOT', None)
        if not root:
            return
        base = Path(root)
        for sub in (
            'photos',
            'gallery',
            'tender_tasks',
            'documents',
            'commercial_proposals',
        ):
            (base / sub).mkdir(parents=True, exist_ok=True)
