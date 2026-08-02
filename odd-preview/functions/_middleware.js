class HeadInjector {
  element(element) {
    element.append('<link rel="stylesheet" href="/weebly-restore.css">', { html: true });
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
    .transform(response);
}
