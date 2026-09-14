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
    def test_query_build_diagnosis_keeps_previous_profiles_separate(self):
        skill, tasks = runner.select_profile('query-build-diagnosis')
        self.assertEqual(skill, 'exorcist')
        self.assertEqual(set(tasks), {'query-build'})
        self.assertEqual(runner.select_profile('stream-diagnosis'), ('exorcist', runner.STREAM_DIAGNOSIS_TASKS))
        self.assertEqual(runner.select_profile('queryparams-audit'), ('con-artist', runner.QUERYPARAM_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('query-build-diagnosis', ['queryparams-repeated-values'])

    def test_stream_diagnosis_is_distinct_and_preserves_old_diagnosis(self):
        skill, tasks = runner.select_profile('stream-diagnosis')
        self.assertEqual(skill, 'exorcist')
        self.assertEqual(set(tasks), {'response-preview'})
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('response-preview', 'baseline', 1), ('response-preview', 'skill', 1)})
        self.assertEqual(runner.select_profile('diagnosis'), ('exorcist', runner.DIAGNOSIS_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('stream-diagnosis', ['redirect-auth'])

    def test_main_passes_explicit_persistence_to_each_cell_without_changing_default(self):
        for persist in (False, True):
            with self.subTest(persist=persist), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                source, output = root / 'source', root / 'run'
                source.mkdir()
                def command(args, cwd):
                    if args[:3] == ['git', 'status', '--porcelain']:
                        return ''
                    return runner.REVISION
                def freeze(repository, revision, destination, skill):
                    destination.mkdir(parents=True)
                    (destination / 'SKILL.md').write_text('frozen fixture')
                    return {'SKILL.md': hashlib.sha256(b'frozen fixture').hexdigest()}
                argv = ['run_httpx.py', '--source', str(source), '--python', sys.executable,
                        '--output', str(output), '--profile', 'stream-diagnosis',
                        '--arms', 'baseline', 'skill', '--repeats', '1']
                if persist:
                    argv.append('--persist-session')
                with patch.object(sys, 'argv', argv), patch.object(runner, 'command', side_effect=command), \
                        patch.object(runner, 'freeze_skill', side_effect=freeze), \
                        patch.object(runner, 'disabled_skills', return_value=[]), \
                        patch.object(runner.subprocess, 'run') as native, \
                        patch.object(runner, 'run_cell', return_value={'completed': True}) as cell:
                    runner.main()
                self.assertEqual(cell.call_count, 2)
                self.assertEqual({call.args[1] for call in cell.call_args_list}, {'baseline', 'skill'})
                for call in cell.call_args_list:
                    self.assertIs(call.kwargs['persist_session'], persist)
                    self.assertEqual(call.args[4:7], ('gpt-6-astra', 'medium', 360))
                self.assertEqual(native.call_count, 1)
                self.assertEqual(native.call_args.args[0][-2:],
                                 ['tests/models/test_responses.py::test_read',
                                  'tests/models/test_responses.py::test_iter_bytes'])
                manifest = json.loads((output / 'run.json').read_text())
                self.assertIs(manifest['session_persistence_requested'], persist)
                self.assertEqual(len(manifest['completed_cells']), 2)

    def test_cookie_design_is_distinct_and_preserves_audit_profile(self):
        skill, tasks = runner.select_profile('cookie-design')
        self.assertEqual(skill, 'landlord')
        self.assertEqual(set(tasks), {'cookie-storage-design'})
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('cookie-storage-design', 'baseline', 1), ('cookie-storage-design', 'skill', 1)})
        self.assertEqual(runner.select_profile('cookies-audit'), ('con-artist', runner.COOKIE_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('cookie-design', ['cookies-scoped-clear'])

    def test_header_equality_profile_keeps_prior_boundary_audit(self):
        skill, tasks = runner.select_profile('header-equality-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'headers-duplicate-equality'})
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('headers-duplicate-equality', 'baseline', 1),
                          ('headers-duplicate-equality', 'skill', 1)})
        self.assertEqual(runner.select_profile('headers-audit'), ('con-artist', runner.HEADER_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('header-equality-audit', ['headers-two-boundaries'])

    def test_url_repr_profile_is_new_and_preserves_prior_tasks(self):
        skill, tasks = runner.select_profile('url-repr-audit')
        self.assertEqual(skill, 'con-artist')
        self.assertEqual(set(tasks), {'url-repr-password'})
        self.assertEqual(set(runner.make_schedule(tasks, ['baseline', 'skill'], 1)),
                         {('url-repr-password', 'baseline', 1), ('url-repr-password', 'skill', 1)})
        self.assertEqual(runner.select_profile('cookies-audit'), ('con-artist', runner.COOKIE_TASKS))
        with self.assertRaises(ValueError):
            runner.select_profile('url-repr-audit', ['cookies-scoped-clear'])

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
        for name in ('exorcist', 'landlord', 'con-artist', 'receipt'):
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

    def test_receipt_snapshot_contains_all_committed_resources(self):
        revision = runner.command(['git', 'rev-parse', 'HEAD'], runner.ROOT)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'skill'
            hashes = runner.freeze_skill(runner.ROOT, revision, destination, 'receipt')
            prefix = 'skills/receipt/'
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
