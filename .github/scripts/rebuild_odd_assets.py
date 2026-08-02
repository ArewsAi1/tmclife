from pathlib import Path
from urllib.parse import unquote
from PIL import Image
import os
import re

root = Path('odd-preview')
text_exts = {'.html', '.htm', '.css', '.js', '.json', '.xml', '.txt'}
image_exts = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg', '.ico'}
site_root_prefixes = ('uploads/', 'files/', 'images/', 'assets/')
conversion = {}

for src in list(root.rglob('*')):
    if not src.is_file() or src.suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
        continue
    rel = src.relative_to(root).as_posix()
    dst = src.with_suffix('.webp')
    try:
        with Image.open(src) as im:
            im.load()
            if max(im.size) > 1600:
                im.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
            if im.mode not in ('RGB', 'RGBA'):
                im = im.convert('RGBA' if 'transparency' in im.info else 'RGB')
            im.save(dst, 'WEBP', quality=72, method=6)
        conversion[rel] = dst.relative_to(root).as_posix()
        src.unlink()
    except Exception as exc:
        print('KEEP ORIGINAL', rel, exc)

text_files = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in text_exts]
for p in text_files:
    text = p.read_text(errors='ignore')
    original = text
    for old, new in conversion.items():
        for a, b in ((old, new), ('/' + old, '/' + new), (old.replace(' ', '%20'), new.replace(' ', '%20')), (('/' + old).replace(' ', '%20'), ('/' + new).replace(' ', '%20'))):
            text = text.replace(a, b)
    if text != original:
        p.write_text(text)

def norm_stem(path):
    stem = Path(path).stem.lower()
    stem = re.sub(r'_(orig|\d+)$', '', stem)
    return re.sub(r'[^a-z0-9]+', '-', stem).strip('-')

image_files = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in image_exts]
by_stem = {}
for p in image_files:
    by_stem.setdefault(norm_stem(p.name), []).append(p)

url_re = re.compile(r'''(?P<q>["'(=:\s])(?P<u>/?[^"'()\s]+?\.(?:webp|jpe?g|png|gif|svg|ico)(?:\?[^"'()\s]*)?)''', re.I)
repaired = [0]

def resolve_target(page, clean):
    if clean.startswith('/'):
        return root / clean.lstrip('/'), True
    if clean.startswith(site_root_prefixes):
        return root / clean, True
    return page.parent / clean, False

for p in text_files:
    text = p.read_text(errors='ignore')
    def replace(match):
        raw = match.group('u')
        clean = unquote(raw.split('?', 1)[0].split('#', 1)[0])
        decoded = clean.replace('&quot;', '').replace('&#34;', '')
        if decoded.startswith(('http://', 'https://', '//', 'data:')):
            return match.group(0)
        target, root_style = resolve_target(p, clean)
        if target.exists():
            return match.group(0)
        candidates = by_stem.get(norm_stem(clean), [])
        if not candidates:
            return match.group(0)
        candidate = sorted(candidates, key=lambda x: (0 if 'uploads' in x.parts else 1, len(x.as_posix())))[0]
        new = '/' + candidate.relative_to(root).as_posix() if root_style else os.path.relpath(candidate, p.parent).replace(os.sep, '/')
        repaired[0] += 1
        return match.group('q') + new
    updated = url_re.sub(replace, text)
    if updated != text:
        p.write_text(updated)

missing = []
for p in text_files:
    text = p.read_text(errors='ignore')
    for match in url_re.finditer(text):
        raw = match.group('u')
        clean = unquote(raw.split('?', 1)[0].split('#', 1)[0])
        decoded = clean.replace('&quot;', '').replace('&#34;', '')
        if decoded.startswith(('http://', 'https://', '//', 'data:')):
            continue
        target, _ = resolve_target(p, clean)
        if not target.exists():
            missing.append((p.relative_to(root).as_posix(), raw))

print('Converted images:', len(conversion))
print('Heuristic reference repairs:', repaired[0])
print('Missing local image references:', len(missing))
for item in missing[:100]:
    print('MISSING', item[0], '=>', item[1])
Path('/tmp/odd_missing_assets.txt').write_text('\n'.join(f'{a} => {b}' for a, b in missing))
if missing:
    raise SystemExit('Asset validation failed: local image references remain missing')
