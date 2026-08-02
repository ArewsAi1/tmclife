class HeadInjector {
  element(element) {
    element.append('<link rel="stylesheet" href="/weebly-restore.css">', { html: true });
  }
}

class ImagePathNormalizer {
  element(element) {
    const src = element.getAttribute('src');
    if (!src || src.startsWith('data:') || src.startsWith('http://') || src.startsWith('https://')) return;

    let fixed = src;

    // The restored Weebly export converted local JPG/PNG files to WebP,
    // while some HTML references retained the original extension.
    fixed = fixed.replace(/\.(jpe?g|png)(\?.*)?$/i, '.webp$2');

    // Some archived paths received a duplicated _orig suffix during export.
    fixed = fixed
      .replace(/_orig_orig\.webp(\?.*)?$/i, '_orig.webp$1')
      .replace(/-orig_orig\.webp(\?.*)?$/i, '-orig.webp$1');

    if (fixed !== src) {
      element.setAttribute('src', fixed);
    }

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

  return new HTMLRewriter()
    .on('head', new HeadInjector())
    .on('img[src]', new ImagePathNormalizer())
    .transform(response);
}
