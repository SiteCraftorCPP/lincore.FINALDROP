# -*- coding: utf-8 -*-
"""Second pass: regex-based emoji cleanup in HTML templates."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "website" / "templates"
INC = "{%% include 'website/partials/ui_icon.html' with name='%s' %s %%}"


def wind_badge_repl(m):
    inner = INC % ("wind", "svg_class='badge-icon-svg' w=22 h=22")
    return f'<span class="badge-icon animated-maintenance">{inner}</span>'


def sub_file(path: Path, rules):
    text = path.read_text(encoding="utf-8")
    orig = text
    for rx, rep in rules:
        text = re.sub(rx, rep, text, flags=re.DOTALL)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        print("updated", path)


def main():
    # Ventilation: feature list emojis -> dot marker
    v = ROOT / "website" / "ventilation.html"
    if v.exists():
        t = v.read_text(encoding="utf-8")
        t = re.sub(
            r'<span class="mega-feature-emoji">[^<]*</span>',
            '<span class="mega-feature-marker" aria-hidden="true"></span>',
            t,
        )
        # Hero badge wind (may be \U0001f32c + fe0f)
        t = re.sub(
            r'<span class="badge-icon animated-maintenance">[\U0001f300-\U0001ffff\u2600-\u27BF\uFE0F\s]*</span>',
            wind_badge_repl,
            t,
        )
        # Section header icon
        t = re.sub(
            r'<span class="icon animated-maintenance">[\U0001f300-\U0001ffff\u2600-\u27BF\uFE0F\s]*</span>',
            f'<span class="icon animated-maintenance">{INC % ("wrench", "w=40 h=40")}</span>',
            t,
        )
        # Mega service header icons -> SVG
        t = re.sub(
            r'<span class="mega-service-icon animated-maintenance">[^<]*</span>',
            f'<span class="mega-service-icon animated-maintenance">{INC % ("calendar", "w=36 h=36")}</span>',
            t,
        )
        t = re.sub(
            r'<span class="mega-service-icon animated-season">🔄</span>',
            f'<span class="mega-service-icon animated-season">{INC % ("refresh-cw", "w=36 h=36")}</span>',
            t,
        )
        t = re.sub(
            r'<span class="mega-service-icon animated-season">☀️</span>',
            f'<span class="mega-service-icon animated-season">{INC % ("sun", "w=36 h=36")}</span>',
            t,
        )
        t = re.sub(
            r'<span class="mega-service-icon animated-season">❄️</span>',
            f'<span class="mega-service-icon animated-season">{INC % ("snowflake", "w=36 h=36")}</span>',
            t,
        )
        # Wrap bare includes in hero buttons with btn-icon
        t = t.replace(
            '<button class="btn-modern btn-primary" onclick="openApplicationModal()">\n'
            '                        <span class="btn-text">Оставить заявку</span>\n'
            "                        {% include 'website/partials/ui_icon.html' with name='clipboard-list' w=20 h=20 %}",
            '<button class="btn-modern btn-primary" onclick="openApplicationModal()">\n'
            '                        <span class="btn-text">Оставить заявку</span>\n'
            f'                        <span class="btn-icon">{INC % ("pen-line", "w=20 h=20")}</span>',
        )
        t = t.replace(
            '<button class="btn-modern btn-secondary" onclick="openCallbackModal()">\n'
            '                        <span class="btn-text">Заказать звонок специалиста</span>\n'
            "                        {% include 'website/partials/ui_icon.html' with name='phone' w=20 h=20 %}",
            '<button class="btn-modern btn-secondary" onclick="openCallbackModal()">\n'
            '                        <span class="btn-text">Заказать звонок специалиста</span>\n'
            f'                        <span class="btn-icon">{INC % ("phone", "w=20 h=20")}</span>',
        )
        v.write_text(t, encoding="utf-8")
        print("updated ventilation.html")

    # Generic: icon-emoji spans (installation etc.)
    for path in sorted((ROOT / "website").glob("*.html")):
        if path.name in ("ventilation.html", "index.html", "heating_service.html"):
            continue
        t = path.read_text(encoding="utf-8")
        orig = t

        # icon-emoji with single emoji char inside
        def ico(m):
            return m.group(1)  # keep wrapper, replace inner in separate pass

        t = re.sub(
            r'<span class="icon-emoji([^"]*)">[\U0001f300-\U0001ffff\u2600-\u27BF][\uFE0F\u200d\U0001f300-\U0001ffff\u2600-\u27BF]*</span>',
            lambda m: f'<span class="icon-emoji{m.group(1)}">{INC % ("circle-dot", "w=22 h=22")}</span>',
            t,
        )
        # mega-icon / why-icon / timeline-icon with emoji only
        for cls in ("mega-icon", "why-icon", "timeline-icon", "icon animate", "installation-icon", "emergency-icon"):
            pass  # skip broad — handled per file below

        if t != orig:
            path.write_text(t, encoding="utf-8")
            print("icon-emoji pass", path.name)


if __name__ == "__main__":
    main()
