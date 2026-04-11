"""Копирование media/str* → static/bundled_media/ для коммита в git (картинки на VPS без ручной заливки)."""

from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand

# Те же каталоги, что использует get_photos_context() в website.views
MEDIA_SUBDIRS = ('str1', 'str2', 'str3', 'str4', 'str5', 'str7', 'str8', 'str9')


class Command(BaseCommand):
    help = (
        'Копирует папки media/str1 … str9 в static/bundled_media/. '
        'Дальше: git add static/bundled_media && git commit — на VPS после pull и collectstatic картинки подхватятся.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать, что было бы скопировано',
        )

    def handle(self, *args, **options):
        dry = options['dry_run']
        media_root = Path(settings.MEDIA_ROOT)
        dest_root = Path(settings.BASE_DIR) / 'static' / 'bundled_media'

        if not dry:
            dest_root.mkdir(parents=True, exist_ok=True)

        total = 0
        for name in MEDIA_SUBDIRS:
            src = media_root / name
            dst = dest_root / name
            if not src.is_dir():
                self.stdout.write(self.style.WARNING(f'Нет папки: {src}'))
                continue
            if dry:
                n = sum(1 for p in src.rglob('*') if p.is_file())
                self.stdout.write(f'[dry-run] {src} → {dst} ({n} файлов)')
                total += n
                continue
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            n = sum(1 for p in dst.rglob('*') if p.is_file())
            total += n
            self.stdout.write(self.style.SUCCESS(f'{name}: {n} файлов → {dst}'))

        if dry:
            self.stdout.write(self.style.NOTICE(f'Всего файлов: {total} (ничего не записано)'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Готово. Всего файлов: {total}. Закоммитьте static/bundled_media/'))
