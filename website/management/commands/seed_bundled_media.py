"""Создаёт JPEG в static/bundled_media/ по всем путям, которые ждёт сайт (если локально нет media/)."""

from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from PIL import Image, ImageDraw, ImageFont


def _paths():
    rels = []
    for i in range(1, 5):
        rels.append(f'str1/photo{i}.jpg')
    for i in range(14, 18):
        rels.append(f'str1/photo{i}.jpg')
    for i in range(5, 9):
        rels.append(f'str2/photo{i}.jpg')
    rels.extend([
        'str3/photo9.jpg', 'str3/photoFF.jpg',
        'str3/photou.jpg', 'str3/photop.jpg', 'str3/photoy.jpg', 'str3/photog.jpg',
        'str4/photojk.jpg', 'str4/photopkk.jpg', 'str4/photoub.jpg', 'str4/photogl.jpg',
    ])
    for i in range(10, 14):
        rels.append(f'str5/photo{i}.jpg')
    rels.extend([
        'str7/photoug.jpg', 'str7/photoyk.jpg', 'str7/kp.jpg',
        'str8/photougtt.jpg', 'str8/photoyktt.jpg',
        'str9/vent1.jpg', 'str9/vent2.jpg',
    ])
    return rels


def _write_jpeg(path: Path, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    w, h = 960, 640
    img = Image.new('RGB', (w, h), (236, 240, 249))
    draw = ImageDraw.Draw(img)
    for y in range(0, h, 48):
        draw.line([(0, y), (w, y)], fill=(220, 226, 238), width=1)
    draw.rectangle([24, 24, w - 24, h - 24], outline=(99, 102, 241), width=3)
    font = ImageFont.load_default()
    text = label[:80]
    tw = draw.textlength(text, font=font) if hasattr(draw, 'textlength') else len(text) * 8
    draw.text(((w - tw) // 2, h // 2 - 20), text, fill=(51, 65, 85), font=font)
    buf = BytesIO()
    img.save(buf, format='JPEG', quality=82, optimize=True)
    path.write_bytes(buf.getvalue())


class Command(BaseCommand):
    help = 'Заполняет static/bundled_media/ JPEG-файлами (заглушки), чтобы после git pull на VPS картинки открывались.'

    def handle(self, *args, **options):
        root = Path(settings.BASE_DIR) / 'static' / 'bundled_media'
        n = 0
        for rel in _paths():
            dest = root.joinpath(*rel.split('/'))
            if dest.is_file():
                continue
            _write_jpeg(dest, rel)
            n += 1
            self.stdout.write(self.style.SUCCESS(f'+ {rel}'))
        if n == 0:
            self.stdout.write('Все файлы уже есть; ничего не создано.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Создано файлов: {n}. Закоммитьте static/bundled_media/'))
