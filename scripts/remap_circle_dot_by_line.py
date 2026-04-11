# -*- coding: utf-8 -*-
from pathlib import Path

RULES = [
    ("mega-icon animate-clipboard", "clipboard-list"),
    ("mega-icon animate-document", "file-text"),
    ("mega-icon animate-money", "banknote"),
    ("mega-icon animate-law", "scale"),
    ("mega-icon animate-car", "car"),
    ("why-icon animate-documents", "clipboard-list"),
    ("why-icon animate-specialist", "users"),
    ("why-icon animate-wrench", "wrench"),
    ("icon animate-search", "search"),
    ("icon animate-tools", "wrench"),
    ("icon animate-folder", "file-text"),
    ("icon animate-star", "circle-check"),
    ("animate-check-doc", "circle-check"),
    ("animate-report", "pen-line"),
    ("animate-chart", "bar-chart-2"),
    ("animate-calendar", "calendar"),
    ("animate-task", "clipboard-list"),
    ("animate-kp", "banknote"),
    ("mega-emoji animate-compliance", "clipboard-list"),
    ("mega-emoji animate-savings", "banknote"),
    ("mega-emoji animate-medal", "circle-check"),
    ("icon animate-pulse", "alert-circle"),
    ("icon animate-team", "users"),
    ("icon animate-phone", "phone"),
    ("icon animate-car", "car"),
    ("icon animate-repair", "wrench"),
    ("icon animate-clean", "clipboard-list"),
    ("icon animate-check", "circle-check"),
    ("icon-emoji animate-water", "droplets"),
    ("icon-emoji animate-fire", "flame"),
    ("icon-emoji animate-lightning", "zap"),
    ("icon-emoji animate-wind", "wind"),
    ("icon-emoji animate-ambulance", "car"),
    ("system-icon animate-wrench", "wrench"),
    ("system-icon animate-bounce", "droplets"),
    ("system-icon animate-sway", "wind"),
    ("system-icon animate-flash", "zap"),
    ("service-icon animated-pressure", "wrench"),
    ("service-icon animated-wind", "wind"),
    ("service-icon animated-chemistry", "flask"),
    ("timeline-icon animated-diagnostic", "search"),
    ("timeline-icon animated-preparation", "wrench"),
    ("timeline-icon animated-execution", "zap"),
    ("timeline-icon animated-startup", "flame"),
    ("timeline-icon animated-completion", "circle-check"),
    ("object-icon animated-building", "building-2"),
    ("object-icon animated-office", "building-2"),
    ("object-icon animated-factory", "factory"),
    ("object-icon animated-hospital", "building-2"),
    ("object-icon animated-commercial", "building-2"),
    ("doc-icon-modern animated-document-ready", "clipboard-list"),
    ("doc-icon-modern animated-hydraulic", "droplets"),
    ("doc-icon-modern animated-cleaning", "clipboard-list"),
    ("doc-icon-modern animated-temperature", "thermometer"),
    ("doc-icon-modern animated-scheme", "bar-chart-2"),
    ("doc-icon-modern animated-moek", "building-2"),
    ("badge-icon animated-heating", "wrench"),
]


def remap_file(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        if "name='circle-dot'" in line:
            for needle, icon in RULES:
                if needle in line:
                    line = line.replace("name='circle-dot'", f"name='{icon}'", 1)
                    break
        out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    root = Path(__file__).resolve().parents[1] / "website" / "templates" / "website"
    for name in ("audit.html", "emergency.html", "heating_preparation.html"):
        p = root / name
        if p.exists():
            remap_file(p)
            print("remapped", name)

    p = root / "complex_service.html"
    t = p.read_text(encoding="utf-8")
    t = t.replace("badge-icon\">{% include", "badge-icon\">{% include", 0)
    t = t.replace(
        "<span class=\"badge-icon\">{% include 'website/partials/ui_icon.html' with name='circle-dot'",
        "<span class=\"badge-icon\">{% include 'website/partials/ui_icon.html' with name='wrench'",
        1,
    )
    t = t.replace(
        "sewage-systems\">\n                    <span class=\"pill-icon\">{% include 'website/partials/ui_icon.html' with name='circle-dot'",
        "sewage-systems\">\n                    <span class=\"pill-icon\">{% include 'website/partials/ui_icon.html' with name='droplets'",
        1,
    )
    t = t.replace(
        "ventilation-systems\">\n                    <span class=\"pill-icon\">{% include 'website/partials/ui_icon.html' with name='circle-dot'",
        "ventilation-systems\">\n                    <span class=\"pill-icon\">{% include 'website/partials/ui_icon.html' with name='wind'",
        1,
    )
    lines = t.splitlines()
    out = []
    for line in lines:
        if "name='circle-dot'" in line:
            for needle, icon in RULES:
                if needle in line:
                    line = line.replace("name='circle-dot'", f"name='{icon}'", 1)
                    break
            else:
                if "icon-emoji" in line:
                    line = line.replace("name='circle-dot'", "name='building-2'", 1)
        out.append(line)
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("remapped complex_service.html")


if __name__ == "__main__":
    main()
