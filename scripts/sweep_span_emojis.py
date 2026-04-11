# -*- coding: utf-8 -*-
"""Replace emoji-only content inside common span/div tags with neutral SVG icon."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "website" / "templates" / "website"
FILES = [
    "audit.html",
    "emergency.html",
    "complex_service.html",
    "heating_preparation.html",
]

INC = "{% include 'website/partials/ui_icon.html' with name='circle-dot' w=24 h=24 %}"

# Any span/div with a single "emoji" run (incl. variation selectors & ZWJ) as only text child
EMOJI_RUN = re.compile(
    r"[\U0001F300-\U0001FAFF\u2600-\u27BF]"
    r"[\U0000FE00-\U0000FE0F\u200d\U0001F300-\U0001FAFF\u2600-\u27BF]*"
)


def sweep(text: str) -> str:
    # <span class="...">EMOJI</span>
    def span_repl(m):
        cls, content = m.group(1), m.group(2)
        if "include" in content or not EMOJI_RUN.search(content):
            return m.group(0)
        return f'<span class="{cls}">{INC}</span>'

    text = re.sub(
        r'<span class="([^"]+)">([^<]*)</span>',
        span_repl,
        text,
    )

    # <div class="timeline-icon">EMOJI</div> etc.
    def div_repl(m):
        cls, content = m.group(1), m.group(2)
        if "include" in content or not EMOJI_RUN.search(content):
            return m.group(0)
        return f'<div class="{cls}">{INC}</div>'

    text = re.sub(r'<div class="([^"]+)">([^<]*)</div>', div_repl, text)

    # <div class="cta-icon">EMOJI</div> already covered

    return text


def main():
    for name in FILES:
        p = ROOT / name
        if not p.exists():
            continue
        t = p.read_text(encoding="utf-8")
        t2 = sweep(t)
        if t2 != t:
            p.write_text(t2, encoding="utf-8")
            print("swept", name)


if __name__ == "__main__":
    main()
