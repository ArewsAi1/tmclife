#!/usr/bin/env python3
from __future__ import annotations
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SKIP_NAMES = {
    '404.html','leave-request.html','material-leads.html','receipt-submission-form.html',
    're-imbursement-of-expense.html','expense-reimbursement.html','time-clock-correction.html',
    'form-submissions.html','confirmation.html'
}
THRESHOLD = 850


def visible_text(markup: str) -> str:
    text = re.sub(r'<script[\s\S]*?</script>', ' ', markup, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', ' ', text, flags=re.I)
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', html.unescape(text)).strip()


def get_heading(markup: str, path: Path) -> str:
    for tag in ('h1', 'title'):
        m = re.search(fr'<{tag}[^>]*>([\s\S]*?)</{tag}>', markup, flags=re.I)
        if m:
            value = re.sub(r'<[^>]+>', ' ', m.group(1))
            value = re.sub(r'\s+', ' ', html.unescape(value)).strip()
            value = value.split('|')[0].strip()
            if value:
                return value
    return path.stem.replace('-', ' ').title()


def topic_copy(key: str) -> tuple[str, str, str, list[tuple[str,str]]]:
    k = key.lower()
    if any(x in k for x in ('repair','restore','refinish','resurface','maintenance','rot','damaged')):
        return (
            'Planning the Correct Repair Scope',
            'A durable repair begins with identifying whether the problem is limited to surface boards or extends into stairs, railing, joists, beams, posts, footings or the connection to the home. Cosmetic replacement without checking the supporting structure can hide the conditions that caused the damage.',
            'The recommended scope depends on age, moisture exposure, movement, fastener condition, access and whether replacement materials can be integrated safely. Photos from above and below the deck help establish the starting point, but an on-site inspection may still be needed.',
            [('/deck-repair-services.html','Deck repair services'),('/deck-inspection-services.html','Deck inspections'),('/deck-replacement-services.html','Deck replacement')]
        )
    if any(x in k for x in ('pergola','shade','awning','covered','cabana','gazebo')):
        return (
            'Planning Shade and Weather Protection',
            'Shade structures should be planned around sun direction, rooflines, windows, doors, drainage, post locations and the way people move through the outdoor space. Attached and freestanding designs have different structural and waterproofing requirements.',
            'Wood pergolas, fixed covers and motorized louvered systems provide different levels of shade and weather protection. The best choice depends on desired coverage, maintenance, budget and whether the structure is being added to an existing deck or designed with a new one.',
            [('/pergola-installation.html','Pergola installation'),('/motorized-pergolas.html','Motorized pergolas'),('/custom-deck-shade-installation-in-ogden-ut.html','Custom deck shade')]
        )
    if any(x in k for x in ('rail','handrail','baluster','cable')):
        return (
            'Railing Safety, Layout and Material Selection',
            'Railing is both a safety system and a major visual element. Post spacing, blocking, stair transitions, gates, deck height and attachment conditions should be reviewed before selecting panels or rail profiles.',
            'Steel, aluminum, cable, composite and vinyl systems differ in sightlines, maintenance and installation requirements. Existing decks may need added blocking or structural corrections before a new railing system can be installed securely.',
            [('/ogden-decks-railing-options.html','Railing options'),('/deck-railing-repair-in-ogden-ut.html','Railing repair'),('/custom-welded-railing-ogden-ut.html','Custom welded railing')]
        )
    if any(x in k for x in ('trex','composite','timbertech','deckorators','fiberon','material','pvc','wood vs')):
        return (
            'Comparing Decking Materials',
            'Decking should be compared by more than initial board price. Color, surface temperature, traction, scratch visibility, warranty terms, fastening, fascia, availability and long-term maintenance all affect the finished project.',
            'Composite and PVC products reduce staining and sealing requirements, while wood offers a natural appearance and different repair options. Framing condition and joist spacing must also be compatible with the selected decking system.',
            [('/ogden-decks-decking-choices.html','Compare decking choices'),('/trex.html','Trex decking'),('/composite-deck-material-selection.html','Composite material selection')]
        )
    if any(x in k for x in ('cost','price','budget','financ','estimate','quote')):
        return (
            'What Changes Deck Project Pricing',
            'Square footage is only one part of a deck estimate. Height, demolition, access, framing, footings, stairs, railing, fascia, permits, drainage, material selection and site conditions can change the scope substantially.',
            'A useful estimate starts with approximate dimensions, property photos and a clear list of desired features. Comparing proposals is easier when each contractor is pricing the same materials, structure, railing and finish details.',
            [('/deck-financing-and-quotes.html','Financing and quotes'),('/free-estimate.html','Request an estimate'),('/deck-building.html','Deck construction')]
        )
    if any(x in k for x in ('hot tub','spa')):
        return (
            'Structural Planning for a Hot-Tub Deck',
            'Hot tubs create concentrated loads that usually require dedicated framing and support. Equipment access, electrical clearances, drainage, cover movement, steps and the finished height of the spa should be planned before construction.',
            'A hot tub may sit on a reinforced deck, on a separate pad beside the deck or partially recessed into the surrounding surface. Each approach changes access, framing and future serviceability.',
            [('/hot-tub-deck-design.html','Hot-tub deck design'),('/custom-hot-tub-deck-builder-in-ogden-ut.html','Custom hot-tub decks'),('/hot-tub-deck-removal-disposal-in-ogden-ut.html','Hot-tub removal')]
        )
    if any(x in k for x in ('patio','concrete','pool','fire pit','outdoor kitchen','entertain')):
        return (
            'Connecting the Outdoor-Living Elements',
            'Decks, patios, pools, cooking areas and fire features work best when circulation, elevations, drainage and safety clearances are planned together. Door locations and transitions into the yard often determine the most practical layout.',
            'The project should separate cooking, seating and travel paths while preserving access for maintenance and utilities. Material transitions and edge details are important for both appearance and long-term performance.',
            [('/outdoor-entertainment-spaces.html','Outdoor entertainment spaces'),('/deck-and-patio-combo.html','Deck and patio combinations'),('/pool-deck-builder-services.html','Pool deck services')]
        )
    if any(x in k for x in ('ogden','layton','kaysville','clearfield','syracuse','bountiful','centerville','woods cross','west haven','north ogden','eden','huntsville','liberty','hooper','fruit heights','uintah','roy','pleasant view')):
        return (
            'Local Deck Planning Considerations',
            'Northern Utah projects must account for snow, freeze-thaw cycles, sun exposure, drainage and local permit requirements. Yard grade, access and the height of the door above the ground influence structure, stairs and railing.',
            'The most useful project information includes property photos, approximate dimensions, preferred materials and how the space will be used. These details help narrow the design before final site verification.',
            [('/service-area-deck-building.html','Service areas'),('/deck-building.html','Deck building'),('/free-estimate.html','Request an estimate')]
        )
    return (
        'Planning a Durable Outdoor Space',
        'A successful deck project starts with the property conditions and intended use. Layout, access, drainage, structure, stairs, railing, shade and material choices should be considered together rather than as separate decisions.',
        'Northern Utah weather makes fastening, water management and maintenance especially important. A clear scope helps homeowners compare options and reduces surprises during construction or renovation.',
        [('/deck-building.html','Deck building services'),('/services-we-offer.html','All services'),('/free-estimate.html','Request an estimate')]
    )


def enrich(path: Path) -> bool:
    if path.name in SKIP_NAMES or 'migration-enrichment' in path.read_text(encoding='utf-8', errors='ignore'):
        return False
    markup = path.read_text(encoding='utf-8', errors='ignore')
    if len(visible_text(markup)) >= THRESHOLD:
        return False
    if 'noindex' in markup.lower():
        return False
    heading = get_heading(markup, path)
    title, p1, p2, links = topic_copy(heading + ' ' + path.as_posix())
    link_html = ' · '.join(f'<a href="{href}">{label}</a>' for href, label in links)
    block = f'''<section class="section alt migration-enrichment"><div class="wrap"><h2>{html.escape(title)}</h2><p>{html.escape(p1)}</p><p>{html.escape(p2)}</p><p>{link_html}</p></div></section><section class="cta migration-enrichment"><div class="wrap"><h2>Discuss Your Project</h2><p>Share photos, approximate dimensions and the features that matter most for a more specific project conversation.</p><a class="btn alt" href="/free-estimate.html">Request a Free Estimate</a></div></section>'''
    if '</main>' in markup:
        markup = markup.replace('</main>', block + '</main>', 1)
    elif '</body>' in markup:
        markup = markup.replace('</body>', block + '</body>', 1)
    else:
        markup += block
    path.write_text(markup, encoding='utf-8')
    return True


def main() -> None:
    changed = 0
    for path in ROOT.rglob('*.html'):
        if enrich(path):
            changed += 1
    print(f'Enriched {changed} thin HTML pages')

if __name__ == '__main__':
    main()
