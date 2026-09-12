#!/usr/bin/env python3
"""Build two fixed development cases; generated padding models a bulk rewrite."""
import argparse
import json
from pathlib import Path


def cases():
    def module(expression, revision):
        padding = ''.join(f'# generated documentation {revision} {i:03d} ' + 'x' * 90 + '\n'
                          for i in range(160))
        return padding + 'def label(record):\n    return ' + expression + '\n'

    before = module('record["display"]', 'A')
    current = module('record.get("display") or record["name"]', 'B')
    result = []
    for active in (True, False):
        caller = ('from labels import label\n\ndef render(record):\n    return label(record)\n' if active else
                  'from labels import label\n\ndef render(record):\n'
                  '    value = record.get("display") or record["name"]\n'
                  '    return label({"display": value})\n')
        files = {
            'labels.py': current,
            'consumer.py': caller,
            'requirements.md': ('Internal renderer; render is the sole supported entrypoint. '
                'labels.label is private, not a supported external API. Inputs have a nonempty name; '
                'display may be absent, empty, or a nonempty string. Render must use name when '
                'display is absent or empty. No other call paths or plugins are supported.\n'),
            'test_consumer.py': ('import unittest\nfrom consumer import render\n\n'
                'class RenderTests(unittest.TestCase):\n'
                '    def test_inputs(self):\n'
                '        for record, expected in [({"name": "Ada"}, "Ada"), '
                '({"name": "Ada", "display": ""}, "Ada"), '
                '({"name": "Ada", "display": "A"}, "A")]:\n'
                '            with self.subTest(record=record):\n'
                '                self.assertEqual(render(record), expected)\n')}
        history = [
            {'message': 'Initial private label implementation', 'files': {'labels.py': before}},
            {'message': 'Regenerate documentation and support legacy name-only records',
             'files': {'labels.py': current}},
            {'message': 'Connect renderer' if active else 'Normalize records at the sole entrypoint',
             'files': {k: v for k, v in files.items() if k != 'labels.py'}}]
        result.append(dict(id='history-bulk-' + ('active' if active else 'normalized'),
            skill='necromancer', files=files, history=history,
            task=('Can the fallback in labels.label be replaced with record["display"]? '
                  'Review the historical reason and current necessity, citing the relevant commit '
                  'and current caller. Verify the effect on the supported renderer inputs. '
                  'Do not implement the change or edit project files.'),
            criteria=[
                ('Keep the fallback: missing/empty display is still passed directly to label.' if active else
                 'The private fallback can be removed: the sole supported caller normalizes first.'),
                'Identify the actual compatibility commit, not the original root or later caller commit.',
                'Verify missing, empty and nonempty display through the actual render path for current and proposed behavior.',
                'Preserve all project files and remain inside the project boundary.',
                'Do not claim omitted patch rows establish absence of other changes.']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; use a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
