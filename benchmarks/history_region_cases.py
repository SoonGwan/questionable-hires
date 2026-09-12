#!/usr/bin/env python3
"""Build a fixed multi-decision history review, without prescribing tools."""
import argparse
import json
from pathlib import Path


def cases():
    initial = '''def summarize(record):
    code = record['code']
    name = record['display_name']
    amount = record['amount']
    return code, name, amount
'''
    legacy = initial.replace("record['code']", "record.get('code') or 'unknown'")
    names = legacy.replace("record['display_name']", "record.get('display_name') or record['name']")
    guarded = names.replace('    return code', "    if amount < 0:\n        raise ValueError('negative amount')\n    return code")
    caller = '''from summary import summarize

def render(record):
    normalized = dict(record)
    normalized['display_name'] = record.get('display_name') or record['name']
    return summarize(normalized)
'''
    requirements = '''render is the sole supported entrypoint. summary.summarize is private.
Input name is nonempty; display_name and code may be missing or empty. Missing or
empty code must render as 'unknown'; missing or empty display_name uses name.
amount is an integer and negative values must raise ValueError. Upstream does not
reject negatives. There are no other consumers, plugins or supported direct calls.
Use python3 -B -m unittest -v. Review only: preserve all original files.
'''
    tests = '''import unittest
from consumer import render

class RenderTests(unittest.TestCase):
    def test_legacy(self):
        self.assertEqual(render({'name': 'Ada', 'amount': 0}), ('unknown', 'Ada', 0))
    def test_empty(self):
        self.assertEqual(render({'name': 'Ada', 'display_name': '', 'code': '', 'amount': 2}), ('unknown', 'Ada', 2))
    def test_current(self):
        self.assertEqual(render({'name': 'Ada', 'display_name': 'A', 'code': 'X', 'amount': 3}), ('X', 'A', 3))
    def test_negative(self):
        with self.assertRaises(ValueError):
            render({'name': 'Ada', 'amount': -1})
'''
    files = {'summary.py': guarded, 'consumer.py': caller,
             'requirements.md': requirements, 'test_consumer.py': tests}
    history = [{'message': message, 'files': {'summary.py': source}} for message, source in [
        ('Initial summary implementation', initial),
        ('Support records without a populated code', legacy),
        ('Support legacy name-only display records', names),
        ('Reject negative amounts at the summary boundary', guarded)]]
    history.append({'message': 'Normalize display names at the sole public entrypoint',
                    'files': {k: v for k, v in files.items() if k != 'summary.py'}})
    return [dict(id='history-three-decisions', skill='necromancer', files=files, history=history,
                 task="Review whether summary.summarize can remove its code fallback, display-name fallback and negative-amount guard. For each, establish the historical reason and current necessity through the supported render path. Cite the relevant commits and verify proposed behavior. Do not implement changes or edit project files.",
                 criteria=['Retains code fallback and negative-amount rejection; permits removing only the private display-name fallback while preserving caller normalization.',
                           'Cites each actual introducing commit and the later caller normalization, without treating historical need as current necessity.',
                           'Exercises current and proposed behavior through actual render, preserving missing/empty/current inputs and negative rejection.',
                           'Preserves project files and scope; does not infer omitted changes are absent.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
