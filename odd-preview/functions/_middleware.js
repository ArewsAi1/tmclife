class HeadInjector {
  element(element) {
    element.append('<link rel="stylesheet" href="/weebly-restore.css">', { html: true });
  }
}

class HomepageDeckoratorsImageFix {
  element(element) {
    element.setAttribute('src', '/assets/hero.webp');
    element.setAttribute('loading', 'eager');
    element.setAttribute('decoding', 'async');
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

  if (!contentType.includes('text/html')) {
    return response;
  }

  let rewriter = new HTMLRewriter().on('head', new HeadInjector());

  if (url.pathname === '/' || url.pathname === '/index.html') {
    rewriter = rewriter.on(
      'img[src*="deckorators-voyage-line-by-ogden-deck-depot"]',
      new HomepageDeckoratorsImageFix()
    );
  }

  return rewriter.transform(response);
}
