import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys

spec = importlib.util.spec_from_file_location("runner", Path(__file__).resolve().parents[1] / "benchmarks/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class BenchmarkRunnerTests(unittest.TestCase):
    def test_resource_manifest_covers_references_scripts_modes_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'references').mkdir()
            (root / 'SKILL.md').write_text('entrypoint')
            (root / 'references/check.py').write_text('print(1)')
            (root / 'outside').symlink_to('/does-not-exist')
            first = runner.resource_manifest(root)
            self.assertEqual(first['outside'], dict(kind='symlink', target='/does-not-exist'))
            (root / 'references/check.py').write_text('print(2)')
            (root / 'references/check.py').chmod(0o755)
            second = runner.resource_manifest(root)
            self.assertEqual(first['SKILL.md'], second['SKILL.md'])
            self.assertNotEqual(first['references/check.py']['sha256'], second['references/check.py']['sha256'])
            self.assertEqual(second['references/check.py']['mode'], 0o755)

    def test_resource_manifest_does_not_follow_replaced_install_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root / 'outside'
            outside.mkdir()
            (outside / 'secret').write_text('not inventoried')
            linked = root / 'linked'
            linked.symlink_to(outside, target_is_directory=True)
            self.assertEqual(set(runner.resource_manifest(linked)), {'.'})
            self.assertEqual(set(runner.resource_manifest(linked / 'skills')), {'.'})

    def test_cell_records_installed_resource_mutation_without_changing_completion(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'skills/exorcist'
            source.mkdir(parents=True)
            (source / 'SKILL.md').write_text('frozen skill')
            (source / 'helper.py').write_text('original')
            output = root / 'results'
            output.mkdir()
            temporary = root / 'temp'
            temporary.mkdir()
            original_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                target = temporary / 'project/.agents/skills/exorcist/helper.py'
                target.write_text('changed during execution')
                event = json.dumps(dict(type='turn.completed', usage=dict(input_tokens=1, output_tokens=1)))
                return original_popen([sys.executable, '-c', 'print(' + repr(event) + ')'], **kwargs)
            # Fixture preparation also uses Popen; only intercept the model command.
            def dispatch(args, **kwargs):
                return launch(args, **kwargs) if args[0] == 'codex' else original_popen(args, **kwargs)
            with patch.object(runner.tempfile, 'mkdtemp', return_value=str(temporary)), patch.object(runner.subprocess, 'Popen', side_effect=dispatch):
                meta = runner.run_cell(dict(id='resources', skill='exorcist', task='Fixture', files={'source.py': 'VALUE=1'}),
                                       'skill', 1, output, 'gpt-6-astra', 'medium', 10, [], root / 'skills')
            self.assertTrue(meta['completed'])
            self.assertEqual(meta['resource_diagnostics']['changed_paths'], ['exorcist/helper.py'])
            self.assertEqual(meta['installed_resources_before']['exorcist/helper.py']['sha256'], runner.hashlib.sha256(b'original').hexdigest())
            self.assertEqual((source / 'helper.py').read_text(), 'original')

    def test_capture_diagnostics_do_not_conflate_empty_output_and_failure(self):
        rows = [dict(type='item.completed', item=dict(type='command_execution', id='empty',
                                                    aggregated_output='', exit_code=0)),
                dict(type='item.completed', item=dict(type='command_execution', id='failure',
                                                    aggregated_output='expected assertion', exit_code=1)),
                dict(type='error', message='example')]
        raw = '\n'.join(json.dumps(row) for row in rows) + '\nnot JSON\n[]\n'
        events, diagnostics = runner.inspect_capture(raw, 'patch rejected: example')
        self.assertEqual(events, rows)
        self.assertEqual(diagnostics['invalid_json_lines'], [4])
        self.assertEqual(diagnostics['non_object_json_lines'], [5])
        self.assertEqual(diagnostics['empty_command_output_items'], ['empty'])
        self.assertEqual(diagnostics['error_event_types'], ['error'])
        self.assertEqual(diagnostics['patch_rejection_count'], 1)

    def test_full_cell_preserves_cli_capture_and_multiline_command_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'results'
            output.mkdir()
            temporary = root / 'temporary'
            temporary.mkdir()
            workspace = temporary / 'project'
            command_output = 'first failure section\n한글\nlast success section\n'
            rows = [dict(type='item.completed', item=dict(type='command_execution',
                    id='probe', aggregated_output=command_output, exit_code=0)),
                    dict(type='turn.completed', usage=dict(input_tokens=5, output_tokens=2))]
            stdout = '\n'.join(json.dumps(row, ensure_ascii=False) for row in rows) + '\n'
            stderr = 'patch rejected: diagnostic fixture\n'
            actual_popen = runner.subprocess.Popen
            def launch(args, **kwargs):
                if args[0] == 'codex':
                    self.assertEqual(args[args.index('-C') + 1], str(workspace.resolve()))
                    producer = ('import sys; sys.stdout.write(' + repr(stdout) +
                                '); sys.stderr.write(' + repr(stderr) + ')')
                    return actual_popen([sys.executable, '-c', producer], **kwargs)
                return actual_popen(args, **kwargs)
            with patch.object(runner.tempfile, 'mkdtemp', return_value=str(temporary)), \
                 patch.object(runner.subprocess, 'Popen', side_effect=launch):
                meta = runner.run_cell(dict(id='capture', skill='exorcist', task='Fixture',
                    files={'source.py': 'VALUE = 1\n'}), 'baseline', 1, output,
                    'gpt-6-astra', 'medium', 10, [])
            cell = output / 'capture--baseline--1'
            self.assertEqual((cell / 'stdout.original.jsonl').read_text(), stdout)
            self.assertEqual((cell / 'stderr.original.txt').read_text(), stderr)
            emitted = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            self.assertEqual(emitted[0]['item']['aggregated_output'], command_output)
            self.assertEqual(meta['capture_diagnostics']['patch_rejection_count'], 1)
            self.assertTrue(meta['completed'])  # completion is not a quality/capture score
            self.assertEqual((cell / 'project/source.py').read_text(), 'VALUE = 1\n')

    def test_symlinked_temporary_root_has_one_physical_workspace_for_all_arms(self):
        for arm in ('baseline', 'control', 'skill', 'auto'):
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as directory:
                root = Path(directory).resolve()
                physical = root / 'physical'
                physical.mkdir()
                alias = root / 'alias'
                alias.symlink_to(physical, target_is_directory=True)
                output = root / 'results'
                output.mkdir()
                source = root / 'skills/example'
                source.mkdir(parents=True)
                (source / 'SKILL.md').write_text('Example fixture skill')
                actual_popen = runner.subprocess.Popen

                def launch(args, **kwargs):
                    if args[0] == 'codex':
                        workspace = Path(args[args.index('-C') + 1])
                        self.assertEqual(workspace, physical / 'project')
                        self.assertEqual(workspace.resolve(), workspace)
                        self.assertTrue(workspace.samefile(alias / 'project'))
                        self.assertEqual(args[args.index('--sandbox') + 1], 'workspace-write')
                        self.assertNotIn('--add-dir', args)
                        event = json.dumps(dict(type='turn.completed', usage=dict(input_tokens=1, output_tokens=1)))
                        return actual_popen([sys.executable, '-c', 'print(' + repr(event) + ')'], **kwargs)
                    return actual_popen(args, **kwargs)

                with patch.object(runner.tempfile, 'mkdtemp', return_value=str(alias)), \
                     patch.object(runner.subprocess, 'Popen', side_effect=launch):
                    meta = runner.run_cell(dict(id='canonical', skill='example', task='Fixture',
                        files={'source.py': 'VALUE = 1\n'}), arm, 1, output,
                        'gpt-6-astra', 'medium', 10, [], root / 'skills')
                self.assertEqual(meta['workspace'], str(physical / 'project'))
                self.assertEqual(meta['allocated_workspace'], str(alias / 'project'))
                self.assertTrue(meta['completed'])
                self.assertEqual(meta['installed_resources_before'], meta['installed_resources_after'])
                self.assertEqual((output / ('canonical--' + arm + '--1') / 'project/source.py').read_text(), 'VALUE = 1\n')

    def test_upstream_copy_preserves_history_without_sharing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source'
            copied = Path(directory) / 'copy'
            case = dict(files={'module.py': 'VALUE = 1\n', 'LICENSE': 'upstream license\n'})
            original = runner.prepare(case, source)
            self.assertEqual(runner.prepare_repository(source, copied), original)
            self.assertEqual((copied / 'LICENSE').read_text(), 'upstream license\n')
            (copied / 'module.py').write_text('VALUE = 2\n')
            self.assertEqual((source / 'module.py').read_text(), 'VALUE = 1\n')
            self.assertNotEqual((source / '.git/config').stat().st_ino, (copied / '.git/config').stat().st_ino)
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], source), '')

    def test_custom_case_ids_rejected_before_output_creation(self):
        for identity in ('../escape', '/tmp/escape', ''):
            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / 'cases.json'
                source.write_text(json.dumps([dict(id=identity, skill='exorcist')]))
                output = Path(directory) / 'output'
                with patch.object(sys, 'argv', ['run.py', '--output', str(output), '--cases-file', str(source)]):
                    with self.assertRaises(SystemExit):
                        runner.main()
                self.assertFalse(output.exists())

    def test_custom_suite_passes_snapshot_without_touching_live_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'cases.json'
            source.write_text(json.dumps([dict(id='new-domain', skill='exorcist', task='Diagnose', files={})]))
            snapshot = root / 'snapshot'
            (snapshot / 'exorcist').mkdir(parents=True)
            (snapshot / 'exorcist/SKILL.md').write_text('Frozen candidate')
            output = root / 'output'
            argv = ['run.py', '--output', str(output), '--cases-file', str(source), '--skills-root', str(snapshot), '--arms', 'skill']
            with patch.object(sys, 'argv', argv), patch.object(runner, 'run_cell', return_value=dict(completed=True)) as run, patch.object(runner, 'command', return_value='test'), patch.object(runner, 'disabled_skills', return_value=[]):
                runner.main()
            self.assertEqual(run.call_args.args[-1], snapshot.resolve())
            manifest = json.loads((output / 'run.json').read_text())
            self.assertEqual(manifest['suite'], 'custom')
            self.assertEqual(manifest['case_ids'], ['new-domain'])
            self.assertEqual(manifest['skill_snapshot_sha256']['exorcist'], runner.hashlib.sha256(b'Frozen candidate').hexdigest())

    def test_jobs_above_three_rejected_without_launch(self):
        with patch.object(sys, 'argv', ['run.py', '--output', '/tmp/unused', '--jobs', '4']):
            with self.assertRaises(SystemExit) as raised:
                runner.main()
            self.assertEqual(raised.exception.code, 2)

    def test_account_limit_records_remaining_schedule_without_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'run'
            def limited(case, arm, repeat, out, *args):
                cell = out / f"{case['id']}--{arm}--{repeat}"
                cell.mkdir()
                meta = dict(case=case['id'], arm=arm, repeat=repeat, completed=False, limit_detected=True)
                (cell / 'metadata.json').write_text(json.dumps(meta))
                return meta
            argv = ['run.py', '--output', str(output), '--jobs', '1', '--repeats', '3']
            with patch.object(sys, 'argv', argv), patch.object(runner, 'run_cell', side_effect=limited) as run, patch.object(runner, 'command', return_value='test'), patch.object(runner, 'disabled_skills', return_value=[]):
                with self.assertRaises(SystemExit):
                    runner.main()
            self.assertEqual(run.call_count, 1)
            rows = [json.loads(p.read_text()) for p in output.glob('*--*/metadata.json')]
            self.assertEqual(len(rows), 72)
            self.assertEqual(sum(r.get('attempted') is False for r in rows), 71)
            manifest = json.loads((output / 'run.json').read_text())
            self.assertTrue(manifest['stopped_after_limit'])
            self.assertEqual(len(set(manifest['schedule'])), 72)

    def test_fixture_paths_cannot_escape_workspace(self):
        for name in ("../escape.py", "/tmp/escape.py", ".git/config"):
            with tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / "project"
                with self.assertRaises(ValueError):
                    runner.prepare({"files": {name: "bad"}}, workspace)
                self.assertFalse(workspace.exists())

    def test_every_hire_has_a_neutral_task(self):
        cases = json.loads((runner.ROOT / "benchmarks/cases.json").read_text())
        actual = {c["skill"] for c in cases}
        expected = {p.parent.name for p in (runner.ROOT / "skills").glob("*/SKILL.md")}
        self.assertEqual(actual, expected)
        self.assertEqual(len({c["id"] for c in cases}), len(cases))

    def test_history_preparation_is_identical_between_arms(self):
        case = json.loads((runner.ROOT / "benchmarks/cases.json").read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            first = Path(directory) / "first"
            second = Path(directory) / "second"
            self.assertEqual(runner.prepare(case, first), runner.prepare(case, second))
            for name, expected in case["files"].items():
                self.assertEqual((first / name).read_text(), expected)
            self.assertFalse((first / "criteria.json").exists())
            self.assertEqual(runner.command(["git", "rev-list", "--count", "HEAD"], first), "2")


if __name__ == "__main__":
    unittest.main()
