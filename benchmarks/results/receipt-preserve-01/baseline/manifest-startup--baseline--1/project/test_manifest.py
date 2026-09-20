import json
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
