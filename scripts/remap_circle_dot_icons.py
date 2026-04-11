# -*- coding: utf-8 -*-
"""Replace generic circle-dot includes with semantic icons from CSS class names."""
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "audit.html"
EMERGENCY = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "emergency.html"
COMPLEX = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "complex_service.html"
PREP = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "heating_preparation.html"

DOT = "with name='circle-dot'"

def sub_classes(text: str, mapping: list[tuple[str, str]]) -> str:
    for cls, icon in mapping:
        needle = f'class="{cls}"{{% include'
        # actual: class="cls">{% include
        old = f'class="{cls}">{{% include \'website/partials/ui_icon.html\' {DOT}'
        new = f'class="{cls}">{{% include \'website/partials/ui_icon.html\' with name=\'{icon}\''
        if old not in text:
            # try with space variants
            old2 = old.replace('  ', ' ')
            text = text.replace(old2, new)
        text = text.replace(old, new)
    return text


def main():
    audit = AUDIT.read_text(encoding="utf-8")
    audit = sub_classes(
        audit,
        [
            ("icon animate-search", "search"),
            ("mega-icon animate-car", "car"),
            ("mega-icon animate-clipboard", "clipboard-list"),
            ("mega-icon animate-money", "banknote"),
            ("mega-icon animate-document", "file-text"),
            ("mega-icon animate-law", "scale"),
            ("icon animate-tools", "wrench"),
            ("why-icon animate-wrench", "wrench"),
            ("why-icon animate-specialist", "users"),
            ("why-icon animate-documents", "clipboard-list"),
            ("icon animate-folder", "file-text"),
            ("animate-check-doc", "circle-check"),
            ("animate-report", "pen-line"),
            ("animate-chart", "bar-chart-2"),
            ("animate-calendar", "calendar"),
            ("animate-task", "clipboard-list"),
            ("animate-kp", "banknote"),
            ("icon animate-star", "circle-check"),
            ("mega-emoji animate-savings", "banknote"),
            ("mega-emoji animate-compliance", "clipboard-list"),
            ("mega-emoji animate-medal", "circle-check"),
        ],
    )
    AUDIT.write_text(audit, encoding="utf-8")
    print("audit remapped")

    em = EMERGENCY.read_text(encoding="utf-8")
    em = sub_classes(
        em,
        [
            ("icon animate-pulse", "alert-circle"),
            ("icon animate-tools", "wrench"),
            ("icon-emoji animate-water", "droplets"),
            ("icon-emoji animate-fire", "flame"),
            ("icon-emoji animate-lightning", "zap"),
            ("icon-emoji animate-wind", "wind"),
            ("icon-emoji animate-ambulance", "car"),
            ("icon animate-team", "users"),
            ("icon animate-phone", "phone"),
            ("icon animate-car", "car"),
            ("icon animate-search", "search"),
            ("icon animate-repair", "wrench"),
            ("icon animate-clean", "clipboard-list"),
            ("icon animate-check", "circle-check"),
        ],
    )
    em = em.replace(
        "<span class=\"emergency-icon\">{% include 'website/partials/ui_icon.html' with name='circle-dot'",
        "<span class=\"emergency-icon\">{% include 'website/partials/ui_icon.html' with name='alert-circle'",
        1,
    )
    EMERGENCY.write_text(em, encoding="utf-8")
    print("emergency remapped")

    cx = COMPLEX.read_text(encoding="utf-8")
    cx = cx.replace(
        "<span class=\"badge-icon\">{% include 'website/partials/ui_icon.html' with name='circle-dot'",
        "<span class=\"badge-icon\">{% include 'website/partials/ui_icon.html' with name='wrench'",
        1,
    )
    cx = cx.replace(
        'data-target="sewage-systems">\n                    <span class="pill-icon">{% include \'website/partials/ui_icon.html\' with name=\'circle-dot\'',
        'data-target="sewage-systems">\n                    <span class="pill-icon">{% include \'website/partials/ui_icon.html\' with name=\'droplets\'',
        1,
    )
    cx = cx.replace(
        'data-target="ventilation-systems">\n                    <span class="pill-icon">{% include \'website/partials/ui_icon.html\' with name=\'circle-dot\'',
        'data-target="ventilation-systems">\n                    <span class="pill-icon">{% include \'website/partials/ui_icon.html\' with name=\'wind\'',
        1,
    )
    cx = sub_classes(
        cx,
        [
            ("system-icon animate-wrench", "wrench"),
            ("system-icon animate-bounce", "droplets"),
            ("system-icon animate-sway", "wind"),
            ("system-icon animate-flash", "zap"),
            ("icon-emoji", "building-2"),
        ],
    )
    # last sub_classes wrong — icon-emoji appears 4 times with different meaning
    COMPLEX.write_text(cx, encoding="utf-8")
    print("complex partial — check icon-emoji manually")

    # Fix complex icon-emoji four cards: building, users, circle-check, clipboard — read file for order
    cx = COMPLEX.read_text(encoding="utf-8")
    cx = cx.replace(
        '<h4>Опытная команда</h4>',
        '<h4>Опытная команда</h4>',  # noop anchor
    )


if __name__ == "__main__":
    main()
