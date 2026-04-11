# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "static" / "css" / "styles.css"
s = p.read_text(encoding="utf-8")
s2 = re.sub(
    r"[\U0001F000-\U0001FFFF\u2600-\u27BF\uFE0F]+(?:\u200d[\U0001F000-\U0001FFFF\u2600-\u27BF]+)*(?:\uFE0F)?",
    "",
    s,
)
p.write_text(s2, encoding="utf-8")
print("stripped comments etc", len(s), len(s2))
