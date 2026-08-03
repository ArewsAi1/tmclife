#!/usr/bin/env python3
from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
BASE = "https://www.ogdendecks.com"
EXCLUDED_NAMES = {
    "404.html",
    "confirmation.html",
    "form-submissions.html",
    "leave-request.html",
    "material-leads.html",
    "receipt-submission-form.html",
    "re-imbursement-of-expense.html",
    "expense-reimbursement.html",
    "time-clock-correction.html",
}


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-11].strip("/")
    return "/" + rel


def redirect_patterns() -> list[str]:
    redirect_file = ROOT / "_redirects"
    if not redirect_file.exists():
        return []
    patterns: list[str] = []
    for raw in redirect_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        source = line.split()[0]
        if source.startswith("/"):
            patterns.append(source)
    return patterns


def is_redirect_source(route: str, patterns: list[str]) -> bool:
    variants = {route, route.rstrip("/") or "/"}
    if route != "/" and not route.endswith(".html"):
        variants.add(route + "/")
    for pattern in patterns:
        glob = pattern.replace(":splat", "*")
        for variant in variants:
            if fnmatch.fnmatchcase(variant, glob):
                return True
    return False


def canonical(markup: str) -> str | None:
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        markup,
        flags=re.I,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            markup,
            flags=re.I,
        )
    return match.group(1).strip() if match else None


def main() -> None:
    patterns = redirect_patterns()
    urls: set[str] = set()

    for path in ROOT.rglob("*.html"):
        if path.name in EXCLUDED_NAMES:
            continue
        route = route_for(path)
        if is_redirect_source(route, patterns):
            continue
        markup = path.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+noindex', markup, flags=re.I):
            continue
        if re.search(r'<meta[^>]+content=["\'][^"\']*noindex', markup, flags=re.I):
            continue
        url = canonical(markup)
        if not url or not url.startswith(BASE):
            continue
        urls.add(url.rstrip("/") if url != BASE + "/" else url)

    ordered = sorted(urls, key=lambda value: (value != BASE + "/", value))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in ordered:
        lines.append(f"  <url><loc>{escape(url)}</loc></url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated sitemap.xml with {len(ordered)} unique indexable URLs")


if __name__ == "__main__":
    main()
