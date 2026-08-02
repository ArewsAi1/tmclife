const PAGE_META = {
  '/': {
    title: 'Decking Supply Store in Ogden, Utah | Ogden Deck Depot',
    description: 'Shop composite decking, railing, lumber, fasteners and deck-building supplies in Ogden, Utah. Serving contractors and homeowners across Northern Utah.'
  },
  '/products-ogden-deck-depot.html': {
    title: 'Decking, Railing & Deck Building Products | Ogden Deck Depot',
    description: 'Browse Deckorators, TimberTech, Trex, Fiberon, railing, lumber, fasteners, footings and other professional deck-building products in Ogden, Utah.'
  },
  '/composite-decking-ogden.html': {
    title: 'Composite Decking in Ogden, Utah | Ogden Deck Depot',
    description: 'Compare composite decking from Deckorators, TimberTech, Trex, Fiberon and other trusted brands at Ogden Deck Depot in Northern Utah.'
  },
  '/deckorators-decking.html': {
    title: 'Deckorators Decking in Ogden, Utah | Ogden Deck Depot',
    description: 'Shop Deckorators composite decking collections and colors with local product guidance from Ogden Deck Depot in Ogden, Utah.'
  },
  '/timbertech-decking-ogden.html': {
    title: 'TimberTech Decking in Ogden, Utah | Ogden Deck Depot',
    description: 'Explore TimberTech composite and PVC decking products available through Ogden Deck Depot for contractors and homeowners in Northern Utah.'
  },
  '/trex-deck-boards-for-sale-in-ogden-ut.html': {
    title: 'Trex Deck Boards for Sale in Ogden, Utah | Ogden Deck Depot',
    description: 'Shop Trex deck boards, fascia, accessories and railing locally through Ogden Deck Depot in Ogden, Utah.'
  },
  '/deck-railing-ogden.html': {
    title: 'Deck Railing Systems in Ogden, Utah | Ogden Deck Depot',
    description: 'Compare steel, aluminum, cable, composite and vinyl deck railing systems at Ogden Deck Depot in Ogden, Utah.'
  },
  '/contact.html': {
    title: 'Contact Ogden Deck Depot | Decking Supply in Ogden, Utah',
    description: 'Contact Ogden Deck Depot for product availability, decking quotes and help choosing deck-building materials in Northern Utah.'
  },
  '/about.html': {
    title: 'About Ogden Deck Depot | Northern Utah Decking Supplier',
    description: 'Learn about Ogden Deck Depot, a local source for decking, railing, lumber and professional deck-building supplies in Northern Utah.'
  }
};

const ASSET_VERSION = '20260802-2';

class HeadInjector {
  constructor(canonicalUrl, isHome, meta) {
    this.canonicalUrl = canonicalUrl;
    this.isHome = isHome;
    this.meta = meta;
  }

  element(element) {
    element.append('<link rel="stylesheet" href="/weebly-restore.css?v=' + ASSET_VERSION + '">', { html: true });
    element.append('<link rel="stylesheet" href="/site-optimizer.css?v=' + ASSET_VERSION + '">', { html: true });
    element.append('<script src="/site-optimizer.js?v=' + ASSET_VERSION + '" defer></script>', { html: true });
    element.append('<link rel="canonical" href="' + this.canonicalUrl + '">', { html: true });
    element.append('<meta name="theme-color" content="#111111">', { html: true });
    element.append('<link rel="preconnect" href="https://cdn11.editmysite.com" crossorigin>', { html: true });
    element.append('<link rel="preconnect" href="https://cdn2.editmysite.com" crossorigin>', { html: true });

    if (this.meta) {
      element.append('<title>' + this.meta.title + '</title>', { html: true });
      element.append('<meta name="description" content="' + this.meta.description + '">', { html: true });
      element.append('<meta property="og:title" content="' + this.meta.title + '">', { html: true });
      element.append('<meta property="og:description" content="' + this.meta.description + '">', { html: true });
      element.append('<meta property="og:type" content="website">', { html: true });
      element.append('<meta property="og:url" content="' + this.canonicalUrl + '">', { html: true });
      element.append('<meta name="twitter:card" content="summary_large_image">', { html: true });
    }

    if (this.isHome) {
      const schema = {
        '@context': 'https://schema.org',
        '@type': ['LocalBusiness', 'HomeAndConstructionBusiness'],
        '@id': 'https://www.ogdendeckdepot.com/#business',
        name: 'Ogden Deck Depot',
        url: 'https://www.ogdendeckdepot.com/',
        telephone: '+1-435-222-5819',
        address: {
          '@type': 'PostalAddress',
          streetAddress: '190 W 33rd Street #160',
          addressLocality: 'Ogden',
          addressRegion: 'UT',
          postalCode: '84401',
          addressCountry: 'US'
        },
        areaServed: ['Ogden', 'Weber County', 'Davis County', 'Northern Utah']
      };
      element.append('<script type="application/ld+json">' + JSON.stringify(schema) + '</script>', { html: true });
    }
  }
}

