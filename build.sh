#!/usr/bin/env bash
set -euo pipefail

rm -rf dist
mkdir -p dist

# Copy the source-controlled static site into Cloudflare's output directory.
# Repository control files stay out of the public website.
find . -mindepth 1 -maxdepth 1 \
  ! -name '.git' \
  ! -name 'dist' \
  ! -name 'build.sh' \
  ! -name 'README.md' \
  ! -name '.cloudflare-trigger' \
  -exec cp -a {} dist/ \;

if [ ! -f dist/index.html ]; then
  echo "index.html is missing from the repository root" >&2
  exit 1
fi
