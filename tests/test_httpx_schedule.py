import importlib.util
from pathlib import Path
import sys
import unittest
import tempfile
import hashlib
import subprocess
import shutil
import json
import venv
from unittest.mock import patch

directory = Path(__file__).resolve().parents[1] / 'benchmarks'
sys.path.insert(0, str(directory))
try:
    spec = importlib.util.spec_from_file_location('httpx_runner', directory / 'run_httpx.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
finally:
    sys.path.pop(0)


class HTTPXScheduleTests(unittest.TestCase):
    def test_interpreter_directory_alias_normalizes_without_leaving_virtualenv(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            environment = root / 'environment'
            venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
            alias = root / 'alias'
            alias.symlink_to(environment, target_is_directory=True)
            executable = alias / 'bin/python'
            resolved = runner.interpreter_path(executable)
            self.assertEqual(resolved, environment / 'bin/python')
            self.assertTrue(resolved.is_symlink())
            self.assertNotEqual(resolved, resolved.resolve())
            output = subprocess.check_output([str(resolved), '-I', '-B', '-c',
                'import json, sys; print(json.dumps([sys.executable, sys.prefix, sys.base_prefix]))'], text=True)
            actual, prefix, base = json.loads(output)
            self.assertEqual(actual, str(resolved))
            self.assertEqual(Path(prefix), environment)
            self.assertNotEqual(prefix, base)

    def test_cookie_transfer_keeps_existing_profiles_and_exact_cells(self):
        skill, tasks = runner.select_profile('cookies-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'cookies-scoped-clear'})
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('cookies-scoped-clear', 'baseline', 1), ('cookies-scoped-clear', 'skill', 1)})
        self.assertEqual(runner.select_profile('headers-audit'), ('con-artist', runner.HEADER_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('cookies-audit', ['headers-two-boundaries'])

    def test_headers_two_boundary_profile_is_separate(self):
        skill, tasks = runner.select_profile('headers-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'headers-two-boundaries'})
        self.assertEqual(len(runner.make_schedule(tasks, ['baseline', 'skill'], 1)), 2)
        self.assertEqual(runner.select_profile('queryparams-audit'), ('con-artist', runner.QUERYPARAM_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('headers-audit', ['queryparams-repeated-values'])

    def test_queryparams_profile_preserves_decoder_and_prior_schedules(self):
        skill, tasks = runner.select_profile('queryparams-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'queryparams-repeated-values'})
        self.assertEqual(len(runner.make_schedule(tasks, ['baseline', 'skill'], 1)), 2)
        self.assertEqual(runner.select_profile('decoder-audit'), ('con-artist', runner.DECODER_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('queryparams-audit', ['line-crlf-split'])

    def test_decoder_profile_does_not_change_prior_audits(self):
        skill, tasks = runner.select_profile('decoder-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'text-finalization', 'line-crlf-split'})
        self.assertEqual(len(runner.make_schedule(tasks, ['baseline', 'skill'], 1)), 4)
        self.assertEqual(runner.select_profile('audit'), ('con-artist', runner.TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('decoder-audit', ['asgi-head'])

    @classmethod
    def setUpClass(cls):
        temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(temp.cleanup)
        repository = Path(temp.name)
        for name in ('exorcist', 'landlord', 'con-artist'):
            shutil.copytree(runner.ROOT / 'skills' / name, repository / 'skills' / name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        for args in (('init', '-q', '--template='), ('config', 'user.name', 'Snapshot Fixture'),
                     ('config', 'user.email', 'fixture@example.invalid'),
                     ('config', 'commit.gpgsign', 'false'),
                     ('config', 'core.hooksPath', str(repository / 'no-hooks')),
                     ('add', 'skills'), ('commit', '-qm', 'skill snapshot')):
            runner.command(['git', *args], repository)
        override = patch.object(runner, 'ROOT', repository)
        override.start()
        cls.addClassCleanup(override.stop)

    def test_auth_design_is_a_single_isolated_transfer(self):
        skill, tasks = runner.select_profile('auth-design')
        self.assertEqual(skill, 'landlord')
        self.assertEqual(list(tasks), ['auth-flow-design'])
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('auth-flow-design', 'baseline', 1), ('auth-flow-design', 'skill', 1)})
        self.assertEqual(list(runner.select_profile('design')[1]), ['transport-design'])
        with self.assertRaises(ValueError):
            runner.select_profile('auth-design', ['transport-design'])
        with self.assertRaises(ValueError):
            runner.select_profile('design', ['auth-flow-design'])

    def test_diagnosis_profile_is_one_separate_exorcist_case(self):
        skill, tasks = runner.select_profile('diagnosis')
        self.assertEqual(skill, 'exorcist')
        self.assertEqual(list(tasks), ['redirect-auth'])
        self.assertEqual(len(runner.make_schedule(tasks, ['baseline', 'skill'], 1)), 2)
        with self.assertRaises(ValueError):
            runner.select_profile('diagnosis', ['asgi-head'])
        with self.assertRaises(ValueError):
            runner.select_profile('audit', ['redirect-auth'])

    def test_diagnosis_snapshot_contains_current_exorcist_resources(self):
        revision = runner.command(['git', 'rev-parse', 'HEAD'], runner.ROOT)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skill'
            hashes = runner.freeze_skill(runner.ROOT, revision, destination, 'exorcist')
            prefix = 'skills/exorcist/'
            committed = subprocess.check_output(
                ['git', 'ls-tree', '-r', '--name-only', revision, '--', prefix],
                cwd=runner.ROOT, text=True).splitlines()
            self.assertEqual(set(hashes), {name[len(prefix):] for name in committed})
            for name, digest in hashes.items():
                expected = subprocess.check_output(['git', 'show', revision + ':' + prefix + name], cwd=runner.ROOT)
                self.assertEqual((destination / name).read_bytes(), expected)
                self.assertEqual(digest, hashlib.sha256(expected).hexdigest())

    def test_design_profile_is_separate_from_original_audit_schedule(self):
        skill, tasks = runner.select_profile('design')
        self.assertEqual(skill, 'landlord')
        self.assertEqual(list(tasks), ['transport-design'])
        self.assertEqual(runner.select_profile('audit'), ('con-artist', runner.TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('audit', ['transport-design'])
        with self.assertRaises(ValueError):
            runner.select_profile('design', ['wsgi-cleanup'])

    def test_design_snapshot_contains_landlord_not_audit_helper(self):
        revision = runner.command(['git', 'rev-parse', 'HEAD'], runner.ROOT)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skill'
            hashes = runner.freeze_skill(runner.ROOT, revision, destination, 'landlord')
            self.assertEqual(set(hashes), {'SKILL.md', 'agents/openai.yaml'})
            self.assertIn('# Landlord', (destination / 'SKILL.md').read_text())

    def test_snapshot_contains_helpers_and_references_from_commit(self):
        revision = runner.command(['git', 'rev-parse', 'HEAD'], runner.ROOT)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skill'
            hashes = runner.freeze_skill(runner.ROOT, revision, destination)
            for name in ('SKILL.md', 'agents/openai.yaml', 'scripts/audit.py', 'references/python-audit.md'):
                self.assertIn(name, hashes)
                self.assertEqual(hashes[name], hashlib.sha256((destination / name).read_bytes()).hexdigest())
            with self.assertRaises(FileExistsError):
                runner.freeze_skill(runner.ROOT, revision, destination)

    def test_bounded_check_does_not_schedule_other_tasks_or_arms(self):
        self.assertEqual(runner.make_schedule(['wsgi-cleanup'], ['skill', 'skill'], 1),
                         [('wsgi-cleanup', 'skill', 1)])

    def test_original_defaults_keep_twenty_seven_unique_cells(self):
        arms = ['baseline', 'control', 'skill']
        schedule = runner.make_schedule(runner.TASKS, arms, 3)
        expected = {(case, arm, repeat) for case in runner.TASKS
                    for arm in arms for repeat in range(1, 4)}
        self.assertEqual(len(schedule), 27)
        self.assertEqual(set(schedule), expected)
        self.assertEqual(schedule, runner.make_schedule(runner.TASKS, arms, 3))

    def test_invalid_repeat_rejected(self):
        with self.assertRaises(ValueError):
            runner.make_schedule(['wsgi-cleanup'], ['skill'], 0)
