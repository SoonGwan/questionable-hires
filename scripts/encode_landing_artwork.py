#!/usr/bin/env python3
"""Encode the approved artwork losslessly; Pillow is needed only to regenerate/check."""
import argparse
import hashlib
import io
import json
from pathlib import Path

from PIL import Image, features

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = (ROOT / 'assets/team-characters.png').read_bytes()
    with Image.open(io.BytesIO(source)) as original:
        encoded = io.BytesIO()
        original.save(encoded, format='WEBP', lossless=True, exact=True,
                      quality=100, method=6, icc_profile=original.info.get('icc_profile', b''))
        data = encoded.getvalue()
        pixels = original.convert('RGBA').tobytes()
        with Image.open(io.BytesIO(data)) as decoded:
            if (decoded.size != original.size or decoded.convert('RGBA').tobytes() != pixels
                    or decoded.info.get('icc_profile') != original.info.get('icc_profile')):
                raise ValueError('Encoded artwork does not preserve dimensions, pixels and color profile')
        manifest = dict(source_sha256=hashlib.sha256(source).hexdigest(),
                        webp_sha256=hashlib.sha256(data).hexdigest(),
                        rgba_sha256=hashlib.sha256(pixels).hexdigest(),
                        width=original.width, height=original.height,
                        source_bytes=len(source), webp_bytes=len(data),
                        pillow=Image.__version__, libwebp=features.version('webp'),
                        options=dict(lossless=True, exact=True, quality=100, method=6))
    files = {'team-characters.webp': data,
             'team-characters-webp.json': (json.dumps(manifest, indent=2) + '\n').encode()}
    for name, content in files.items():
        path = ROOT / 'assets' / name
        if args.check:
            if path.read_bytes() != content:
                raise ValueError('Stale artwork derivative: ' + name)
        else:
            path.write_bytes(content)
    print(('Checked' if args.check else 'Encoded') +
          f' identical RGBA pixels: {len(source):,} -> {len(data):,} bytes')


if __name__ == '__main__':
    main()
