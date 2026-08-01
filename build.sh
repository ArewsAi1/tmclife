#!/usr/bin/env bash
set -euo pipefail

ARCHIVE="tmclife-cloudflare-fixed-v2.zip"
rm -rf dist
mkdir -p dist

if [ ! -f "$ARCHIVE" ]; then
  echo "$ARCHIVE is missing from the repository root" >&2
  exit 1
fi

unzip -q "$ARCHIVE" -d dist

# Support either a flat ZIP or a ZIP containing one outer folder.
if [ ! -f dist/index.html ]; then
  first_dir=$(find dist -mindepth 1 -maxdepth 1 -type d | head -1 || true)
  if [ -n "$first_dir" ] && [ -f "$first_dir/index.html" ]; then
    temp_dir="${first_dir}.tmp"
    mv "$first_dir" "$temp_dir"
    cp -a "$temp_dir/." dist/
    rm -rf "$temp_dir"
  fi
fi

if [ ! -f dist/index.html ]; then
  echo "index.html was not found after extracting $ARCHIVE" >&2
  find dist -maxdepth 2 -type f | head -50 >&2 || true
  exit 1
fi
