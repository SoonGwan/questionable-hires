import asyncio
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
    async def test_retention_keeps_transient_fault_after_final_state_recovers(self):
        class TemporarilyPublishesStale(GuardedSearch):
            async def run(self, query, fetch):
                generation = self.generation + 1
                await super().run(query, fetch)
                if generation < self.generation and self.result == 'seed result':
                    self.result = query + ' result'

        default = await asyncio.wait_for(probe.probe(
            TemporarilyPublishesStale, 'run', 'result', 'old', 'new', None), 1)
        self.assertTrue(all(c['passed'] for c in default))
        cases = await asyncio.wait_for(probe.probe(
            TemporarilyPublishesStale, 'run', 'result', 'old', 'new', None,
            retain_while_pending=True), 1)
        failed = next(c for c in cases if c['name'] == 'retain-normal-overlap')
        self.assertFalse(failed['passed'])
        self.assertEqual(failed['observed']['state'], 'new result')
        self.assertEqual(failed['observed']['failed_checkpoints'], [{
            'phase': 'completion', 'query': 'old', 'state': 'old result',
            'expected_state': 'seed result'}])
        self.assertTrue(all(c['passed'] for c in cases if c is not failed))

    async def test_retention_timeout_cleans_owned_overlapping_tasks(self):
        active, finished = [], []

        class WaitsAfterReply(GuardedSearch):
            async def run(self, query, fetch):
                task = asyncio.current_task()
                active.append(task)
                try:
                    await super().run(query, fetch)
                    if self.generation > 1:
                        await asyncio.Event().wait()
                finally:
                    finished.append(task)

        # Do not depend on wait_for creating a separate task: on newer Python
        # the seed may otherwise run in this still-active unittest task.
        sequence_task = asyncio.create_task(probe.sequence(
            WaitsAfterReply, 'run', 'result', ['old', 'new'], [0, 1],
            retain_while_pending=True))
        with self.assertRaises(asyncio.TimeoutError):
            await asyncio.wait_for(sequence_task, 0.05)
        # The seed uses the sequence task; two subsequent calls are owned peers.
        self.assertEqual(len(active), 3)
        self.assertIs(active[0], sequence_task)
        self.assertNotIn(asyncio.current_task(), active)
        self.assertEqual(set(active), set(finished))
        self.assertTrue(all(task.done() for task in active))

    def test_retention_cli_opt_in_preserves_failure_evidence(self):
        source = '''class Search:
    def __init__(self):
        self.result = None
        self.generation = 0
    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        CLEAR_ON_ENTRY
        result = await fetch(query)
        if generation == self.generation:
            self.result = result
'''
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / 'target.py'
            command = [sys.executable, '-B', probe.__file__, '--root', str(root),
                       '--source', 'target.py', '--class-name', 'Search']
            for clear, expected in (('pass', 0), ('self.result = None', 1)):
                target.write_text(source.replace('CLEAR_ON_ENTRY', clear))
                before = target.read_bytes()
                default = subprocess.run(command, capture_output=True, text=True, timeout=5)
                self.assertEqual(default.returncode, 0, default.stdout + default.stderr)
                result = subprocess.run(command + ['--retain-while-pending'],
                                        capture_output=True, text=True, timeout=5)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                evidence = json.loads(result.stdout)
                self.assertTrue(evidence['complete'])
                self.assertEqual(len(evidence['cases']), 4)
                self.assertEqual(result.stderr, '')
                self.assertEqual(target.read_bytes(), before)
                if expected:
                    checkpoint = evidence['cases'][2]['observed']['failed_checkpoints'][0]
                    self.assertEqual(checkpoint, {'phase': 'pending-entry', 'query': 'old',
                                                 'state': None, 'expected_state': 'seed result'})

    async def test_retention_seed_exception_cannot_be_hidden_by_later_success(self):
        class SeedCrash(GuardedSearch):
            async def run(self, query, fetch):
                await super().run(query, fetch)
                if self.generation == 1:
                    raise RuntimeError('seed callback failed')
        cases = await asyncio.wait_for(probe.probe(
            SeedCrash, 'run', 'result', 'old', 'new', None,
            retain_while_pending=True), 1)
        for case in cases[-2:]:
            self.assertFalse(case['passed'])
            self.assertEqual(case['observed']['unexpected_errors'],
                             [{'query': 'old', 'error': 'seed callback failed'}])

    async def test_opt_in_retention_checks_entry_and_older_completion(self):
        class ClearsWhileLoading(GuardedSearch):
            async def run(self, query, fetch):
                self.result = None
                await super().run(query, fetch)

        for factory, expected in ((GuardedSearch, True), (ClearsWhileLoading, False),
                                  (UnsafeSearch, False)):
            cases = await asyncio.wait_for(probe.probe(
                factory, 'run', 'result', 'old', 'new', None,
                retain_while_pending=True), 1)
            retention = [c for c in cases if c['name'].startswith('retain-')]
            self.assertEqual(len(retention), 2)
            self.assertEqual(all(c['passed'] for c in retention), expected)
            if factory is ClearsWhileLoading:
                first = retention[0]['observed']['failed_checkpoints'][0]
                self.assertEqual(first['phase'], 'pending-entry')
                self.assertIsNone(first['state'])
                self.assertEqual(first['expected_state'], 'seed result')
            if factory is UnsafeSearch:
                failure = retention[0]['observed']['failed_checkpoints'][0]
                self.assertEqual(failure['phase'], 'completion')
                self.assertEqual(failure['state'], 'old result')
                self.assertEqual(failure['expected_state'], 'seed result')

    async def test_helper_success_does_not_certify_loading_retention(self):
        class ClearsWhileLoading(GuardedSearch):
            async def run(self, query, fetch):
                self.result = None
                await super().run(query, fetch)

        # A real counterexample to treating the helper's two cases as complete
        # project QA. Neither outcome claims to inspect loading retention.
        cases = await asyncio.wait_for(probe.probe(
            ClearsWhileLoading, 'run', 'result', 'old', 'new', None), 1)
        self.assertTrue(all(case['passed'] for case in cases))

        async def check_retention(factory):
            target = factory()
            async def initial(query):
                return 'existing result'
            await asyncio.wait_for(target.run('seed', initial), 1)
            self.assertEqual(target.result, 'existing result')
            entered = asyncio.Event()
            reply = asyncio.get_running_loop().create_future()
            async def held(query):
                entered.set()
                return await reply
            task = asyncio.create_task(target.run('next', held))
            try:
                await asyncio.wait_for(entered.wait(), 1)
                self.assertFalse(task.done())
                self.assertEqual(target.result, 'existing result')
            finally:
                if not task.done():
                    task.cancel()
                await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
                self.assertTrue(task.done())

        await check_retention(GuardedSearch)
        with self.assertRaisesRegex(AssertionError, "None != 'existing result'"):
            await check_retention(ClearsWhileLoading)

    async def test_result_written_before_success_exception_is_not_a_pass(self):
        class CrashesAfterRender(ErrorSearch):
            async def run(self, query, fetch):
                await super().run(query, fetch)
                if self.error is None:
                    raise RuntimeError('render callback crashed')

        cases = await probe.probe(
            CrashesAfterRender, 'run', 'result', 'old', 'new', None, 'error')
        self.assertFalse(any(c['passed'] for c in cases))
        self.assertEqual(cases[0]['observed']['unexpected_errors'][0],
                         {'query': 'old', 'error': 'render callback crashed'})

    async def test_stale_success_must_preserve_error_as_well_as_result(self):
        class PollutesError(ErrorSearch):
            async def run(self, query, fetch):
                succeeded = False

                async def watched(q):
                    nonlocal succeeded
                    value = await fetch(q)
                    succeeded = True
                    return value

                await super().run(query, watched)
                if succeeded and query == 'old' and self.generation == 2:
                    self.error = 'stale callback error'

        cases = await probe.probe(
            PollutesError, 'run', 'result', 'old', 'new', None, 'error')
        self.assertEqual([c['passed'] for c in cases], [True, False, True, True])

    async def test_normal_success_checks_error_before_later_success_repairs_it(self):
        class TransientError(ErrorSearch):
            async def run(self, query, fetch):
                await super().run(query, fetch)
                if self.generation == 1 and self.result is not None:
                    self.error = 'unexpected error on first success'

        cases = await probe.probe(
            TransientError, 'run', 'result', 'old', 'new', '', 'error')
        self.assertFalse(cases[0]['passed'])
        self.assertIsNone(cases[0]['observed']['error_state'])
        self.assertEqual(cases[0]['observed']['failed_checkpoints'], [{
            'query': 'old', 'state': 'old result', 'expected_state': 'old result',
            'error_state': 'unexpected error on first success', 'expected_error': 'clear'}])
        self.assertFalse(next(c for c in cases if c['name'] == 'normal-boundary')['passed'])
        self.assertTrue(next(c for c in cases if c['name'] == 'current-error-then-recovery')['passed'])

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
