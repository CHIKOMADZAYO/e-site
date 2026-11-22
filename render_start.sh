#!/usr/bin/env bash
# Render start script: seed the persistent disk with catalog images, then serve.
set -euo pipefail

# A Render persistent disk is mounted (empty) at MEDIA_ROOT. Seed the catalog
# product images from the copies committed under the app's static folder so
# existing products render on first boot. Uploads made later persist on the disk.
MEDIA_DIR="${MEDIA_ROOT:-media}/products"
mkdir -p "$MEDIA_DIR"
for f in ecommerce/ui/static/ui/images/product-*.jpg; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    if [ ! -e "$MEDIA_DIR/$base" ]; then
        cp "$f" "$MEDIA_DIR/$base"
    fi
done

exec gunicorn ecommerce.wsgi:application