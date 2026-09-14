import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
import shutil

spec = importlib.util.spec_from_file_location("runner", Path(__file__).resolve().parents[1] / "benchmarks/run.py")
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class BenchmarkRunnerTests(unittest.TestCase):
    def test_retained_programmatic_runner_partial_capture_is_reviewable(self):
        path = runner.ROOT / 'benchmarks/results/reporter-diagnosis-01/reporter-lifecycle--skill--1/commands.json'
        item = next(c for c in json.loads(path.read_text()) if c['id'] == 'item_8')
        before = json.dumps(item, sort_keys=True)
        candidate = runner.unittest_transcript_candidate(item)
        self.assertIsNotNone(candidate)
        self.assertEqual((candidate['reported_tests'], candidate['observed_verbose_headers']), (4, 1))
        self.assertIn('manual review', candidate['interpretation'])
        self.assertEqual(json.dumps(item, sort_keys=True), before)

    def test_cli_streams_survive_post_execution_git_failure(self):
        with tempfile.TemporaryDirectory(dir=runner.ROOT) as directory:
            root = Path(directory)
            output = root / 'results'
            output.mkdir()
            stdout = json.dumps(dict(type='turn.completed', usage=dict(input_tokens=1,
                                                                       output_tokens=1))) + '\n'
            stderr = 'retained diagnostic: 한글\n'
            actual_popen = runner.subprocess.Popen

            def launch(args, **kwargs):
                if args[0] != 'codex':
                    return actual_popen(args, **kwargs)
                workspace = Path(args[args.index('-C') + 1])
                # Preserve Git data in this disposable fixture, but make the
                # author's subsequent git-add fail after the child has exited.
                producer = ('import pathlib, sys; p = pathlib.Path(' + repr(str(workspace)) +
                            '); (p / ".git").rename(p / "saved-git"); '
                            '(p / ".git").write_text("gitdir: missing-fixture-git\\n"); '
                            'sys.stdout.write(' + repr(stdout) + '); '
                            'sys.stderr.write(' + repr(stderr) + ')')
                return actual_popen([sys.executable, '-c', producer], **kwargs)

            with patch.object(runner.subprocess, 'Popen', side_effect=launch):
                with self.assertRaises(runner.subprocess.CalledProcessError) as caught:
                    runner.run_cell(dict(id='postprocess', skill='exorcist', task='Fixture',
                                         files={'source.py': 'VALUE = 1\n'}),
                                    'baseline', 1, output, 'gpt-6-astra', 'medium', 10, [],
                                    workspace_root=root / 'workspaces')
            self.assertEqual(caught.exception.cmd, ['git', 'add', '-N', '.'])
            cell = output / 'postprocess--baseline--1'
            self.assertEqual((cell / 'stdout.original.jsonl').read_text(), stdout)
            self.assertEqual((cell / 'stderr.original.txt').read_text(), stderr)
            self.assertEqual((cell / 'events.jsonl').read_text(), stdout)
            self.assertEqual((cell / 'stderr.txt').read_text(), stderr)
            self.assertFalse((cell / 'metadata.json').exists())

    def test_node_summary_review_finds_retained_gap_without_changing_evidence(self):
        path = runner.ROOT / 'benchmarks/results/hostage-entry-wait-model-01/javascript-preview-latest--skill--1/events.jsonl'
        before = path.read_bytes()
        events, diagnostic = runner.inspect_capture(before.decode(), '')
        self.assertEqual([row['item_id'] for row in diagnostic['node_missing_summary_review_candidates']],
                         ['item_8'])
        self.assertEqual(events, [json.loads(line) for line in before.decode().splitlines()])
        self.assertEqual(path.read_bytes(), before)

    @unittest.skipUnless(shutil.which('node'), 'Native Node reporters are required')
    def test_node_summary_review_accepts_native_pass_fail_and_empty_files(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'checks.test.mjs'
            for reporter in ('tap', 'spec'):
                for failing in (False, True):
                    source.write_text("import test from 'node:test';\nimport assert from 'node:assert/strict';\n"
                                      + "test('identity', () => assert.equal('actual', "
                                      + ("'expected'" if failing else "'actual'") + "));\n")
                    process = runner.subprocess.run(['node', '--test', '--test-reporter=' + reporter,
                                                     str(source)], capture_output=True, text=True, timeout=10)
                    self.assertEqual(process.returncode, int(failing))
                    output = process.stdout + process.stderr
                    if failing:
                        self.assertIn('actual', output)
                        self.assertIn('expected', output)
                    item = dict(type='command_execution', id='native', command='node --test',
                                aggregated_output=output, exit_code=process.returncode)
                    def inspect(value):
                        events, diagnostics = runner.inspect_capture(json.dumps(
                            dict(type='item.completed', item=value)), '')
                        self.assertEqual(events[0]['item'], value)
                        return diagnostics['node_missing_summary_review_candidates']
                    self.assertEqual(inspect(item), [])
                    self.assertEqual(len(inspect(dict(item, aggregated_output=output.splitlines()[0]))), 1)
            source.write_text('// no tests\n')
            process = runner.subprocess.run(['node', '--test', '--test-reporter=tap', str(source)],
                                            capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0)
            self.assertEqual(inspect(dict(item, aggregated_output=process.stdout)), [])

    def test_node_summary_review_is_not_a_shell_or_test_result_verdict(self):
        def inspect(command, output=''):
            item = dict(type='command_execution', id='probe', command=command,
                        aggregated_output=output, exit_code=0)
            return runner.inspect_capture(json.dumps(dict(type='item.completed', item=item)), '')[1][
                'node_missing_summary_review_candidates']
        for command in ('node --test > results.log', 'false && node --test; git status --short',
                        'node --test --test-reporter=dot', "echo 'node --test'"):
            self.assertEqual(len(inspect(command)), 1)
        for command in ('node --test-only', 'node --test-reporter=tap', 'my-node --test', 'cp support.mjs copy.mjs'):
            self.assertEqual(inspect(command), [])
        summary = ''.join(f'ℹ {field} 0\n' for field in ('tests', 'pass', 'fail', 'cancelled', 'skipped'))
        self.assertEqual(inspect('node --test', summary), [])
        self.assertEqual(inspect('node --test', '\x1b[32m' + summary + '\x1b[0m'), [])
        self.assertEqual(len(inspect('node --test', 'ℹ tests 4\nℹ pass 4\n')), 1)

    def test_missing_test_summary_flags_retained_native_gap_without_rescoring(self):
        path = runner.ROOT / 'benchmarks/results/hostage-call-model-01/necessary-state--skill--1/events.jsonl'
        raw = path.read_text()
        events, diagnostic = runner.inspect_capture(raw, '')
        self.assertEqual(events, [json.loads(line) for line in raw.splitlines()])
        flagged = diagnostic['unittest_missing_summary_review_candidates']
        self.assertEqual([row['item_id'] for row in flagged], ['item_8'])
        item = next(e['item'] for e in events if e.get('type') == 'item.completed'
                    and e.get('item', {}).get('id') == 'item_8')
        self.assertEqual(item['exit_code'], 0)
        self.assertIn('diff --git', item['aggregated_output'])
        self.assertTrue(any(e['type'] == 'turn.completed' for e in events))

    def test_missing_summary_distinguishes_review_from_proven_capture_loss(self):
        def inspect(output, command='python3 -m unittest -v; git status --short', status=0):
            item = dict(type='command_execution', id='probe', command=command,
                        aggregated_output=output, exit_code=status)
            _, diagnostics = runner.inspect_capture(json.dumps(dict(type='item.completed', item=item)), '')
            return diagnostics['unittest_missing_summary_review_candidates']
        self.assertEqual(inspect('Ran 1 test in 0.001s\n\nOK\n'), [])
        self.assertEqual(inspect('Ran 0 tests in 0.000s\n\nOK\n'), [])
        self.assertEqual(inspect('Ran 2 tests in 0.001s\n\nFAILED (failures=1)\n', status=1), [])
        for output, command in [('', 'python3 -m unittest -v > saved.log 2>&1'),
                                ('M form.py\n', 'false && python3 -m unittest -v; git status --short'),
                                ('ImportError: missing support\n', 'python3 -m unittest -v')]:
            self.assertEqual(len(inspect(output, command)), 1)
        self.assertEqual(inspect('', 'cp helper.py tests/helper.py'), [])
        self.assertEqual(inspect('', 'python3 -m unittest_extra -v'), [])

    def test_verbose_capture_review_uses_real_native_output_without_scoring_failure(self):
        source = '''import unittest
class Checks(unittest.TestCase):
    def test_first(self): self.assertEqual(1, 1)
    def test_second(self): self.assertEqual("actual", "expected")
    def test_third(self): self.assertTrue(True)
unittest.main(verbosity=2)
'''
        process = runner.subprocess.run([sys.executable, '-c', source],
                                        text=True, capture_output=True, timeout=10)
        self.assertEqual(process.returncode, 1)
        self.assertIn('AssertionError', process.stderr)
        item = dict(type='command_execution', id='native',
                    command='python3 -m unittest -v', aggregated_output=process.stderr,
                    exit_code=process.returncode)
        def inspect(value):
            raw = json.dumps(dict(type='item.completed', item=value))
            events, diagnostics = runner.inspect_capture(raw, '')
            self.assertEqual(events[0]['item'], value)
            self.assertEqual(diagnostics['unittest_missing_summary_review_candidates'], [])
            return diagnostics['unittest_transcript_review_candidates']
        self.assertEqual(inspect(item), [])
        partial = dict(item, aggregated_output=process.stderr[process.stderr.index('test_third'):])
        candidates = inspect(partial)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0]['reported_tests'], 3)
        self.assertEqual(candidates[0]['observed_verbose_headers'], 1)
        self.assertEqual(partial['exit_code'], 1)
        self.assertEqual(len(inspect(dict(partial, command='python3 -m unittest -q'))), 1)
        self.assertEqual(len(inspect(dict(partial, command='python3 report.py'))), 1)
        # Actual quiet native output has no verbose headers, unlike the changed
        # command labels above; no claim about completeness follows from silence.
        quiet = runner.subprocess.run([sys.executable, '-c', source.replace('verbosity=2', 'verbosity=0')],
                                      text=True, capture_output=True, timeout=10)
        self.assertEqual(quiet.returncode, 1)
        self.assertEqual(inspect(dict(item, command='python3 report.py', aggregated_output=quiet.stderr)), [])
        self.assertEqual(inspect(dict(item, command='python3 report.py')), [])
        self.assertEqual(inspect(dict(partial, aggregated_output=process.stderr * 2)), [])

    def test_partial_success_summary_is_review_candidate_not_failure(self):
        item = dict(type='command_execution', id='partial',
                    command='python3 -m unittest --verbose', exit_code=0,
                    aggregated_output='ok\ntest_last (checks.C) ... ok\n\nRan 6 tests in 0.033s\n\nOK\n')
        candidate = runner.unittest_transcript_candidate(item)
        self.assertEqual((candidate['reported_tests'], candidate['observed_verbose_headers']), (6, 1))
        self.assertEqual(item['exit_code'], 0)
        self.assertIsNone(runner.unittest_transcript_candidate(dict(item, aggregated_output='')))

    def test_working_overlay_stays_uncommitted_and_model_diff_excludes_it(self):
        case = dict(id='dirty', skill='receipt', task='Verify only',
                    files={'rule.py': 'VALUE = "old"\n', '.gitignore': 'ignored.txt\n'},
                    working_files={'rule.py': 'VALUE = "fixed"\n', 'test_new.py': '# supplied\n',
                                   'ignored.txt': 'initial ignored content\n'})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output, workspaces = root / 'results', root / 'workspaces'
            output.mkdir()
            original_popen = runner.subprocess.Popen
            def dispatch(args, **kwargs):
                if args[0] != 'codex':
                    return original_popen(args, **kwargs)
                project = Path(args[args.index('-C') + 1])
                self.assertEqual((project / 'rule.py').read_text(), 'VALUE = "fixed"\n')
                self.assertEqual(runner.command(['git', 'show', 'HEAD:rule.py'], project), 'VALUE = "old"')
                self.assertEqual(runner.command(['git', 'diff', '--cached'], project), '')
                self.assertEqual(runner.command(['git', 'rev-list', '--count', 'HEAD'], project), '1')
                self.assertIn('?? test_new.py', runner.command(['git', 'status', '--short'], project))
                event = json.dumps(dict(type='turn.completed', usage=dict(input_tokens=1, output_tokens=1)))
                return original_popen([sys.executable, '-c', 'print(' + repr(event) + ')'], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=dispatch):
                meta = runner.run_cell(case, 'baseline', 1, output, 'gpt-6-astra',
                                       'medium', 10, [], workspace_root=workspaces)
            cell = output / 'dirty--baseline--1'
            self.assertTrue(meta['completed'])
            self.assertEqual((cell / 'changes.diff').read_text().strip(), '')
            initial = (cell / 'initial.diff').read_text()
            self.assertIn('+VALUE = "fixed"', initial)
            self.assertIn('+# supplied', initial)
            self.assertIn('+initial ignored content', initial)
            self.assertEqual(set(meta['initial_working_files']), set(case['working_files']))
            # Execute the actual exporter too; this initial-state evidence must
            # survive export rather than becoming a claimed model change.
            export_spec = importlib.util.spec_from_file_location('export_dirty', runner.ROOT / 'benchmarks/export.py')
            exporter = importlib.util.module_from_spec(export_spec)
            export_spec.loader.exec_module(exporter)
            (output / 'run.json').write_text('{}')
            exporter.export(output, root / 'export')
            self.assertEqual((root / 'export/dirty--baseline--1/initial.diff').read_text(), initial)
            self.assertEqual((root / 'export/dirty--baseline--1/changes.diff').read_text().strip(), '')

    def test_overlay_paths_reject_before_creating_repository(self):
        for working in ({'../escape': 'x'}, {'.git/config': 'x'}, {'.agents/skills/a': 'x'},
                        {'./rule.py': 'x'}, {'rule.py': None}, [], {'': 'x'}):
            with self.subTest(working=working), tempfile.TemporaryDirectory() as directory:
                workspace = Path(directory) / 'project'
                with self.assertRaises(ValueError):
                    runner.prepare(dict(files={'rule.py': 'old'}, working_files=working), workspace)
                self.assertFalse(workspace.exists())

    def test_overlay_diff_retains_agent_edits_and_deletion_of_initial_ignored_file(self):
        case = dict(id='edit', skill='receipt', task='Fixture',
                    files={'rule.py': 'original\n', '.gitignore': 'ignored.txt\n'},
                    working_files={'rule.py': 'user change\n', 'ignored.txt': 'user scratch\n'})
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'results'
            output.mkdir()
            original_popen = runner.subprocess.Popen
            def dispatch(args, **kwargs):
                if args[0] != 'codex':
                    return original_popen(args, **kwargs)
                project = Path(args[args.index('-C') + 1])
                (project / 'rule.py').write_text('agent change\n')
                (project / 'ignored.txt').unlink()
                event = json.dumps(dict(type='turn.completed', usage=dict(input_tokens=1, output_tokens=1)))
                return original_popen([sys.executable, '-c', 'print(' + repr(event) + ')'], **kwargs)
            with patch.object(runner.subprocess, 'Popen', side_effect=dispatch):
                runner.run_cell(case, 'baseline', 1, output, 'gpt-6-astra', 'medium', 10,
                                [], workspace_root=root / 'workspaces')
            diff = (output / 'edit--baseline--1/changes.diff').read_text()
            self.assertIn('-user change', diff)
            self.assertIn('+agent change', diff)
            self.assertIn('-user scratch', diff)
            self.assertNotIn('-original', diff)

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
            self.assertEqual(manifest['skill_resources_sha256']['exorcist'],
                             runner.resource_digest(snapshot / 'exorcist'))

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
