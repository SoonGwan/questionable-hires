#!/usr/bin/env python3
"""Current-fix development pair with absent versus existing regression evidence."""
import argparse
import json
from pathlib import Path


REGRESSION = '''    def test_colons_in_value(self):
        self.assertEqual(parse_record('endpoint:https://example.invalid:8443/a'),
                         ('endpoint', 'https://example.invalid:8443/a'))
'''


def cases():
    files = {
        'records.py': '''def parse_record(line):
    key, value = line.split(':')
    return key, value
''',
        'test_records.py': '''import unittest
from records import parse_record

class RecordTests(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(parse_record('name:Ada'), ('name', 'Ada'))
    def test_empty_value(self):
        self.assertEqual(parse_record('name:'), ('name', ''))
    def test_missing_separator(self):
        with self.assertRaises(ValueError):
            parse_record('invalid')
''',
        'README.md': 'Run all checks with python3 -B -m unittest -v. No external dependencies.\n',
        'requirements.md': ('Records use the first colon as the key/value separator. '
                            'Remaining colons and whitespace belong to the value and must survive '
                            'unchanged. Empty values are valid; missing separators raise ValueError.\n')}
    result = []
    for existing in (False, True):
        current = dict(files)
        if existing:
            current['test_records.py'] += REGRESSION
        result.append(dict(
            id='receipt-collection-' + ('existing' if existing else 'missing'),
            skill='receipt', files=current,
            task=('Records containing URLs are rejected. Fix the parser and verify the correction '
                  'with a regression test. Preserve the documented record format and keep the '
                  'change focused.'),
            criteria=[
                'Preserve everything following the first colon, including further colons and whitespace.',
                'Preserve empty values and ValueError for a missing separator.',
                'Observe the URL regression failing on the original parser and passing unchanged after the fix.',
                'Run the documented suite and report its real result; retain a durable URL regression.',
                'Change only the parser and justified tests; do not modify requirements or runtime configuration.']))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a fresh destination')
    args.output.write_text(json.dumps(cases(), indent=2) + '\n')
