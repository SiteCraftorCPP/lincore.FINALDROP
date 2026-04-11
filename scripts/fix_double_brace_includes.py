# -*- coding: utf-8 -*-
from pathlib import Path

root = Path(__file__).resolve().parents[1] / "website" / "templates"
for p in root.rglob("*.html"):
    t = p.read_text(encoding="utf-8")
    if "{%%" not in t and "%%}" not in t:
        continue
    t2 = t.replace("{%%", "{%").replace("%%}", "%}")
    if t2 != t:
        p.write_text(t2, encoding="utf-8")
        print("fixed", p.relative_to(root))
