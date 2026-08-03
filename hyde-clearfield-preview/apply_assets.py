#!/usr/bin/env python3
from pathlib import Path

root = Path(__file__).resolve().parent
index = root / "index.html"
html = index.read_text(encoding="utf-8")
html = html.replace("/assets/hyde-clearfield-hero.svg", "/assets/hyde-clearfield-original.webp")
html = html.replace(
    'alt="Hyde Beauty and Wellness Clearfield aesthetic and wellness services"',
    'alt="Hyde Beauty and Wellness original brand photography" width="800" height="534" loading="eager" fetchpriority="high"'
)
index.write_text(html, encoding="utf-8")
print("Applied locally hosted Hyde Clearfield imagery and social metadata")
