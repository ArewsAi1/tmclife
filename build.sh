#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://d3463ff9.tmclife.pages.dev"
rm -rf dist mirror
mkdir -p dist mirror

# Mirror the current stable Cloudflare deployment.
wget --quiet --mirror --page-requisites --adjust-extension --convert-links --no-parent \
  --directory-prefix=mirror "$BASE_URL/"

SOURCE_DIR="mirror/d3463ff9.tmclife.pages.dev"
cp -a "$SOURCE_DIR/." dist/

# Remove the stray visible Google ads.txt line from generated HTML.
find dist -type f -name '*.html' -print0 | xargs -0 sed -i \
  '/google\.com, pub-6809869907055930, DIRECT, f08c47fec0942fa0/d'

# Repair the homepage hero asset reference.
sed -i 's#1078885227\.jpg#1078885227.webp#g' dist/index.html

# Force readable navigation colors and a reliable hero background.
cat >> dist/files/main_style.css <<'CSS'

/* TMC Cloudflare Git deployment fixes */
body.header-page .birdseye-header {
  background-color: rgba(0, 0, 0, 0.82) !important;
  color: #fff !important;
  border-color: #fff !important;
}
body.header-page .birdseye-header a,
body.header-page .birdseye-header .logo a,
body.header-page .birdseye-header #wsite-title,
body.header-page .birdseye-header .nav a,
body.header-page .birdseye-header .nav .wsite-menu-item,
body.header-page .birdseye-header .nav .wsite-menu-title {
  color: #fff !important;
  text-shadow: 0 1px 2px rgba(0,0,0,.9) !important;
}
body.header-page.affix .birdseye-header {
  background-color: #fff !important;
  color: #111 !important;
  border-color: #111 !important;
}
body.header-page.affix .birdseye-header a,
body.header-page.affix .birdseye-header .logo a,
body.header-page.affix .birdseye-header #wsite-title,
body.header-page.affix .birdseye-header .nav a,
body.header-page.affix .birdseye-header .nav .wsite-menu-item,
body.header-page.affix .birdseye-header .nav .wsite-menu-title {
  color: #111 !important;
  text-shadow: none !important;
}
body.header-page .wsite-header-section {
  background-image: url('/uploads/1/1/3/7/113789703/background-images/1078885227.webp') !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  background-attachment: scroll !important;
}
CSS

# Keep clean URLs working on Cloudflare Pages.
cat > dist/_redirects <<'REDIRECTS'
/* /:splat.html 200
REDIRECTS
