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

pages = {}
pages['teethwhitening.html'] = shell(
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
pages['body-sculpting-services.html'] = shell(
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
pages['ipl-photofacial.html'] = shell(
    'IPL Photofacial Clearfield UT | Hyde Beauty & Wellness',
    'Learn how IPL photofacial consultations at Hyde Beauty & Wellness Clearfield address appropriate pigment and redness concerns.',
    'ipl-photofacial.html',
    'IPL Photofacial in Clearfield',
    'Intense pulsed light treatments use filtered light to address selected visible pigment and redness concerns when the client and condition are appropriate for treatment.',
    [
        ('Concerns Commonly Discussed', '<p>Consultations may cover visible sun-related discoloration, freckles, age spots, uneven tone, redness and selected vascular-looking concerns. IPL is not appropriate for every skin type or every pigment concern, so provider assessment is essential.</p>'),
        ('Before Treatment', '<p>Share recent sun exposure, tanning, photosensitizing medications, active skin conditions, pregnancy status, prior light or laser treatments and current skincare products. The provider may recommend changing products or postponing treatment.</p>'),
        ('Treatment Series and Aftercare', '<p>Some clients may need more than one session. Temporary redness, warmth or darkening of treated pigment can occur. Follow sun-protection and skincare instructions closely, and do not pick or scrub treated areas.</p>'),
        ('Related Skin Services', '<p><a href="/facials.html">Facials and skincare</a> · <a href="/microneedling.html">Microneedling</a> · <a href="/chemicalpeel.html">Chemical peels</a></p>')
    ]
)
pages['jawline-botox.html'] = shell(
    'Jawline and Masseter Botox Clearfield UT | Hyde Beauty & Wellness',
    'Consult with a qualified Hyde Clearfield provider about masseter and jawline Botox goals, candidacy, risks and expected timing.',
    'jawline-botox.html',
    'Jawline and Masseter Botox Consultation',
    'Masseter treatment requires an individual facial and functional assessment because muscle size, bite concerns, facial balance and treatment goals vary widely.',
    [
        ('Why the Masseter Is Assessed', '<p>The masseter is a strong chewing muscle at the side of the jaw. A provider may evaluate muscle activity, facial width, symmetry, tenderness and the client\'s goals before deciding whether neuromodulator treatment is appropriate.</p>'),
        ('Medical and Dental Considerations', '<p>Tell the provider about jaw pain, grinding, dental treatment, swallowing concerns, facial weakness, prior injections, medications and medical conditions. Cosmetic treatment does not replace evaluation by a dentist or medical professional for pain or bite disorders.</p>'),
        ('Timing and Expectations', '<p>Neuromodulator effects develop gradually. Dose, placement, response and duration vary. Possible effects and risks should be reviewed before treatment, including temporary weakness or changes in chewing sensation.</p>'),
        ('Related Injectable Services', '<p><a href="/botox.html">Botox and Dysport guide</a> · <a href="/forehead-botox.html">Forehead Botox</a> · <a href="/natural-lip-filler.html">Natural-looking lip filler</a></p>')
    ]
)

for filename, html in pages.items():
    (ROOT / filename).write_text(html, encoding='utf-8')

print(f'Enhanced {len(pages)} priority treatment pages')
