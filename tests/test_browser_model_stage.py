import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
try:
    spec = importlib.util.spec_from_file_location('browser_model_stage', ROOT / 'benchmarks/run_browser_model.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
finally:
    sys.path.pop(0)


class BrowserModelStageTests(unittest.TestCase):
    def test_container_launcher_translates_workspace_and_keeps_auth_out_of_image(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            auth = root / 'auth.json'
            auth.write_text('{}')
            workspace = root / 'project'
            launch = runner.container_launcher('test-context', 'test-image', auth)
            command = launch(workspace, [
                'codex', 'exec', '--sandbox', 'workspace-write', '-C',
                str(workspace), 'prompt',
            ])
        self.assertEqual(command[:5], ['docker', '--context', 'test-context', 'run', '--rm'])
        self.assertIn('test-image', command)
        self.assertIn(f'{auth.resolve()}:/run/codex-auth.json:ro', command)
        self.assertIn(f'{workspace}:/work:rw', command)
        self.assertIn('--dangerously-bypass-approvals-and-sandbox', command)
        self.assertNotIn('--sandbox', command)
        self.assertIn('/work', command)
        self.assertNotIn(str(workspace), command[command.index('test-image') + 1:])
        self.assertTrue(any('test -f /work/README.md' in value for value in command))

    def test_container_launcher_rejects_missing_or_linked_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            missing = root / 'missing.json'
            with self.assertRaises(ValueError):
                runner.container_launcher('context', 'image', missing)
            auth = root / 'auth.json'
            auth.write_text('{}')
            linked = root / 'linked.json'
            linked.symlink_to(auth)
            with self.assertRaises(ValueError):
                runner.container_launcher('context', 'image', linked)

    def test_runner_exit_distinguishes_completion_limit_and_integrity(self):
        for scenario, expected, count in [('complete', 0, 2), ('incomplete', 1, 2),
                                          ('limit', 1, 1), ('changed', 1, 2)]:
            with self.subTest(scenario=scenario), tempfile.TemporaryDirectory() as directory:
                output = Path(directory) / 'run'
                def cell(*args, **kwargs):
                    return dict(completed=scenario != 'incomplete',
                                limit_detected=scenario == 'limit', elapsed_seconds=1)
                def inventory(path):
                    return {'changed': {}} if scenario == 'changed' and 'project' in path.parts else {}
                with mock.patch.object(sys, 'argv', ['run_browser_model.py', '--output', str(output)]), \
                        mock.patch.object(runner, 'stage', return_value={}), \
                        mock.patch.object(runner, 'command', return_value='frozen-revision'), \
                        mock.patch.object(runner, 'resource_manifest', side_effect=inventory), \
                        mock.patch.object(runner, 'disabled_skills', return_value=[]), \
                        mock.patch.object(runner, 'run_cell', side_effect=cell) as model, \
                        mock.patch('builtins.print'):
                    self.assertEqual(runner.main(), expected)
                manifest = json.loads((output / 'run.json').read_text())
                self.assertEqual(model.call_count, count)
                self.assertEqual(len(manifest['cells']), count)
                self.assertEqual(manifest['runtime']['codex'], 'frozen-revision')
                self.assertEqual(manifest['runtime']['node'], 'frozen-revision')
                self.assertEqual(manifest['runtime']['python'], runner.platform.python_version())
                self.assertEqual('finished_at' in manifest, scenario != 'limit')
                self.assertEqual(bool(manifest.get('stopped_after_limit')), scenario == 'limit')

    def fixture(self, root):
        source = root / 'benchmarks/browser/model-project'
        dependency = root / 'benchmarks/browser/node_modules/playwright-core'
        (source / 'nested').mkdir(parents=True)
        dependency.mkdir(parents=True)
        (source / 'index.html').write_text('<title>fixture</title>')
        (source / 'nested/requirements.md').write_text('Keep nested requirements')
        (dependency / 'package.json').write_text(json.dumps({'version': '1.63.0'}))
        (dependency / 'LICENSE').write_text('Synthetic test license')
        return source, dependency

    def test_stages_nested_sources_and_exact_dependencies_without_model(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, dependency = self.fixture(root)
            with mock.patch.object(runner, 'ROOT', root), mock.patch.object(runner, 'run_cell') as model:
                inventory = runner.stage(root / 'output')
                model.assert_not_called()
            self.assertEqual((root / 'output/nested/requirements.md').read_bytes(),
                             (source / 'nested/requirements.md').read_bytes())
            self.assertEqual(inventory, runner.resource_manifest(dependency))
            self.assertEqual(inventory, runner.resource_manifest(root / 'output/node_modules/playwright-core'))
            self.assertEqual(runner.command(['git', 'status', '--porcelain'], root / 'output'), '')
            with mock.patch.object(runner, 'ROOT', root), self.assertRaises(FileExistsError):
                runner.stage(root / 'output')

    def test_rejects_changed_version_and_source_links_before_preparation(self):
        for invalid in ('version', 'link'):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                source, dependency = self.fixture(root)
                if invalid == 'version':
                    (dependency / 'package.json').write_text('{"version":"0.0.0"}')
                else:
                    (source / 'linked.html').symlink_to(source / 'index.html')
                with mock.patch.object(runner, 'ROOT', root), self.assertRaises(ValueError):
                    runner.stage(root / 'output')
                self.assertFalse((root / 'output').exists())
