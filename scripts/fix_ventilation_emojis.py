# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(__file__).resolve().parents[1] / "website" / "templates" / "website" / "ventilation.html"
INC = "{%% include 'website/partials/ui_icon.html' with name='%s' %s %%}"
t = p.read_text(encoding="utf-8")

t = re.sub(
    r'<span class="mega-feature-emoji">[^<]*</span>',
    '<span class="mega-feature-marker" aria-hidden="true"></span>',
    t,
)

t = re.sub(
    r'<span class="feature-emoji">[^<]*</span>',
    '<span class="feature-marker" aria-hidden="true"></span>',
    t,
)

# Hero badge: any non-ASCII in badge-icon span
t = re.sub(
    r'(<span class="badge-icon animated-maintenance">)[^<]*?(</span>)',
    r"\1" + INC % ("wind", "svg_class='badge-icon-svg' w=22 h=22") + r"\2",
    t,
    count=1,
)

t = re.sub(
    r'<span class="icon animated-maintenance">[^<]*</span>',
    f'<span class="icon animated-maintenance">{INC % ("wrench", "w=40 h=40")}</span>',
    t,
    count=1,
)

t = re.sub(
    r'<span class="icon animated-repair">[^<]*</span>',
    f'<span class="icon animated-repair">{INC % ("zap", "w=40 h=40")}</span>',
    t,
    count=1,
)

t = re.sub(
    r'<span class="icon animated-control">[^<]*</span>',
    f'<span class="icon animated-control">{INC % ("bar-chart-2", "w=40 h=40")}</span>',
    t,
    count=1,
)

t = re.sub(
    r'<span class="icon animated-specialist">[^<]*</span>',
    f'<span class="icon animated-specialist">{INC % ("circle-check", "w=40 h=40")}</span>',
    t,
    count=1,
)

# mega-service-icon first maintenance block
t = re.sub(
    r'<span class="mega-service-icon animated-maintenance">[^<]*</span>',
    f'<span class="mega-service-icon animated-maintenance">{INC % ("calendar", "w=36 h=36")}</span>',
    t,
    count=1,
)

# remaining mega-service-icon animated-season (refresh, sun, snowflake) — order in file
for name in ("refresh-cw", "sun", "snowflake"):
    t = re.sub(
        r'<span class="mega-service-icon animated-season">[^<]*</span>',
        f'<span class="mega-service-icon animated-season">{INC % (name, "w=36 h=36")}</span>',
        t,
        count=1,
    )

# timeline icons
for name in ("wrench", "alert-circle"):
    t = re.sub(
        r'<div class="timeline-icon animated-repair">[^<]*</div>',
        f'<div class="timeline-icon animated-repair">{INC % (name, "w=32 h=32")}</div>',
        t,
        count=1,
    )

t = re.sub(
    r'<div class="timeline-icon animated-emergency">[^<]*</div>',
    f'<div class="timeline-icon animated-emergency">{INC % ("alert-circle", "w=32 h=32")}</div>',
    t,
    count=1,
)

# ultra-control-icon
t = re.sub(
    r'<span class="ultra-control-icon animated-monitoring">[^<]*</span>',
    f'<span class="ultra-control-icon animated-monitoring">{INC % ("bar-chart-2", "w=32 h=32")}</span>',
    t,
    count=1,
)
t = re.sub(
    r'<span class="ultra-control-icon animated-testing">[^<]*</span>',
    f'<span class="ultra-control-icon animated-testing">{INC % ("cog", "w=32 h=32")}</span>',
    t,
    count=1,
)

# advantage-icon-modern
adv = [
    ("animated-specialist", "target"),
    ("animated-equipment", "wrench"),
    ("animated-support", "clock"),
    ("animated-guarantee", "clipboard-list"),
    ("animated-price", "banknote"),
]
for anim, icon in adv:
    t = re.sub(
        rf'<span class="advantage-icon-modern {re.escape(anim)}">[^<]*</span>',
        f'<span class="advantage-icon-modern {anim}">{INC % (icon, "w=28 h=28")}</span>',
        t,
        count=1,
)

t = re.sub(
    r'<span class="icon animate-team">[^<]*</span>',
    f'<span class="icon animate-team">{INC % ("users", "w=40 h=40")}</span>',
    t,
    count=1,
)

# CTA block
t = re.sub(
    r'<span class="cta-icon ventilation-icon animated-ventilation-pulse">[^<]*</span>',
    f'<span class="cta-icon ventilation-icon animated-ventilation-pulse">{INC % ("wind", "w=36 h=36")}</span>',
    t,
    count=1,
)

# Fix hero buttons: ensure btn-icon wrapper
t = t.replace(
    "<span class=\"btn-text\">Оставить заявку</span>\n                        {% include",
    "<span class=\"btn-text\">Оставить заявку</span>\n                        <span class=\"btn-icon\">{% include",
    1,
)
t = t.replace(
    "with name='clipboard-list' w=20 h=20 %}\n                    </button>",
    "with name='pen-line' w=20 h=20 %}</span>\n                    </button>",
    1,
)
t = t.replace(
    "<span class=\"btn-text\">Заказать звонок специалиста</span>\n                        {% include",
    "<span class=\"btn-text\">Заказать звонок специалиста</span>\n                        <span class=\"btn-icon\">{% include",
    1,
)
t = t.replace(
    "with name='phone' w=20 h=20 %}\n                    </button>",
    "with name='phone' w=20 h=20 %}</span>\n                    </button>",
    1,
)

# Footer CTA buttons
t = re.sub(
    r'(<span class="btn-text">Оставить заявку</span>\s*){% include \'website/partials/ui_icon.html\' with name=\'clipboard-list\' w=20 h=20 %}',
    r"\1<span class=\"btn-icon\">" + INC % ("pen-line", "w=20 h=20") + "</span>",
    t,
)
t = re.sub(
    r'(<span class="btn-text">Заказать звонок специалиста</span>\s*){% include \'website/partials/ui_icon.html\' with name=\'phone\' w=20 h=20 %}',
    r"\1<span class=\"btn-icon\">" + INC % ("phone", "w=20 h=20") + "</span>",
    t,
)

p.write_text(t, encoding="utf-8")
print("OK", p)
