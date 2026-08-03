#!/usr/bin/env python3
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
HOST = "www.hydemedspaclearfield.com"
errors = []


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10].strip("/")
    return "/" + rel


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style\b[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html).strip()


def is_html_document(path: Path) -> bool:
    if path.suffix.lower() == ".html":
        return True
    if path.parent.name == "blog" and not path.suffix:
        try:
            return "<html" in path.read_text(encoding="utf-8", errors="replace").lower()
        except OSError:
            return False
    return False

html_files = [p for p in ROOT.rglob("*") if p.is_file() and is_html_document(p)]
routes = {route_for(p): p for p in html_files}
canonical_to_route = {}
indexable_routes = set()

for path in html_files:
    route = route_for(path)
    html = path.read_text(encoding="utf-8", errors="replace")
    robots = re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)', html, re.I)
    noindex = bool(robots and "noindex" in robots.group(1).lower())
    if route == "/404.html":
        if not noindex:
            errors.append("404.html must be noindex")
        continue

    title = re.search(r"<title[^>]*>([\s\S]*?)</title>", html, re.I)
    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html, re.I)
    h1_count = len(re.findall(r"<h1\b", html, re.I))
    text_len = len(visible_text(html))

    if not title or not visible_text(title.group(1)):
        errors.append(f"{route}: missing title")
    if h1_count != 1:
        errors.append(f"{route}: expected 1 H1, found {h1_count}")
    if not canonical:
        errors.append(f"{route}: missing canonical")
    else:
        url = canonical.group(1)
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != HOST:
            errors.append(f"{route}: invalid canonical host {url}")
        if url in canonical_to_route and canonical_to_route[url] != route:
            errors.append(f"duplicate canonical {url}: {canonical_to_route[url]} and {route}")
        canonical_to_route[url] = route

    threshold = 500 if route in {"/privacy-policy.html", "/terms.html"} else 700
    if not noindex and text_len < threshold:
        errors.append(f"{route}: thin visible text ({text_len} < {threshold})")
    if not noindex:
        indexable_routes.add(route)

sitemap_path = ROOT / "sitemap.xml"
if not sitemap_path.exists():
    errors.append("missing sitemap.xml")
    sitemap_urls = []
else:
    xml = sitemap_path.read_text(encoding="utf-8", errors="replace")
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", xml)
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("sitemap contains duplicate URLs")
    for url in sitemap_urls:
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != HOST:
            errors.append(f"sitemap invalid host: {url}")
        route = parsed.path or "/"
        if route not in indexable_routes:
            errors.append(f"sitemap URL has no indexable HTML destination: {route}")

redirect_path = ROOT / "_redirects"
redirect_sources = set()
if redirect_path.exists():
    for line_no, raw in enumerate(redirect_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            errors.append(f"_redirects:{line_no}: malformed rule")
            continue
        source, target = parts[0], parts[1]
        if source in redirect_sources:
            errors.append(f"_redirects:{line_no}: duplicate source {source}")
        redirect_sources.add(source)
        if target.startswith("https://"):
            continue
        target_path = target.split("?", 1)[0].split("#", 1)[0]
        if "*" in target_path or ":" in target_path:
            continue
        if target_path not in routes and target_path not in {"/blog", "/"}:
            errors.append(f"_redirects:{line_no}: missing target {target}")

robots_path = ROOT / "robots.txt"
if not robots_path.exists():
    errors.append("missing robots.txt")
else:
    robots = robots_path.read_text(encoding="utf-8", errors="replace")
    if "Sitemap: https://www.hydemedspaclearfield.com/sitemap.xml" not in robots:
        errors.append("robots.txt missing production sitemap reference")

if errors:
    print("SITE VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print(f"SITE VALIDATION PASSED: {len(html_files)} HTML documents, {len(sitemap_urls)} sitemap URLs, {len(redirect_sources)} redirect rules")
