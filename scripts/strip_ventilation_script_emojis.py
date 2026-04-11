# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "partials" / "ventilation_scripts.html"
s = p.read_text(encoding="utf-8")
s2 = re.sub(
    r"[\U0001F000-\U0001FFFF\u2600-\u27BF]+(?:\u200d[\U0001F000-\U0001FFFF\u2600-\u27BF]+)*(?:\uFE0F)?",
    "",
    s,
)
# Explosion particles: visual dot instead of glyph
old = """        particle.textContent = '';
        particle.style.cssText = `"""
if "particle.textContent = '';" in s2 and "particle.style.cssText" in s2:
    s2 = s2.replace(
        "particle.textContent = '';\n        particle.style.cssText = `",
        "particle.textContent = '';\n        particle.style.width = '6px';\n        particle.style.height = '6px';\n        particle.style.borderRadius = '50%';\n        particle.style.background = 'rgba(99,102,241,0.85)';\n        particle.style.fontSize = '0';\n        particle.style.cssText = `",
        1,
    )
else:
    s2 = s2.replace(
        "particle.textContent = '';\n        particle.style.cssText = `",
        "particle.textContent = '';\n        particle.style.width = '6px';\n        particle.style.height = '6px';\n        particle.style.borderRadius = '50%';\n        particle.style.background = 'rgba(99,102,241,0.85)';\n        particle.style.fontSize = '0';\n        particle.style.cssText = `",
        1,
    )

p.write_text(s2, encoding="utf-8")
print("done", len(s), "->", len(s2))
