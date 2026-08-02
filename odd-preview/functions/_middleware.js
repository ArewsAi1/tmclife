class HeadInjector {
  constructor(canonicalUrl, isHome) {
    this.canonicalUrl = canonicalUrl;
    this.isHome = isHome;
  }

  element(element) {
    element.append('<link rel="stylesheet" href="/weebly-restore.css">', { html: true });
    element.append('<link rel="stylesheet" href="/site-optimizer.css">', { html: true });
    element.append('<script src="/site-optimizer.js" defer></script>', { html: true });
    element.append('<link rel="canonical" href="' + this.canonicalUrl + '">', { html: true });
    element.append('<meta name="theme-color" content="#111111">', { html: true });
    element.append('<link rel="preconnect" href="https://cdn11.editmysite.com" crossorigin>', { html: true });
    element.append('<link rel="preconnect" href="https://cdn2.editmysite.com" crossorigin>', { html: true });

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
        areaServed: ['Ogden', 'Weber County', 'Davis County', 'Northern Utah'],
        sameAs: []
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

class ImagePathNormalizer {
  constructor() {
    this.count = 0;
  }

  element(element) {
    this.count += 1;
    const src = element.getAttribute('src');
    if (!src || src.startsWith('data:')) return;

    let fixed = src;
    if (!src.startsWith('http://') && !src.startsWith('https://')) {
      fixed = fixed.replace(/\.(jpe?g|png)(\?.*)?$/i, '.webp$2');
      fixed = fixed
        .replace(/_orig_orig\.webp(\?.*)?$/i, '_orig.webp$1')
        .replace(/-orig_orig\.webp(\?.*)?$/i, '-orig.webp$1');
      if (fixed !== src) element.setAttribute('src', fixed);
    }

    element.setAttribute('decoding', 'async');
    if (this.count <= 2) {
      element.setAttribute('loading', 'eager');
      element.setAttribute('fetchpriority', 'high');
    } else {
      element.setAttribute('loading', 'lazy');
      element.setAttribute('fetchpriority', 'low');
    }

    if (!element.getAttribute('alt')) {
      const clean = fixed.split('/').pop().split('?')[0]
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
  const canonicalUrl = 'https://www.ogdendeckdepot.com' + (isHome ? '/' : url.pathname);

  return new HTMLRewriter()
    .on('link[rel="canonical"]', new RemoveElement())
    .on('meta[name="keywords"]', new RemoveElement())
    .on('head', new HeadInjector(canonicalUrl, isHome))
    .on('img[src]', new ImagePathNormalizer())
    .on('a[href]', new LinkNormalizer())
    .transform(response);
}
