#!/usr/bin/env python3
"""Reuse two existing tasks unchanged for current-bundle auto selection."""
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def cases():
    spec = importlib.util.spec_from_file_location('assembly_selection', ROOT / 'receipt_assembly_cases.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return json.loads((ROOT / 'landlord-check-scope-cases.json').read_text()) + module.cases()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
