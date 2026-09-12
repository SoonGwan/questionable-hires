import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'mother_in_law_sequence_probe',
    ROOT / 'skills/mother-in-law/scripts/sequence_probe.py')
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class UnsafeSearch:
    def __init__(self):
        self.result = None

    async def run(self, query, fetch):
        self.result = await fetch(query)


class GuardedSearch:
    def __init__(self):
        self.result = None
        self.generation = 0

    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        result = await fetch(query)
        if generation == self.generation:
            self.result = result


class ErrorSearch:
    def __init__(self):
        self.result = None
        self.error = None
        self.generation = 0

    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        try:
            result = await fetch(query)
        except RuntimeError as error:
            if generation == self.generation:
                self.error = str(error)
            return
        if generation == self.generation:
            self.result = result
            self.error = None


class MotherInLawSequenceProbeTests(unittest.IsolatedAsyncioTestCase):
    async def test_normal_detects_missing_first_result_hidden_by_overlap(self):
        class DropsFirst(GuardedSearch):
            async def run(self, query, fetch):
                await super().run(query, fetch)
                if self.generation == 1:
                    self.result = None

        cases = await probe.probe(DropsFirst, 'run', 'result', 'old', 'new', None)
        self.assertFalse(cases[0]['passed'])
        self.assertEqual(cases[0]['observed']['checkpoints_passed'], [False, True])
        self.assertTrue(cases[1]['passed'])

    async def test_clear_normal_and_stale_cases_preserve_working_guard(self):
        cases = await probe.probe(GuardedSearch, 'run', 'result', 'old', 'new', '')
        self.assertEqual(len(cases), 4)
        self.assertTrue(all(case['passed'] for case in cases))

    async def test_distinguishes_stale_overwrite_from_guard(self):
        unsafe = await probe.probe(UnsafeSearch, 'run', 'result', 'old', 'new', None)
        guarded = await probe.probe(GuardedSearch, 'run', 'result', 'old', 'new', None)
        self.assertEqual([case['passed'] for case in unsafe], [True, False])
        self.assertEqual([case['passed'] for case in guarded], [True, True])

    async def test_boundary_sequence_is_optional_and_discriminating(self):
        cases = await probe.probe(UnsafeSearch, 'run', 'result', 'old', 'new', '')
        self.assertEqual(cases[-1]['name'], 'older-success-after-boundary')
        self.assertFalse(cases[-1]['passed'])

    async def test_error_state_adds_stale_failure_without_another_harness(self):
        cases = await probe.probe(
            ErrorSearch, 'run', 'result', 'old', 'new', None, 'error')
        self.assertEqual(cases[-1]['name'], 'older-error-after-newer-success')
        self.assertTrue(cases[-1]['passed'])
        self.assertIsNone(cases[-1]['observed']['error_state'])

    def test_loader_rejects_source_outside_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / 'outside.py'
            outside.write_text('class Search: pass')
            try:
                with self.assertRaises(ValueError):
                    probe.load_class(outside, 'Search', root)
            finally:
                outside.unlink()


if __name__ == '__main__':
    unittest.main()
