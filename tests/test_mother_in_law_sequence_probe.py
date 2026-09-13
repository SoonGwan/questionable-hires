import importlib.util
import json
from pathlib import Path
import subprocess
import sys
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
    async def test_recovery_detects_sticky_error_missed_by_stale_only_check(self):
        class StickyError(ErrorSearch):
            async def run(self, query, fetch):
                previous = self.error
                await super().run(query, fetch)
                if previous:
                    self.error = previous

        cases = await probe.probe(StickyError, 'run', 'result', 'old', 'new', None, 'error')
        self.assertTrue(cases[-1]['passed'])
        recovery = next(c for c in cases if c['name'] == 'current-error-then-recovery')
        self.assertEqual(recovery['observed']['checkpoints_passed'], [True, False])
        self.assertFalse(recovery['passed'])

    async def test_error_must_be_displayed_and_healthy_recovery_passes(self):
        class SilentError(ErrorSearch):
            async def run(self, query, fetch):
                await super().run(query, fetch)
                self.error = None

        for factory, expected in ((SilentError, False), (ErrorSearch, True)):
            cases = await probe.probe(factory, 'run', 'result', 'old', 'new', None, 'error')
            recovery = next(c for c in cases if c['name'] == 'current-error-then-recovery')
            self.assertEqual(recovery['passed'], expected)
        self.assertTrue(all(c['passed'] for c in cases))

    def test_cli_retains_exact_execution_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'target.py').write_text(
                'class Search:\n'
                '    result = None\n'
                '    async def run(self, query, fetch):\n'
                '        self.result = await fetch(query)\n')
            args = [sys.executable, '-B', probe.__file__, '--root', str(root),
                    '--source', 'target.py', '--class-name', 'Search',
                    '--output', 'evidence.json']
            run = subprocess.run(args, capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 1, run.stderr)
            evidence = root / 'evidence.json'
            original = evidence.read_bytes()
            self.assertEqual(json.loads(original), json.loads(run.stdout))
            self.assertTrue(json.loads(original)['complete'])
            again = subprocess.run(args, capture_output=True, text=True, timeout=10)
            self.assertEqual(again.returncode, 2)
            self.assertFalse(json.loads(again.stdout)['complete'])
            self.assertEqual(evidence.read_bytes(), original)

    def test_cli_rejects_duplicate_boundary_before_running_source(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run(
                [sys.executable, '-B', probe.__file__, '--root', directory,
                 '--source', 'missing.py', '--class-name', 'Search', '--boundary', 'old'],
                capture_output=True, text=True, timeout=10)
            self.assertEqual(run.returncode, 2)
            self.assertIn('queries must differ', json.loads(run.stdout)['error'])

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
