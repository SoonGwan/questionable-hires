#!/usr/bin/env python3
"""Preserve both existing interval and final-only contracts without rewriting them."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def cases():
    source = json.loads((ROOT / 'bundle-contract-v2-cases.json').read_text())
    return [next(c for c in source if c['id'] == name)
            for name in ('search-protected', 'search-order')]


if __name__ == '__main__':
    (ROOT / 'mother-interval-cases.json').write_text(json.dumps(cases(), indent=2) + '\n')
