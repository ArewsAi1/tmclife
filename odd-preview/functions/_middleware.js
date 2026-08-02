export async function onRequest(context) {
  const url = new URL(context.request.url);
  if (url.hostname === 'ogdendeckdepot.com') {
    url.hostname = 'www.ogdendeckdepot.com';
    return Response.redirect(url.toString(), 301);
  }
  return context.next();
}
