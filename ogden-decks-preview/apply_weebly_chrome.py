#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
SKIP = {'404.html','form-submissions.html','leave-request.html','material-leads.html','receipt-submission-form.html','re-imbursement-of-expense.html','expense-reimbursement.html','time-clock-correction.html','confirmation.html'}
HEADER = '''<div class="top-strip"><div class="wrap top-row"><span>Ogden, Utah Deck Builder</span><a href="tel:+18015289807">Call 801-528-9807</a></div></div><header class="site-header"><div class="logo-row wrap"><a class="logo" href="/"><img src="/uploads/5/6/0/8/56087945/published/logo-8-1.png" alt="Ogden Decks"></a></div><nav class="nav" aria-label="Primary"><div class="wrap nav-inner"><a href="/">HOME</a><a href="/about-us.html">ABOUT US</a><a href="/services-we-offer.html">SERVICES</a><a href="/deck-project-gallery.html">GALLERY</a><a href="/service-area-deck-building.html">SERVICE AREAS</a><a href="/blog/">BLOG</a><a href="/contact-us.html">CONTACT</a></div></nav></header>'''
FOOTER = '''<footer class="footer old-footer"><div class="wrap footer-grid"><div><h2>OGDEN DECKS</h2><p>Crafting Exceptional Outdoor Spaces</p><p>190 W 33rd St<br>Ogden, UT 84401</p><p>Phone: <a href="tel:+18015289807">(801) 528-9807</a><br>Email: <a href="mailto:ogdendecks@gmail.com">ogdendecks@gmail.com</a></p></div><div><h2>SERVICE AREAS</h2><p>Proudly serving Ogden and surrounding areas throughout Northern Utah, including Ogden, Weber County, Pleasant View, North Ogden, South Ogden, Roy, Clinton, Layton, Syracuse, Eden, Huntsville and surrounding communities.</p></div><div><h2>QUICK LINKS</h2><p><a href="/services-we-offer.html">Services</a><br><a href="/deck-project-gallery.html">Gallery</a><br><a href="/about-us.html">About Us</a><br><a href="/contact-us.html">Contact</a><br><a href="/free-estimate.html">Free Estimate</a></p></div></div><div class="copyright">© Ogden Decks · Northern Utah Deck Builder</div></footer>'''

def transform(path: Path) -> bool:
    if path.name in SKIP or path.name == 'index.html' and path.parent == ROOT:
        return False
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text
    text = re.sub(r'<header\b[\s\S]*?</header>', HEADER, text, count=1, flags=re.I)
    if '<header' not in original.lower():
        text = re.sub(r'<body([^>]*)>', r'<body\1>' + HEADER, text, count=1, flags=re.I)
    text = re.sub(r'<footer\b[\s\S]*?</footer>', FOOTER, text, count=1, flags=re.I)
    if '<footer' not in original.lower():
        text = re.sub(r'</body>', FOOTER + '</body>', text, count=1, flags=re.I)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def main():
    changed = sum(1 for p in ROOT.rglob('*.html') if transform(p))
    print(f'Applied Weebly-style shared chrome to {changed} pages')

if __name__ == '__main__':
    main()
