#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen
import re
import sys

ROOT = Path('ogden-decks-preview')
HOSTS = {'www.ogdendecks.com', 'ogdendecks.com'}
PATTERN = re.compile(r'https?://(?:www\.)?ogdendecks\.com(/uploads/[^\"\'\s<>?#]+)(?:\?[^\"\'\s<>#]*)?', re.I)


def download(url: str, destination: Path) -> bool:
    if destination.exists() and destination.stat().st_size > 0:
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = Request(url, headers={'User-Agent': 'Mozilla/5.0 OgdenDecksMigration/1.0'})
    with urlopen(request, timeout=60) as response:
        data = response.read()
    if not data:
        raise RuntimeError(f'Empty download: {url}')
    destination.write_bytes(data)
    return True


def main() -> int:
    if not ROOT.exists():
        print(f'Missing {ROOT}', file=sys.stderr)
        return 1
    discovered = {}
    html_files = list(ROOT.rglob('*.html')) + list(ROOT.rglob('*.xml')) + list(ROOT.rglob('*.css'))
    for path in html_files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        for match in PATTERN.finditer(text):
            rel = unquote(match.group(1))
            discovered.setdefault(rel, f'https://www.ogdendecks.com{rel}')

    downloaded = 0
    failures = []
    for rel, url in sorted(discovered.items()):
        try:
            if download(url, ROOT / rel.lstrip('/')):
                downloaded += 1
        except Exception as exc:
            failures.append((url, str(exc)))

    rewritten = 0
    for path in html_files:
        text = path.read_text(encoding='utf-8', errors='ignore')
        updated = PATTERN.sub(lambda m: m.group(1), text)
        if updated != text:
            path.write_text(updated, encoding='utf-8')
            rewritten += 1

    print(f'Discovered: {len(discovered)}')
    print(f'Downloaded: {downloaded}')
    print(f'Rewritten files: {rewritten}')
    if failures:
        print('Failures:', file=sys.stderr)
        for url, error in failures:
            print(f'- {url}: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
