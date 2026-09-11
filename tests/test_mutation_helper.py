import copy
import json
import importlib.util
from pathlib import Path
import tempfile
import subprocess
import sys
import tracemalloc
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mutation_helper', ROOT / 'skills/con-artist/scripts/audit.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class MutationHelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'service.py').write_text('def save(store, value):\n    store.append(value)\n    return True\n')
        (self.root / 'test_service.py').write_text(
            'import unittest\nfrom service import save\n'
            'class Tests(unittest.TestCase):\n'
            '    def test_saved(self):\n        self.assertTrue(save([], "item"))\n')
        self.recipe = dict(files=['service.py', 'test_service.py'], imports=['service'],
                           target='service.py', old='    store.append(value)\n', new='',
                           tests=['-v', 'test_service'],
                           probe='from service import save\ns = ["kept"]\nsave(s, "item")\nassert s == ["kept", "item"]\n')

    def run_audit(self, recipe=None, **kwargs):
        originals = {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()}
        result = helper.audit(self.root, recipe or self.recipe, **kwargs)
        self.assertEqual(originals, {p.name: p.read_bytes() for p in self.root.iterdir() if p.is_file()})
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])
        return result

    def test_survivor_and_same_probe_correct_and_faulty(self):
        result = self.run_audit()
        self.assertEqual(result['status'], 'observed')
        self.assertEqual({k: v['exit_code'] for k, v in result['checks'].items()},
                         dict(correct_tests=0, correct_probe=0, mutant_tests=0, mutant_probe=1))
        self.assertIn('AssertionError', result['checks']['mutant_probe']['output'])

    def test_sensitive_test_needs_no_extra_probe(self):
        p = self.root / 'test_service.py'
        p.write_text(p.read_text().replace('self.assertTrue(save([], "item"))',
                                         's = []; save(s, "item"); self.assertEqual(s, ["item"])'))
        recipe = copy.deepcopy(self.recipe)
        del recipe['probe']
        result = self.run_audit(recipe)
        self.assertEqual(set(result['checks']), {'correct_tests', 'mutant_tests'})
        self.assertEqual(result['checks']['mutant_tests']['exit_code'], 1)

    def test_failed_baseline_stops_before_mutation(self):
        (self.root / 'service.py').write_text('import missing_internal_runtime\n' + (self.root / 'service.py').read_text())
        result = self.run_audit()
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(list(result['checks']), ['correct_tests'])

    def test_broken_proposal_stops_before_mutation(self):
        recipe = dict(self.recipe, probe='assert False')
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(set(result['checks']), {'correct_tests', 'correct_probe'})

    def test_external_import_is_not_accepted(self):
        result = self.run_audit(dict(self.recipe, imports=['json']))
        self.assertEqual(result['status'], 'incomplete')
        self.assertIn('Import escaped copy', result['checks']['correct_tests']['output'])

    def test_syntax_failure_is_not_automatically_called_killed(self):
        result = self.run_audit(dict(self.recipe, new='    broken syntax !!!\n'))
        self.assertIn('SyntaxError', result['checks']['mutant_tests']['output'])
        self.assertIn('not automatically', result['limitation'])

    def test_invalid_mutations_are_rejected_before_copying(self):
        for changes in (dict(old='absent'), dict(old=''), dict(new=self.recipe['old']),
                        dict(target='outside.py'), dict(target='../service.py')):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.run_audit(dict(self.recipe, **changes))
        self.assertEqual(list(self.root.glob('.con-artist-*')), [])

    def test_symlinks_and_path_traversal_rejected(self):
        (self.root / 'alias.py').symlink_to(self.root / 'service.py')
        for name in ('alias.py', '../service.py', '/tmp/service.py', '.', '.git/config'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                helper.snapshot(self.root, [name])

    def test_timeout_is_incomplete_and_copy_is_cleaned(self):
        p = self.root / 'service.py'
        p.write_text('import time\ntime.sleep(10)\n' + p.read_text())
        result = self.run_audit(timeout=0.1)
        self.assertEqual(result['status'], 'incomplete')
        self.assertTrue(result['checks']['correct_tests']['timed_out'])

    def test_each_check_has_fresh_filesystem(self):
        p = self.root / 'test_service.py'
        p.write_text('from pathlib import Path\nPath("side-effect").touch()\n' + p.read_text())
        result = self.run_audit(dict(self.recipe, probe='from pathlib import Path\nassert not Path("side-effect").exists()'))
        self.assertEqual(result['checks']['correct_probe']['exit_code'], 0)
        self.assertEqual(result['checks']['mutant_probe']['exit_code'], 0)

    def test_cli_accepts_stdin_without_a_recipe_file(self):
        result = subprocess.run([sys.executable, str(Path(helper.__file__)), '--spec', '-'],
                                input=json.dumps(self.recipe), cwd=self.root,
                                text=True, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['checks']['mutant_probe']['exit_code'], 1)
        self.assertEqual({p.name for p in self.root.iterdir()}, {'service.py', 'test_service.py'})

    def test_non_object_recipe_is_rejected(self):
        with self.assertRaises(ValueError):
            helper.audit(self.root, [])

    def test_selected_executable_keeps_its_mode_in_copies(self):
        script = self.root / 'fixture.sh'
        script.write_text('#!/bin/sh\nexit 0\n')
        script.chmod(0o755)
        test = self.root / 'test_service.py'
        test.write_text('import subprocess\nsubprocess.run(["./fixture.sh"], check=True)\n' + test.read_text())
        recipe = dict(self.recipe, files=self.recipe['files'] + ['fixture.sh'])
        result = self.run_audit(recipe)
        self.assertEqual(result['status'], 'observed')
        self.assertEqual(result['checks']['correct_tests']['exit_code'], 0)
        self.assertEqual(script.stat().st_mode & 0o777, 0o755)

    def test_large_output_keeps_tail_without_buffering_entire_log(self):
        probe = "import sys\nsys.stdout.write('x' * 8_000_000 + '\\nFINAL RESULT\\n')"
        tracemalloc.start()
        try:
            result = helper.execute(sys.executable, self.root, self.recipe, probe, 5)
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(result['output_truncated'])
        self.assertEqual(len(result['output']), 12000)
        self.assertTrue(result['output'].endswith('\nFINAL RESULT\n'))
        self.assertLess(peak, 2_000_000, 'Parent captured the entire child log')

    def test_non_utf8_output_does_not_lose_exit_status(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nos.write(1, b'bad \\xff byte\\n')\nraise SystemExit(7)", 5)
        self.assertEqual(result['exit_code'], 7)
        self.assertIn('bad \ufffd byte', result['output'])

    def test_continuous_output_still_obeys_deadline(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nwhile True: os.write(1, b'x' * 4096)", 0.2)
        self.assertTrue(result['timed_out'])
        self.assertTrue(result['output_truncated'])
        self.assertLessEqual(len(result['output']), 12000)

    def test_multibyte_output_survives_chunk_boundaries(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os\nos.write(1, ('한' * 9000).encode('utf-8'))", 5)
        self.assertEqual(result['exit_code'], 0)
        self.assertTrue(result['output'].endswith('한' * 9000))
        self.assertNotIn('\ufffd', result['output'])
        self.assertFalse(result['output_truncated'])

    def test_closed_output_does_not_bypass_process_deadline(self):
        result = helper.execute(sys.executable, self.root, self.recipe,
                                "import os, time\nos.close(1)\nos.close(2)\ntime.sleep(10)", 0.2)
        self.assertTrue(result['timed_out'])
        self.assertLess(result['exit_code'], 0)
