#!/usr/bin/env python3
"""Authored range-normalization retrospective verification transfer."""
import argparse
import json
from pathlib import Path


def cases():
    before = '''def coalesce(ranges):
    result = []
    for start, end in sorted(ranges):
        if result and start < result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result
'''
    after = before.replace('start < result', 'start <= result')
    tests = '''import unittest
import ranges

class RangeTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(ranges.coalesce([]), [])
    def test_disjoint(self):
        self.assertEqual(ranges.coalesce([(5, 7), (1, 3)]), [(1, 3), (5, 7)])
    def test_overlap(self):
        self.assertEqual(ranges.coalesce([(1, 4), (3, 8)]), [(1, 8)])
    def test_nested(self):
        self.assertEqual(ranges.coalesce([(1, 9), (2, 3)]), [(1, 9)])
    def test_touching(self):
        self.assertEqual(ranges.coalesce([(1, 4), (4, 8)]), [(1, 8)])
    def test_bridge(self):
        self.assertEqual(ranges.coalesce([(7, 9), (1, 4), (4, 7)]), [(1, 9)])
    def test_input_preserved(self):
        value = [(6, 9), (1, 3)]
        ranges.coalesce(value)
        self.assertEqual(value, [(6, 9), (1, 3)])
'''
    task = ('Verify the already-present uncommitted ranges.py fix against HEAD. '
            'Run all seven current test_ranges tests unchanged on HEAD and working '
            'implementations in separate project-local copies. Within each native '
            'unittest process, confirm ranges.__file__ resolves inside its copy before '
            'running tests. Capture actual before assertion failures and passing controls, '
            'then all after outcomes. Identify the before commit and working implementation '
            'SHA-256. Preserve all existing original files, including unrelated drafts; '
            'report byte and permission checks for ranges.py, test_ranges.py and drafts/release.txt. '
            'Delete owned comparison copies before finishing; captured output is sufficient. '
            'Do not commit, stash, reset, install dependencies or use external services. '
            'Follow project instructions and requirements.md.')
    return [dict(id='uncommitted-ranges-fix', skill='receipt', task=task,
        files={'AGENTS.md': 'Verification only, no original-file edits. Use Python standard library unittest (-v test_ranges). Scratch must be explicitly project-local; remove owned comparison copies before finishing.\n',
               'requirements.md': 'coalesce accepts a finite list of integer (start, end) pairs with start < end. Return sorted maximal unions, merging overlapping OR touching pairs. Do not mutate the caller list. Empty input returns []. Invalid intervals, other numeric types and concurrent mutation are out of scope. The working fix already exists; compare retrospectively using the same current tests.\n',
               'ranges.py': before, 'drafts/release.txt': 'Old release note.\n'},
        working_files={'ranges.py': after, 'test_ranges.py': tests,
                       'drafts/release.txt': 'Unrelated unfinished release draft. Preserve exactly.\n'},
        criteria=['Seven unchanged native tests on both versions; before two assertion failures and five passing controls, after seven passes.',
                  'Implementation provenance checked within each native test process.',
                  'Before commit and working SHA-256 identified; originals preserved with requested byte/mode checks.',
                  'Project-local copies removed; no commit/stash/reset/install/external actions.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
