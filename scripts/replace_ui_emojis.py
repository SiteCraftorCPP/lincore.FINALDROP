# -*- coding: utf-8 -*-
"""One-off: replace common emoji spans in Django HTML templates with ui_icon includes."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "website" / "templates"

INC = "{% include 'website/partials/ui_icon.html' with name='%s' %s %}"

REPLACEMENTS = [
    # (pattern, replacement) — pattern is regex
    (r'<span class="btn-icon">📝</span>', INC % ("pen-line", "w=20 h=20")),
    (r'<span class="btn-icon">📞</span>', INC % ("phone", "w=20 h=20")),
    (r'<span class="btn-icon">📋</span>', INC % ("clipboard-list", "w=20 h=20")),
    (r'<span class="btn-icon">🛠</span>', INC % ("wrench", "w=20 h=20")),
    (r'<span class="btn-icon">🚨</span>', INC % ("alert-circle", "w=20 h=20")),
    (r'<span class="phone-icon">📞</span>', INC % ("phone", "svg_class='phone-icon' w=20 h=20")),
    (r'<span class="pill-icon">🔧</span>', INC % ("wrench", "w=20 h=20")),
    (r'<span class="pill-icon">🛠</span>', INC % ("wrench", "w=20 h=20")),
    (r'<span class="pill-icon">⚡</span>', INC % ("zap", "w=20 h=20")),
    (r'<span class="pill-icon">📊</span>', INC % ("bar-chart-2", "w=20 h=20")),
    (r'<span class="pill-icon">✅</span>', INC % ("circle-check", "w=20 h=20")),
    (r'<span class="pill-icon">⚖️</span>', INC % ("scale", "w=20 h=20")),
    (r'<span class="pill-icon">🔍</span>', INC % ("search", "w=20 h=20")),
    (r'<span class="pill-icon">📄</span>', INC % ("file-text", "w=20 h=20")),
    (r'<span class="pill-icon">📍</span>', INC % ("map-pin", "w=20 h=20")),
    (r'<span class="pill-icon">🏗</span>', INC % ("hammer", "w=20 h=20")),
    (r'<span class="pill-icon">⭐</span>', INC % ("circle-check", "w=20 h=20")),
    (r'<span class="pill-icon">👨‍🔧</span>', INC % ("users", "w=20 h=20")),
    (r'<span class="badge-icon">🛠</span>', INC % ("wrench", "svg_class='badge-icon-svg' w=22 h=22")),
    (r'<span class="badge-icon">⚖️</span>', INC % ("scale", "svg_class='badge-icon-svg' w=22 h=22")),
    (r'<span class="badge-icon">🚨</span>', INC % ("alert-circle", "svg_class='badge-icon-svg' w=22 h=22")),
    (r'<span class="badge-icon">🔍</span>', INC % ("search", "svg_class='badge-icon-svg' w=22 h=22")),
    (r'<span class="header-email-copy__btn-icon" aria-hidden="true">📋</span>',
     f'<span class="header-email-copy__btn-icon" aria-hidden="true">{INC % ("clipboard-list", "w=18 h=18")}</span>'),
    (r'<span class="mobile-menu-quick__icon" aria-hidden="true">✉️</span>',
     f'<span class="mobile-menu-quick__icon" aria-hidden="true">{INC % ("mail", "w=22 h=22")}</span>'),
]

# Second pass: more specific multiline or alternate class names
EXTRA = [
    (r'<span class="btn-icon animated-document">📋</span>', INC % ("clipboard-list", "w=20 h=20")),
    (r'<span class="btn-icon animated-phone">📞</span>', INC % ("phone", "w=20 h=20")),
    (r'<span class="btn-icon animated-document">📝</span>', INC % ("pen-line", "w=20 h=20")),
]


def main():
    for path in sorted(ROOT.rglob("*.html")):
        if "ui_icon.html" in str(path):
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for pat, rep in REPLACEMENTS + EXTRA:
            text = re.sub(pat, rep, text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.relative_to(ROOT.parent.parent))


if __name__ == "__main__":
    main()
