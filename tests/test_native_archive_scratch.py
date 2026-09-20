"""Native tool regressions must not require an ignored developer scratch folder."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class NativeArchiveScratchTests(unittest.TestCase):
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
