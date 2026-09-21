"""CLI serialization preserves native evidence and exit semantics."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/con-artist/scripts/audit.py'
spec = importlib.util.spec_from_file_location('audit_output', SCRIPT)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditOutputTests(unittest.TestCase):
    def test_single_and_batch_serialization_and_exits(self):
        for batch in (False, True):
            for status in ('observed', 'incomplete'):
                check = dict(exit_code=1, native_exit_code=1, timed_out=False,
                             output_truncated=True, output='AssertionError: 한글\n\\x00\x00',
                             suite_observation=dict(tests=2, skipped=0, successful=False))
                result = dict(status=status, checks=dict(mutant_tests=check),
                              integrity=dict(owned_scratch_removed=True))
                if batch:
                    result = dict(status=status, audits=[result, dict(checks=dict(
                        correct_tests=dict(observation_ref='#/audits/0/checks/correct_tests')))])
                for pretty in (False, True):
                    with self.subTest(batch=batch, status=status, pretty=pretty):
                        stream = io.StringIO()
                        argv = ['audit.py', '--spec', '-'] + (['--pretty'] if pretty else [])
                        recipe = {'mutations': []} if batch else {}
                        with patch.object(sys, 'argv', argv), patch.object(sys, 'stdin', io.StringIO(json.dumps(recipe))), patch.object(audit, 'audit_batch' if batch else 'audit', return_value=result) as execute, contextlib.redirect_stdout(stream):
                            code = audit.main()
                        execute.assert_called_once()
                        self.assertEqual(code, 0 if status == 'observed' else 2)
                        self.assertEqual(json.loads(stream.getvalue()), result)
                        expected = json.dumps(result, indent=2) if pretty else json.dumps(result, separators=(',', ':'))
                        self.assertEqual(stream.getvalue(), expected + '\n')

    def test_invalid_recipe_has_no_observation_output(self):
        for pretty in (False, True):
            out, err = io.StringIO(), io.StringIO()
            with patch.object(sys, 'argv', ['audit.py', '--spec', '-'] + (['--pretty'] if pretty else [])), patch.object(sys, 'stdin', io.StringIO('{invalid')), contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                with self.assertRaises(SystemExit) as caught:
                    audit.main()
            self.assertEqual(caught.exception.code, 2)
            self.assertEqual(out.getvalue(), '')
            self.assertIn('Audit not established:', err.getvalue())
