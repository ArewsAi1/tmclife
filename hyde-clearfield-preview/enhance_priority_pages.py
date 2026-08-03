#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOK = 'https://dashboard.boulevard.io/booking/businesses/9bf461e1-913f-4005-9f23-ac457d7a3747/widget#/locations'
BASE = 'https://www.hydemedspaclearfield.com'
NAV = f'''<header class="site-header"><div class="wrap header-row"><a class="logo" href="/">Hyde Beauty & Wellness</a><nav><a href="/services.html">Services</a><a href="/laserhairremoval.html">Laser</a><a href="/botox.html">Injectables</a><a href="/facials.html">Facials</a><a href="/blog">Blog</a><a class="btn" href="{BOOK}">Book Online</a></nav></div></header>'''
FOOT = '''<footer><div class="wrap"><p>Hyde Beauty & Wellness Clearfield · 189 S State St #160, Clearfield, UT 84015 · <a href="tel:+13854215854">(385) 421-5854</a></p><p><a href="/privacy-policy.html">Privacy</a> · <a href="/terms.html">Terms</a></p><small>Educational information only. Results and eligibility vary.</small></div></footer>'''

def shell(title, description, canonical, h1, intro, sections):
    body = ''.join(f'<section class="section{(" alt" if i % 2 else "")}"><div class="wrap"><h2>{heading}</h2>{content}</div></section>' for i, (heading, content) in enumerate(sections))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{description}"><link rel="canonical" href="{BASE}/{canonical}"><link rel="stylesheet" href="/styles.css"></head><body>{NAV}<main><section class="hero"><div class="wrap"><p>Hyde Beauty & Wellness Clearfield</p><h1>{h1}</h1><p>{intro}</p><div class="actions"><a class="btn" href="{BOOK}">Book Online</a><a class="btn secondary" href="tel:+13854215854">Call (385) 421-5854</a></div></div></section>{body}<section class="cta"><div class="wrap"><h2>Schedule in Clearfield</h2><p>Review current availability and service options through Hyde's Boulevard booking system.</p><a class="btn" href="{BOOK}">View Availability</a></div></section></main>{FOOT}</body></html>'''

whitening = shell(
    'Teeth Whitening Clearfield UT | Hyde Beauty & Wellness',
    'Learn about professional in-office and take-home teeth whitening options at Hyde Beauty & Wellness in Clearfield, Utah.',
    'teethwhitening.html',
    'Professional Teeth Whitening in Clearfield',
    'Cosmetic whitening options are planned around your starting shade, sensitivity history, existing dental work and the result you hope to achieve.',
    [
        ('Whitening Options', '<p>Hyde may offer professional in-office whitening and take-home whitening options based on current availability and individual screening. In-office treatment is designed for clients seeking a supervised appointment, while take-home options may support a more gradual schedule.</p><p>Current products, treatment times and pricing should be confirmed directly through the Clearfield location or Boulevard booking page.</p>'),
        ('Before Your Appointment', '<p>Tell the provider about tooth sensitivity, recent dental treatment, gum irritation, cavities, crowns, veneers or bonding. Cosmetic whitening changes natural tooth structure differently than restorations, so an individual review is important before treatment.</p>'),
        ('Aftercare and Expectations', '<p>Temporary sensitivity can occur. Follow the provider\'s instructions regarding food, drinks, oral-care products and timing after the appointment. Results vary with starting shade, stain type, habits and the whitening option selected.</p>'),
        ('Related Services', '<p><a href="/services.html">View all services</a> · <a href="/contact-us.html">Contact Hyde Clearfield</a> · <a href="/clearfield-spa.html">Clearfield location details</a></p>')
    ]
)
(ROOT / 'teethwhitening.html').write_text(whitening, encoding='utf-8')

body = shell(
    'Body Services Clearfield UT | Hyde Beauty & Wellness',
    'Explore consultation-based body services at Hyde Beauty & Wellness in Clearfield, Utah, with candidacy and realistic outcome planning.',
    'body-sculpting-services.html',
    'Body Services and Contouring Consultations',
    'Body-focused services begin with a consultation to review goals, health history, treatment area, comfort, expected maintenance and realistic outcomes.',
    [
        ('Consultation First', '<p>Available technologies and service names can change. The provider will explain which current options are offered at Hyde Clearfield, what each service is intended to address, and whether the treatment is appropriate for the individual.</p>'),
        ('What to Discuss', '<p>Share relevant medical history, implanted devices, pregnancy status, recent procedures, medications, skin conditions and prior body treatments. These details may affect candidacy or timing.</p>'),
        ('Realistic Expectations', '<p>Non-surgical body services are not substitutes for weight-loss treatment or surgery. Outcomes, number of sessions and maintenance vary by service and client. The consultation should cover expected temporary effects, aftercare and when results may become visible.</p>'),
        ('Related Services', '<p><a href="/wellness.html">Wellness services</a> · <a href="/services.html">All services</a> · <a href="/meet-our-service-providers-clearfield.html">Meet providers</a></p>')
    ]
)
(ROOT / 'body-sculpting-services.html').write_text(body, encoding='utf-8')

print('Enhanced teeth whitening and body services pages')
