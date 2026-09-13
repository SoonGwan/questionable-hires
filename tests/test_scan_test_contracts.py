import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'benchmarks/scan_test_contracts.py'
spec = importlib.util.spec_from_file_location('contract_scan', SCRIPT)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class ContractScanTests(unittest.TestCase):
    def test_unittest_aliases_and_local_inheritance_find_async_sync_overrides(self):
        findings, unresolved = scanner.inspect_source(
            'import unittest as ut\nfrom unittest import TestCase as TC\n'
            'class Base(ut.IsolatedAsyncioTestCase):\n'
            '    async def fail(self, message): pass\n'
            '    async def asyncSetUp(self): pass\n'
            '    async def test_example(self): pass\n'
            'class Child(Base):\n    async def setUp(self): pass\n'
            'class Other(TC):\n    async def assertEqual(self, a, b): pass\n')
        self.assertEqual({(item['class_name'], item['method']) for item in findings},
                         {('Base', 'fail'), ('Child', 'setUp'), ('Other', 'assertEqual')})
        self.assertEqual(unresolved, [])

    def test_transport_fail_is_not_a_testcase_collision_and_imported_base_is_unknown(self):
        findings, unresolved = scanner.inspect_source(
            'from support import ExternalCase\n'
            'class Transport:\n    async def fail(self, key): pass\n'
            'class Review(ExternalCase):\n    async def fail(self, message): pass\n')
        self.assertEqual(findings, [])
        self.assertEqual([item['class_name'] for item in unresolved], ['Review'])

    def test_scan_never_executes_targets_and_reports_parse_gaps(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = 'raise RuntimeError("must not execute")\nimport unittest\n'
            source += 'class Case(unittest.TestCase):\n    async def fail(self, message): pass\n'
            (root / 'test_case.py').write_text(source)
            (root / 'invalid.py').write_text('not python !!!')
            (root / 'linked.py').symlink_to(root / 'test_case.py')
            result = scanner.scan(root)
            self.assertEqual(result['python_files'], 2)
            self.assertEqual(result['parsed_files'], 1)
            self.assertEqual(result['findings'][0]['path'], 'test_case.py')
            self.assertEqual(result['parse_errors'], [{'path': 'invalid.py', 'error': 'SyntaxError'}])
            self.assertEqual((root / 'test_case.py').read_text(), source)

    def test_missing_root_cannot_look_like_an_empty_successful_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, 'existing directory'):
                scanner.scan(Path(directory) / 'absent')
