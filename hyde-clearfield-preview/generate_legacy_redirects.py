#!/usr/bin/env python3
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re

ROOT = Path(__file__).parent
LIVE_SITEMAP = 'https://www.hydemedspaclearfield.com/sitemap.xml'
REDIRECTS = ROOT / '_redirects'


def local_paths():
    paths = {'/'}
    for p in ROOT.rglob('*.html'):
        rel = p.relative_to(ROOT).as_posix()
        if rel == 'index.html':
            paths.add('/')
        elif rel.endswith('/index.html'):
            paths.add('/' + rel[:-10].rstrip('/'))
        else:
            paths.add('/' + rel)
    return paths


def target(path):
    s = path.lower()
    if s == '/index.html': return '/'
    if s == '/blog.html' or s.startswith('/blog/'): return '/blog'
    if 'privacy' in s: return '/privacy-policy.html'
    if 'terms' in s: return '/terms.html'
    if 'contact' in s: return '/contact-us.html'
    if 'about' in s or 'provider' in s: return '/about-us.html'
    places = {
        'layton':'/layton-spa.html','syracuse':'/syracuse-spa.html','clinton':'/clinton-spa.html',
        'roy':'/roy-spa.html','sunset':'/sunset-spa.html','west-point':'/west-point-spa.html',
        'riverdale':'/riverdale-spa.html','west-haven':'/west-haven-spa.html','davis-county':'/davis-county-medical-spa.html'
    }
    for key, dest in places.items():
        if key in s: return dest
    if 'tattoo' in s: return '/tattoo-removal.html'
    if re.search(r'laser|hair-removal|full-body-laser|bikini-line-laser|back-and-chest-laser|leg-laser', s): return '/laserhairremoval.html'
    if re.search(r'botox|dysport|filler|sculptra|inject|pixie-tip', s): return '/botox.html'
    if 'wax' in s: return '/waxing.html'
    if re.search(r'lash|brow|microblad|ombre|powder|henna', s): return '/eyelashextensions.html'
    if re.search(r'massage|prenatal|stone|reflex|swedish|deep-tissue|sports-massage|couplesmassage|deeptissue', s): return '/massage.html'
    if re.search(r'facial|skin|peel|microneed|derma|ipl|glow|hydra|acne|carbon|retinol|oxygen|photo-rejuvenation|collagen|azelaic', s): return '/facials.html'
    if re.search(r'teeth|whitening', s): return '/teeth-whitening.html'
    if re.search(r'body|sculpt|cellulite|cupping|emsella|fat-reduction|gluteal', s): return '/body-sculpting-services.html'
    return '/services.html'


def main():
    existing = []
    if REDIRECTS.exists():
        existing = [line.strip() for line in REDIRECTS.read_text(encoding='utf-8').splitlines() if line.strip() and not line.startswith('# AUTO-GENERATED')]
    local = local_paths()
    generated = []
    try:
        req = Request(LIVE_SITEMAP, headers={'User-Agent':'HydeMigrationBot/1.0'})
        xml = urlopen(req, timeout=30).read().decode('utf-8', errors='replace')
        live = sorted(set(urlparse(u).path.rstrip('/') or '/' for u in re.findall(r'<loc>(.*?)</loc>', xml)))
        for path in live:
            if path in local:
                continue
            dest = target(path)
            if path != dest:
                generated.append(f'{path} {dest} 301')
    except Exception as exc:
        print(f'Warning: live sitemap unavailable; preserving existing redirects: {exc}')
    lines = []
    seen = set()
    for line in existing + generated:
        source = line.split()[0] if line.split() else ''
        if source and source not in seen:
            lines.append(line)
            seen.add(source)
    REDIRECTS.write_text('# AUTO-GENERATED LEGACY COVERAGE\n' + '\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Legacy redirect coverage: {len(lines)} rules ({len(generated)} generated from live sitemap)')

if __name__ == '__main__':
    main()
