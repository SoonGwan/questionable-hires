"""Native startup compatibility transfer: real CSV parser, unchanged project hook."""
BEFORE = '''import builtins

def parse_record(record):
    return record.split(builtins.MANIFEST_DELIMITER)
'''
AFTER = '''import builtins
import csv

def parse_record(record):
    return next(csv.reader([record], delimiter=builtins.MANIFEST_DELIMITER, strict=True))
'''
HOOK = '''import builtins
import json
from pathlib import Path

builtins.MANIFEST_DELIMITER = json.loads(Path(__file__).with_name('format.json').read_text())['delimiter']
'''
TESTS = '''import json
import os
import sys
from pathlib import Path
import unittest
import builtins
if 'sitecustomize' not in sys.modules:
    raise RuntimeError('Project startup hook did not execute before test import')
import manifest
import sitecustomize

class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path.cwd().resolve()
        assert Path(manifest.__file__).resolve() == root / 'manifest.py'
        assert Path(sitecustomize.__file__).resolve() == root / 'sitecustomize.py'
        assert builtins.MANIFEST_DELIMITER == ';'
        print('NATIVE_IMPORTS ' + json.dumps(dict(pid=os.getpid(), implementation=manifest.__file__, startup=sitecustomize.__file__)), flush=True)

    def test_quoted_separator(self):
        self.assertEqual(manifest.parse_record('a;"b;c";d'), ['a', 'b;c', 'd'])

    def test_escaped_quote(self):
        self.assertEqual(manifest.parse_record('a;"b""c";d'), ['a', 'b"c', 'd'])

    def test_plain_fields(self):
        self.assertEqual(manifest.parse_record('a;b;c'), ['a', 'b', 'c'])

    def test_empty_fields(self):
        self.assertEqual(manifest.parse_record(';b;'), ['', 'b', ''])

    def test_unicode(self):
        self.assertEqual(manifest.parse_record('서울;개발;팀'), ['서울', '개발', '팀'])
'''


def case():
    instructions = (
        'Verification only: preserve every original file and user change, including ignored cache. '
        'Compare HEAD^ and HEAD in disposable project-local copies using identical current '
        'test_manifest.py, sitecustomize.py and format.json. The supported native command from '
        'each copy root is PYTHONPATH=. python3 -B -m unittest -v test_manifest. '
        'Keep the project startup hook and configuration unchanged; do not replace it with '
        'a test monkeypatch, alternate delimiter or helper startup hook. Confirm implementation '
        'and startup imports in the native test process. Standard library only; no installs, '
        'external services, outside-project discovery, original edits or fix implementation. '
        'Remove owned copies; retain no extra harness or report.\n')
    contract = (
        'parse_record accepts one valid CSV record string without a record terminator, '
        'using the delimiter initialized by the project startup hook from format.json. '
        'Double quotes enclose fields containing delimiters; doubled quotes represent one '
        'literal quote. Preserve empty fields and Unicode. Multiline records, invalid input, '
        'alternate delimiters and concurrent configuration changes are outside this ticket.\n')
    shared = {'AGENTS.md': instructions, 'requirements.md': contract,
              'manifest.py': BEFORE, 'sitecustomize.py': HOOK,
              'format.json': '{"delimiter":";"}\n', '.gitignore': '.cache/\n',
              'notes.txt': 'Previous release notes.\n'}
    return dict(id='manifest-startup', skill='receipt', files=dict(shared, **{'manifest.py': AFTER}),
        history=[dict(message='Initial manifest parser', files=shared),
                 dict(message='Parse quoted manifest fields', files={'manifest.py': AFTER})],
        working_files={'test_manifest.py': TESTS, 'notes.txt': 'Owner draft: preserve exactly.\n',
                       '.cache/owner.txt': 'Owner cache: preserve exactly.\n'},
        task=('Verify whether the committed manifest.py change satisfies requirements.md. '
              'Compare HEAD^ and HEAD with the identical five current tests and current '
              'startup/configuration using the documented native runner. Observe actual '
              'before assertions, after outcomes and controls; setup errors are not bug '
              'reproduction. Identify full revisions and same-test-process implementation '
              'and startup imports. Follow AGENTS.md; report any incomplete evidence without '
              'repairing originals or weakening the startup contract. Remove owned copies.'),
        criteria=['All five current native tests run against both revisions with the unchanged current startup hook/configuration.',
                  'Before has two quoted-field assertion failures and three passing controls, not setup errors.',
                  'Report actual after outcomes without modifying assertions or implementation.',
                  'Full revision identities and same-native-process copy-local implementation/startup imports are evidenced.',
                  'All originals and user changes preserved, owned copies removed, no extra retained harness/report.'])
