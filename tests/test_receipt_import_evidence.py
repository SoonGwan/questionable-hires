"""Verify reported imports against the actual native test process."""
import json
from pathlib import Path
import sys
import unittest

import test_receipt_helper as fixture


class ReceiptImportEvidenceTests(unittest.TestCase):
    setUp = fixture.ReceiptHelperTests.setUp
    git = fixture.ReceiptHelperTests.git
    commit = fixture.ReceiptHelperTests.commit

    def test_loaded_path_and_pid_match_native_assertions_in_both_modes(self):
        test = self.root / 'test_rule.py'
        test.write_text(test.read_text() + '\nimport json, os, rule\n'
                        'print("NATIVE_IDENTITY " + json.dumps({"path": rule.__file__, '
                        '"pid": os.getpid()}), flush=True)\n')
        for invocation in ('bootstrap', 'module'):
            with self.subTest(invocation=invocation):
                result = fixture.helper.compare(self.root, dict(self.recipe,
                    invocation=invocation), python=sys.executable)
                identities = []
                for phase, exit_code in [('before', 1), ('after', 0)]:
                    check = result['checks'][phase]
                    self.assertEqual(check['exit_code'], exit_code, check['output'])
                    lines = check['output'].splitlines()
                    prefix = 'Verified copied import: rule '
                    evidence = [json.loads(s[len(prefix):]) for s in lines
                                if s.startswith(prefix)]
                    self.assertEqual(len(evidence), 1, check['output'])
                    native = [json.loads(s[len('NATIVE_IDENTITY '):]) for s in lines
                              if s.startswith('NATIVE_IDENTITY ')]
                    self.assertEqual(evidence, native)
                    path = Path(evidence[0]['path'])
                    self.assertTrue(path.is_relative_to(self.root.resolve()))
                    self.assertEqual(path.parent.name, phase)
                    self.assertFalse(path.exists(), 'Comparison copy must be removed')
                    identities.append(evidence[0])
                self.assertNotEqual(identities[0], identities[1])
                self.assertIn('AssertionError: False is not true',
                              result['checks']['before']['output'])
                self.assertTrue(result['originals']['unchanged'])

    def test_escaped_import_has_no_verified_identity(self):
        for invocation in ('bootstrap', 'module'):
            with self.subTest(invocation=invocation):
                result = fixture.helper.compare(self.root, dict(self.recipe,
                    invocation=invocation, imports=['json']), python=sys.executable)
                check = result['checks']['before']
                self.assertEqual(check['exit_code'], 7)
                self.assertNotIn('Verified copied import: json', check['output'])
                self.assertEqual(list(result['checks']), ['before'])
