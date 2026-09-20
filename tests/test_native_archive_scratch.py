"""Native tool regressions must not require an ignored developer scratch folder."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeArchiveScratchTests(unittest.TestCase):
    def test_buffer_and_stale_patch_controls_execute_without_local_runs(self):
        names = ('tests/test_hostage_stale_patch_case.py', 'tests/test_hostage_buffer_runner.py',
                 'tests/native_fixture_support.py', 'tests/runner_snapshot_support.py', 'benchmarks/hostage_stale_patch_case.py',
                 'benchmarks/hostage_buffer_cases.py', 'benchmarks/run_hostage_buffer_01.py',
                 'benchmarks/run.py')
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / 'archive'
            for name in names:
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest',
                                     'test_hostage_stale_patch_case',
                                     'test_hostage_buffer_runner.BufferRunnerTests.test_actual_positive_negative_and_valid_alternative_controls',
                                     '-v'], cwd=archive / 'tests', capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Ran 3 tests', result.stderr)
            self.assertNotIn('skipped', result.stderr)
            self.assertFalse((archive / '.git').exists())
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
            self.assertEqual({p.relative_to(archive): p.read_bytes()
                              for p in archive.rglob('*') if p.is_file()}, before)

    def test_repository_controls_run_in_archive_and_reject_changed_fixture(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / 'archive'
            project = 'benchmarks/results/con-artist-repository-01/baseline/repository-collector-cache--baseline--1/project/'
            names = ('tests/test_con_artist_repository_case.py',
                     'tests/con_artist_fixture_support.py',
                     'benchmarks/con_artist_repository_case.py',
                     project + 'skills/con-artist/scripts/context.py',
                     project + 'tests/test_context_line_index.py')
            for name in names:
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-v']
            passed = subprocess.run(command, cwd=archive, capture_output=True, text=True, timeout=15)
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertIn('Ran 3 tests', passed.stderr)
            self.assertIn('OK (skipped=1)', passed.stderr)
            self.assertRegex(passed.stderr,
                r'test_retained_bytes_match_pinned_project_history_when_available[^\n]*\.\.\. skipped ')
            self.assertRegex(passed.stderr,
                r'test_actual_repository_tests_pass_and_reject_cross_call_cache[^\n]*\.\.\. ok')
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
            fixture = archive / project / 'skills/con-artist/scripts/context.py'
            fixture.write_bytes(fixture.read_bytes() + b'\n# altered retained source\n')
            rejected = subprocess.run(command, cwd=archive, capture_output=True, text=True, timeout=15)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn('Retained repository fixture identity changed', rejected.stderr)

    def test_native_controls_execute_without_git_or_local_runs(self):
        with tempfile.TemporaryDirectory() as scratch:
            archive = Path(scratch) / 'archive'
            names = (
                'tests/test_history_special_files.py',
                'tests/test_owned_tasks_asset.py',
                'tests/test_landlord_scope_cases.py',
                'skills/necromancer/scripts/trace.py',
                'skills/hostage-negotiator/assets/controlled_call.py',
                'skills/hostage-negotiator/assets/controlled_call.mjs',
                'benchmarks/landlord_scope_cases.py',
                'benchmarks/landlord_configured_cases.py',
                'benchmarks/landlord-check-scope-cases.json',
                'benchmarks/korean_auto_cases.py',
                'benchmarks/cases.json',
                'benchmarks/results/all-eight-current-02/current/refresh-owner-a--skill--1/project/test_preview.py',
                'benchmarks/results/all-eight-current-02/current/refresh-owner-a--skill--1/project/preview.py',
                'benchmarks/results/all-eight-current-02/current/refresh-owner-a--skill--1/project/controlled_call.py',
            )
            for name in names:
                target = archive / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / name, target)
            self.assertFalse((archive / '.git').exists())
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
            before = {p.relative_to(archive): p.read_bytes() for p in archive.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
                                     '-s', 'tests', '-v'], cwd=archive,
                                    capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('test_native_fifo_rejected_without_waiting_for_a_writer', result.stderr)
            self.assertIn('test_contract_controls_preserve_originals', result.stderr)
            self.assertNotIn('skipped', result.stderr)
            self.assertFalse((archive / 'benchmarks/local-runs').exists())
            self.assertEqual({p.relative_to(archive): p.read_bytes()
                              for p in archive.rglob('*') if p.is_file()}, before)
