#!/usr/bin/env python3
"""Authored uncommitted-fix verification with frozen current data and tests."""
import argparse
import json
from pathlib import Path


def cases():
    original = '''def parse(text):
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("=")
        values[parts[0].strip()] = parts[1].strip()
    return values
'''
    files = {
        'AGENTS.md': ('Work only in this project. Verify, do not edit original files, commit, '
                      'stash or reverse the working patch. Use project-local disposable copies. '
                      'Python standard library only; do not install anything. Run the current '
                      'suite with python3 -B -m unittest -v checks.test_parser in each copy.\n'),
        'requirements.md': ('Settings contain KEY=VALUE lines. Split at the first equals only; '
                            'later equals signs belong to the value. Strip surrounding key/value '
                            'whitespace, ignore blank/comment lines, retain empty values, last '
                            'duplicate key wins. Inputs have nonempty keys and an equals sign '
                            'on each non-comment/nonblank line. Quoting, interpolation and malformed '
                            'input policy are outside scope. Current checks and samples must be '
                            'identical for both implementations. The working parser fix is not committed.\n'),
        'settings/__init__.py': '',
        'settings/parser.py': original,
        'notes.txt': 'Previous planning note.\n',
    }
    working = {
        'settings/parser.py': original.replace('line.split("=")', 'line.split("=", 1)'),
        'notes.txt': 'Unrelated user draft: keep this exact text.\n',
        'checks/__init__.py': '',
        'checks/samples/values.json': json.dumps({
            'token': 'TOKEN=abc==\n', 'query': 'URL=https://example.invalid/a?x=1&y=2\n',
            'plain': ' # ignored\n\nNAME = Ada\n', 'empty': 'EMPTY=\n',
            'duplicate': 'NAME=first\nNAME=last\n'}) + '\n',
        'checks/support.py': '''import json
from pathlib import Path

def sample(name):
    return json.loads((Path(__file__).parent / "samples/values.json").read_text())[name]
''',
        'checks/test_parser.py': '''import unittest
from settings.parser import parse
from checks.support import sample

class ParserTests(unittest.TestCase):
    def test_token_padding(self):
        self.assertEqual(parse(sample("token")), {"TOKEN": "abc=="})

    def test_query_value(self):
        self.assertEqual(parse(sample("query")), {"URL": "https://example.invalid/a?x=1&y=2"})

    def test_whitespace_and_comments(self):
        self.assertEqual(parse(sample("plain")), {"NAME": "Ada"})

    def test_empty_value(self):
        self.assertEqual(parse(sample("empty")), {"EMPTY": ""})

    def test_duplicate_last_wins(self):
        self.assertEqual(parse(sample("duplicate")), {"NAME": "last"})
''',
    }
    return [dict(id='uncommitted-settings-fix', skill='receipt', files=files,
                 working_files=working,
                 task=('Verify the already-present uncommitted fix in settings/parser.py against '
                       'HEAD. Execute the same current checks.test_parser suite and sample files '
                       'on HEAD implementation and the current working implementation in separate '
                       'project-local copies. Confirm implementation imports resolve inside each '
                       'comparison copy. Establish actual defect-specific before failures and '
                       'after passes, including all five existing test methods; identify the '
                       'before commit and current implementation content. Preserve every original '
                       'file, including current tests and unrelated notes.txt changes; do not '
                       'commit, stash, reset or implement anything. Follow requirements.md and '
                       'project instructions. Report observed results and limits, not just exit codes.'),
                 criteria=[
                     'Identical current tests/data execute against HEAD and frozen uncommitted implementation.',
                     'Before has token/query assertion failures and three controls passing; after all five pass.',
                     'Imported implementation belongs to each copy; before commit and current content are identified.',
                     'Original working bytes and user changes preserved; no commits, stash, reset, external discovery or installs.',
                     'Copies stay project-local and are cleaned; only actual execution supports the final claim.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
