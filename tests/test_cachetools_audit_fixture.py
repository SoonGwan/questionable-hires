import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('cachetools_audit', ROOT / 'benchmarks/cachetools_audit_cases.py')
fixture = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(fixture)


class CachetoolsAuditFixtureTests(unittest.TestCase):
    def test_upstream_identities_and_task_separation(self):
        files = fixture.source_files()
        case, = fixture.cases()
        for name, text in files.items(): self.assertEqual(case['files'][name], text)
        self.assertEqual(len(case['criteria']), 5)
        self.assertNotIn('behavioral_witness', case['files'])
        source = files[fixture.TARGET]
        before = source[:source.index('class LRUCache(Cache):')]
        after = source[source.index('class MRUCache(Cache):'):]
        for name in [*fixture.FAULTS, 'equivalent']:
            revised = fixture.revise(source, name)
            self.assertTrue(revised.startswith(before) and revised.endswith(after))

    def test_native_correct_equivalent_and_fault_witnesses(self):
        rows = fixture.preflight()
        self.assertEqual(len(rows), 6)
        self.assertEqual([r['behavioral_witness']['exit_code'] for r in rows], [0, 0, 1, 1, 1, 1])
        for row in rows:
            self.assertEqual(len(row['selected']), 2)
