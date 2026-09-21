"""Native non-adjacent probe reuse; counts are not model-performance evidence."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('probe_cache', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


class AuditProbeCacheTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        (self.root / 'service.py').write_text('def save(items, value):\n    items.append(value)\n    return True\n')
        (self.root / 'test_service.py').write_text('import unittest\nfrom service import save\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_ack(self): self.assertTrue(save([], "x"))\n')
        self.common = dict(files=['service.py', 'test_service.py'], imports=['service', 'test_service'],
                           tests=['-v', 'test_service'])
        self.fault = dict(target='service.py', old='    items.append(value)\n', new='')

    def recipe(self, labels):
        return dict(self.common, mutations=[dict(self.fault, probe=
            f'from service import save\nitems = []; save(items, {label!r})\nassert items == [{label!r}], repr(items)\n')
            for label in labels])

    def test_native_alternating_probes_keep_all_mutants_and_direct_references(self):
        originals = {p.name: (p.read_bytes(), p.stat().st_mode) for p in self.root.iterdir()}
        for labels, count in [('aab', 9), ('aba', 9), ('abababab', 19)]:
            for repeat in range(2):
                with self.subTest(labels=labels, repeat=repeat):
                    with patch.object(helper, 'execute', wraps=helper.execute) as execute:
                        result = helper.audit_batch(self.root, self.recipe(labels))
                    self.assertEqual(result['status'], 'observed')
                    self.assertEqual(execute.call_count, count)
                    for index, observation in enumerate(result['audits']):
                        checks = observation['checks']
                        self.assertEqual(checks['mutant_tests']['exit_code'], 0)
                        self.assertEqual(checks['mutant_probe']['exit_code'], 1)
                        self.assertIn('AssertionError: []', checks['mutant_probe']['output'])
                        self.assertFalse(checks['mutant_probe']['timed_out'])
                        self.assertFalse(checks['mutant_probe']['output_truncated'])
                        first = labels.index(labels[index])
                        if first < index:
                            self.assertEqual(checks['correct_probe']['observation_ref'],
                                             f'#/audits/{first}/checks/correct_probe')
                        else:
                            self.assertNotIn('correct_probe_reused', observation)
                        self.assertTrue(observation['integrity']['owned_scratch_removed'])
                    self.assertEqual(originals, {p.name: (p.read_bytes(), p.stat().st_mode)
                                                for p in self.root.iterdir()})

    def test_native_context_change_clears_every_probe_entry(self):
        cache = {}
        faults = self.recipe('aba')['mutations']
        for fault in faults[:2]:
            helper.audit(self.root, dict(self.common, **fault), _probe_baseline=cache)
        self.assertEqual(len(cache['entries']), 2)
        source = self.root / 'service.py'
        source.write_text(source.read_text() + '# new input identity\n')
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            result = helper.audit(self.root, dict(self.common, **faults[2]), _probe_baseline=cache)
        self.assertEqual(execute.call_count, 4)
        self.assertNotIn('correct_probe_reused', result)
        self.assertEqual(len(cache['entries']), 1)

    def test_native_replacement_probes_reuse_only_exact_source(self):
        weak = (self.root / 'test_service.py').read_text()
        mutations = []
        for label in 'aba':
            strong = weak.replace('self.assertTrue(save([], "x"))',
                f'items = []; self.assertTrue(save(items, {label!r})); self.assertEqual(items, [{label!r}])')
            mutations.append(dict(self.fault, probe_replacements={'test_service.py': strong},
                                  probe_tests=['-v', 'test_service']))
        with patch.object(helper, 'execute', wraps=helper.execute) as execute:
            report = helper.audit_batch(self.root, dict(self.common, mutations=mutations))
        self.assertEqual(execute.call_count, 9)
        self.assertEqual(report['status'], 'observed')
        self.assertNotIn('correct_probe_reused', report['audits'][1])
        self.assertEqual(report['audits'][2]['checks']['correct_probe']['observation_ref'],
                         '#/audits/0/checks/correct_probe')
        for observation in report['audits']:
            self.assertEqual(observation['checks']['mutant_probe']['exit_code'], 1)
            self.assertIn('AssertionError: Lists differ:', observation['checks']['mutant_probe']['output'])
        self.assertEqual((self.root / 'test_service.py').read_text(), weak)

    def test_cache_retention_budget_evicts_without_reusing_an_evicted_probe(self):
        # Structural cache control, not native execution or a timing measurement.
        cache = {}
        result = dict(exit_code=0, timed_out=False, output='', output_truncated=False)
        probes = ['#' + label * 10_000_001 for label in 'aba']
        with patch.object(helper, 'execute', return_value=result) as execute:
            for index, probe in enumerate(probes):
                cache['index'] = index
                report = helper.audit(self.root, dict(self.common, **self.fault, probe=probe),
                                      _probe_baseline=cache)
                self.assertNotIn('correct_probe_reused', report)
                self.assertEqual(len(cache['entries']), 1)
                self.assertLessEqual(cache['payload_bytes'], 20_000_000)
                self.assertNotIn('context', cache['entries'][0])
        self.assertEqual(execute.call_count, 12)

    def test_probe_entry_limit_keeps_one_shared_source_context(self):
        cache = {}
        result = dict(exit_code=0, timed_out=False, output='', output_truncated=False)
        context = None
        with patch.object(helper, 'execute', return_value=result):
            for index in range(9):
                helper.audit(self.root, dict(self.common, **self.fault, probe=f'assert {index} >= 0'),
                             _probe_baseline=cache)
                if context is None:
                    context = cache['context']
                self.assertIs(cache['context'], context)
        self.assertEqual(len(cache['entries']), 8)
        self.assertEqual(cache['entries'][0]['identity'][0], 'assert 1 >= 0')


if __name__ == '__main__':
    unittest.main()