class RemoveElement {
  element(element) {
    element.remove();
  }
}

class ImageOptimizer {
  constructor() {
    this.count = 0;
  }

  element(element) {
    this.count += 1;
    const src = element.getAttribute('src');
    if (!src || src.startsWith('data:')) return;

    element.setAttribute('decoding', 'async');
    if (this.count <= 2) {
      element.setAttribute('loading', 'eager');
      element.setAttribute('fetchpriority', 'high');
    } else {
      element.setAttribute('loading', 'lazy');
      element.setAttribute('fetchpriority', 'low');
    }

    if (!element.getAttribute('alt')) {
      const clean = src.split('/').pop().split('?')[0]
        .replace(/\.(webp|jpe?g|png|gif|svg)$/i, '')
        .replace(/[-_]+/g, ' ')
        .replace(/\borig\b/gi, '')
        .replace(/\s+/g, ' ')
        .trim();
      element.setAttribute('alt', clean || 'Ogden Deck Depot decking product');
    }
  }
}

class LinkNormalizer {
  element(element) {
    const href = element.getAttribute('href');
    if (!href) return;

    if (href.startsWith('http://ogdendeckdepot.com')) {
      element.setAttribute('href', href.replace('http://ogdendeckdepot.com', 'https://www.ogdendeckdepot.com'));
    } else if (href.startsWith('https://ogdendeckdepot.com')) {
      element.setAttribute('href', href.replace('https://ogdendeckdepot.com', 'https://www.ogdendeckdepot.com'));
    }

    if (element.getAttribute('target') === '_blank') {
      const rel = new Set((element.getAttribute('rel') || '').split(/\s+/).filter(Boolean));
      rel.add('noopener');
      rel.add('noreferrer');
      element.setAttribute('rel', Array.from(rel).join(' '));
    }
  }
}

export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === 'ogdendeckdepot.com') {
    url.hostname = 'www.ogdendeckdepot.com';
    return Response.redirect(url.toString(), 301);
  }

  const response = await context.next();
  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/html')) return response;

  const isHome = url.pathname === '/' || url.pathname === '/index.html';
  const normalizedPath = isHome ? '/' : url.pathname;
  const canonicalUrl = 'https://www.ogdendeckdepot.com' + normalizedPath;
  const meta = PAGE_META[normalizedPath];

  let rewriter = new HTMLRewriter()
    .on('link[rel="canonical"]', new RemoveElement())
    .on('meta[name="keywords"]', new RemoveElement())
    .on('head', new HeadInjector(canonicalUrl, isHome, meta))
    .on('img[src]', new ImageOptimizer())
    .on('a[href]', new LinkNormalizer());

  if (meta) {
    rewriter = rewriter
      .on('title', new RemoveElement())
      .on('meta[name="description"]', new RemoveElement())
      .on('meta[property="og:title"]', new RemoveElement())
      .on('meta[property="og:description"]', new RemoveElement())
      .on('meta[property="og:url"]', new RemoveElement());
  }

  return rewriter.transform(response);
}
