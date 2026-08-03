#!/usr/bin/env python3
from pathlib import Path
import re
import sys
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parent
HOST = "www.hydemedspaclearfield.com"
errors = []
warnings = []


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


def local_path_exists(raw_url: str, routes: dict[str, Path]) -> bool:
    parsed = urlparse(raw_url)
    path = unquote(parsed.path or "/")
    if parsed.netloc and parsed.netloc != HOST:
        return True
    if path in routes:
        return True
    candidate = ROOT / path.lstrip("/")
    if candidate.is_file():
        return True
    if candidate.is_dir() and (candidate / "index.html").is_file():
        return True
    return False


html_files = [p for p in ROOT.rglob("*") if p.is_file() and is_html_document(p)]
routes = {route_for(p): p for p in html_files}
canonical_to_route = {}
indexable_routes = set()
title_to_route = {}

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
    description = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', html, re.I)
    canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', html, re.I)
    h1_count = len(re.findall(r"<h1\b", html, re.I))
    text_len = len(visible_text(html))

    if not title or not visible_text(title.group(1)):
        errors.append(f"{route}: missing title")
    else:
        title_text = visible_text(title.group(1))
        if title_text in title_to_route and title_to_route[title_text] != route:
            errors.append(f"duplicate title: {title_text} on {title_to_route[title_text]} and {route}")
        title_to_route[title_text] = route
        if len(title_text) > 70:
            warnings.append(f"{route}: long title ({len(title_text)} characters)")

    if not description or not description.group(1).strip():
        errors.append(f"{route}: missing meta description")
    else:
        desc_len = len(description.group(1).strip())
        if desc_len < 70:
            warnings.append(f"{route}: short meta description ({desc_len} characters)")
        if desc_len > 180:
            warnings.append(f"{route}: long meta description ({desc_len} characters)")

    if h1_count != 1:
        errors.append(f"{route}: expected 1 H1, found {h1_count}")
    if not canonical:
        errors.append(f"{route}: missing canonical")
    else:
        url = canonical.group(1)
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != HOST:
            errors.append(f"{route}: invalid canonical host {url}")
        expected_path = route
        if parsed.path.rstrip("/") != expected_path.rstrip("/"):
            errors.append(f"{route}: canonical path mismatch {parsed.path}")
        if url in canonical_to_route and canonical_to_route[url] != route:
            errors.append(f"duplicate canonical {url}: {canonical_to_route[url]} and {route}")
        canonical_to_route[url] = route

    threshold = 500 if route in {"/privacy-policy.html", "/terms.html"} else 700
    if not noindex and text_len < threshold:
        errors.append(f"{route}: thin visible text ({text_len} < {threshold})")
    if not noindex:
        indexable_routes.add(route)

    for tag in re.findall(r"<img\b[^>]*>", html, re.I):
        src_match = re.search(r'\bsrc=["\']([^"\']+)', tag, re.I)
        alt_match = re.search(r'\balt=["\']([^"\']*)', tag, re.I)
        if not src_match:
            errors.append(f"{route}: image missing src")
            continue
        src = src_match.group(1)
        if not alt_match:
            errors.append(f"{route}: image missing alt: {src}")
        if not local_path_exists(src, routes):
            errors.append(f"{route}: missing image asset {src}")
        if not re.search(r'\bwidth=["\']?\d+', tag, re.I) or not re.search(r'\bheight=["\']?\d+', tag, re.I):
            warnings.append(f"{route}: image missing explicit dimensions: {src}")

    for attr, raw_url in re.findall(r"\b(href|src)=[\"']([^\"']+)", html, re.I):
        if raw_url.startswith(("mailto:", "tel:", "javascript:", "data:", "#")):
            continue
        parsed = urlparse(raw_url)
        if parsed.scheme == "http" and parsed.netloc == HOST:
            errors.append(f"{route}: insecure internal URL {raw_url}")
        if parsed.scheme in {"http", "https"} and parsed.netloc not in {"", HOST}:
            continue
        if not local_path_exists(raw_url, routes):
            errors.append(f"{route}: broken internal {attr} {raw_url}")

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
redirect_map = {}
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
        redirect_map[source] = target
        if target.startswith("https://"):
            continue
        target_path = target.split("?", 1)[0].split("#", 1)[0]
        if "*" in target_path or ":" in target_path:
            continue
        if target_path not in routes and target_path not in {"/blog", "/"}:
            errors.append(f"_redirects:{line_no}: missing target {target}")

for source, target in redirect_map.items():
    target_path = target.split("?", 1)[0].split("#", 1)[0]
    if target_path in redirect_map and "*" not in source and ":" not in source:
        errors.append(f"redirect chain: {source} -> {target_path} -> {redirect_map[target_path]}")

robots_path = ROOT / "robots.txt"
if not robots_path.exists():
    errors.append("missing robots.txt")
else:
    robots = robots_path.read_text(encoding="utf-8", errors="replace")
    if "Sitemap: https://www.hydemedspaclearfield.com/sitemap.xml" not in robots:
        errors.append("robots.txt missing production sitemap reference")
    if "Disallow: /" not in robots:
        errors.append("staging robots.txt must block crawling before cutover")

for required in ["styles.css", "_headers", "_redirects", "robots.txt", "sitemap.xml"]:
    if not (ROOT / required).exists():
        errors.append(f"missing required file {required}")

if errors:
    print("SITE VALIDATION FAILED")
    for error in sorted(set(errors)):
        print(f"- {error}")
    if warnings:
        print("WARNINGS")
        for warning in sorted(set(warnings)):
            print(f"- {warning}")
    sys.exit(1)

print(f"SITE VALIDATION PASSED: {len(html_files)} HTML documents, {len(sitemap_urls)} sitemap URLs, {len(redirect_sources)} redirect rules, zero redirect chains")
if warnings:
    print(f"SITE VALIDATION WARNINGS: {len(set(warnings))}")
    for warning in sorted(set(warnings)):
        print(f"- {warning}")
