#!/usr/bin/env python3
"""Combine two unchanged exposed tasks to check both documentation routes."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def cases():
    selections = [('retention-cases.json', 'retention-guarded'),
                  ('bundle-contract-v2-cases.json', 'search-protected')]
    return [next(c for c in json.loads((ROOT / file).read_text()) if c['id'] == name)
            for file, name in selections]


if __name__ == '__main__':
    (ROOT / 'mother-routing-cases.json').write_text(json.dumps(cases(), indent=2) + '\n')
