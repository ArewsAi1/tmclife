#!/usr/bin/env python3
from pathlib import Path
from html import escape
import re
ROOT=Path(__file__).parent
BASE='https://www.hydemedspaclearfield.com'
BOOK='https://dashboard.boulevard.io/booking/businesses/9bf461e1-913f-4005-9f23-ac457d7a3747/widget#/locations'
LOCATIONS={
'layton-spa.html':('Medical Spa Near Layton, Utah','Layton clients are a short drive from Hyde Beauty & Wellness Clearfield for injectables, laser hair removal, facials, waxing, lashes and massage. Appointment planning considers the selected service, preparation and any expected downtime.'),
'spa-syracuse-utah.html':('Medical Spa Near Syracuse, Utah','Hyde Clearfield serves Syracuse-area clients seeking consultation-based aesthetic and wellness services. Online booking makes it easy to review current availability before traveling to the Clearfield location.'),
'spa-clinton-utah.html':('Medical Spa Near Clinton, Utah','Clients from Clinton can access a broad selection of skincare, beauty, massage and medical-aesthetic services at the nearby Clearfield practice.'),
'spa-roy-utah.html':('Medical Spa Near Roy, Utah','Hyde Beauty & Wellness Clearfield welcomes Roy-area clients for personalized treatments selected around individual goals, history and provider assessment.'),
'spa-sunset-utah.html':('Medical Spa Near Sunset, Utah','The Clearfield spa is conveniently located for Sunset residents looking for coordinated skincare, laser, waxing, lash, massage and injectable services.'),
'spa-west-point-utah.html':('Medical Spa Near West Point, Utah','West Point clients can book consultations and services at Hyde Clearfield, with online availability through the established Boulevard booking system.'),
'spa-riverdale-utah.html':('Medical Spa Near Riverdale, Utah','Hyde Clearfield provides Riverdale-area clients with a nearby option for aesthetic treatments, professional skincare and beauty services.'),
'spa-west-haven-utah.html':('Medical Spa Near West Haven, Utah','West Haven clients can visit the Clearfield location for treatment planning, skincare, hair reduction, waxing, massage and lash services.'),
'davis-county-medical-spa.html':('Medical Spa Serving Davis County, Utah','Hyde Beauty & Wellness Clearfield serves communities throughout northern Davis County with personalized aesthetic, skincare and wellness services.')
}
NAV='<header class="site-header"><div class="wrap header-row"><a class="logo" href="/">Hyde Beauty & Wellness</a><nav><a href="/services.html">Services</a><a href="/clearfield-spa.html">Clearfield</a><a href="/blog">Blog</a><a class="btn" href="'+BOOK+'">Book Online</a></nav></div></header>'
FOOT='<footer><div class="wrap"><p>Hyde Beauty & Wellness Clearfield · 189 S State St #160, Clearfield, UT 84015 · <a href="tel:+13854215854">(385) 421-5854</a></p><small>Individual consultation required. Results and eligibility vary.</small></div></footer>'
for fn,(h1,desc) in LOCATIONS.items():
 city=h1.replace('Medical Spa Near ','').replace('Medical Spa Serving ','').replace(', Utah','')
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(h1)} | Hyde Beauty & Wellness</title><meta name="description" content="{escape(desc)}"><link rel="canonical" href="{BASE}/{fn}"><link rel="stylesheet" href="/styles.css"></head><body>{NAV}<main><section class="hero"><div class="wrap"><p>Serving {escape(city)}</p><h1>{escape(h1)}</h1><p>{escape(desc)}</p><a class="btn" href="{BOOK}">Book at Hyde Clearfield</a></div></section><section class="section"><div class="wrap"><h2>Services Available Through Hyde Clearfield</h2><p>Clients can explore laser hair removal, Botox and Dysport, lip filler, facials, microneedling, chemical peels, waxing, lashes and massage. Service availability and provider schedules are shown in the online booking system.</p><h2>Planning Your Visit</h2><p>The spa is located at 189 S State St #160 in Clearfield. Review preparation instructions for your selected treatment and contact the office when medical history, recent procedures or medication changes may affect eligibility.</p><p><a href="/services.html">Explore all services</a> · <a href="/meet-our-service-providers-clearfield.html">Meet the provider team</a> · <a href="/contact-us.html">Contact Hyde Clearfield</a></p></div></section></main>{FOOT}</body></html>'''
 (ROOT/fn).write_text(html,encoding='utf-8')
site=ROOT/'sitemap.xml'
xml=site.read_text(encoding='utf-8')
insert=''.join(f'<url><loc>{BASE}/{fn}</loc></url>' for fn in sorted(LOCATIONS))
xml=xml.replace('</urlset>',insert+'</urlset>')
site.write_text(xml,encoding='utf-8')
print(f'Generated {len(LOCATIONS)} service-area pages')
