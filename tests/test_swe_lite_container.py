import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('swe_container', ROOT / 'benchmarks/swe_lite_container.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
IMAGE = 'sha256:' + 'a' * 64


class ContainerAdapterTests(unittest.TestCase):
    def test_inspect_failure_is_not_cleanup_success(self):
        result = SimpleNamespace(returncode=1, stdout='', stderr='Cannot connect to Docker daemon')
        with self.assertRaises(RuntimeError):
            runner.inspected_container(result, 'owned')
        result.stderr = 'Error: No such object: owned\n'
        self.assertIsNone(runner.inspected_container(result, 'owned'))
        result.stderr = 'error: no such object: owned\n'
        self.assertIsNone(runner.inspected_container(result, 'owned'))
        with self.assertRaises(RuntimeError):
            runner.inspected_container(result, 'different')
        result = SimpleNamespace(returncode=0, stdout='[{"Id":"exists"}]', stderr='')
        self.assertEqual(runner.inspected_container(result, 'owned'), {'Id': 'exists'})

    def args(self, workspace):
        return ['codex', 'exec', '--sandbox', 'workspace-write', '--json', '-C',
                str(workspace), 'A prompt mentioning workspace-write must not change.']

    def test_translates_only_execution_arguments(self):
        args = self.args(Path('/synthetic/project'))
        translated = runner.translated_args(Path('/synthetic/project'), args)
        self.assertEqual(translated[translated.index('-C') + 1], '/testbed')
        self.assertIn('--dangerously-bypass-approvals-and-sandbox', translated)
        self.assertNotIn('--sandbox', translated)
        self.assertEqual(translated[-1], args[-1])
        self.assertIn('--sandbox', args)

    def test_rejects_lost_sessions_or_wrong_workspace(self):
        workspace = Path('/synthetic/project')
        for args in (self.args(workspace) + ['--ephemeral'], self.args(Path('/other')),
                     ['codex', 'exec', '-C', str(workspace), 'task']):
            with self.subTest(args=args), self.assertRaises(ValueError):
                runner.translated_args(workspace, args)

    def test_exclusive_private_state_and_separate_mount_roots(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            auth = root / 'auth.json'
            auth.write_text('{}')
            state = root / 'state'
            launch = runner.container_launcher(IMAGE, auth, state, 'pytest',
                context='synthetic-context', memory_gib=6)
            command = launch(root / 'project', self.args(root / 'project'))
            self.assertEqual(state.stat().st_mode & 0o777, 0o700)
            self.assertTrue((state / 'sessions').is_dir())
            self.assertIn(str(auth), command)
            self.assertNotIn('{}', command)
            self.assertIn(IMAGE, command)
            self.assertEqual(command[command.index('--network') + 1], 'none')
            self.assertEqual(command[command.index('--context') + 1], 'synthetic-context')
            self.assertEqual(command[command.index('--memory-gib') + 1], '6')
            with self.assertRaises(FileExistsError):
                runner.container_launcher(IMAGE, auth, state, 'pytest')
            for workspace in (state, state / 'project', root):
                with self.subTest(workspace=workspace), self.assertRaises(ValueError):
                    launch(workspace, self.args(workspace))

    def test_rejects_mutable_image_and_linked_auth(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            auth = root / 'auth.json'
            auth.write_text('{}')
            link = root / 'linked.json'
            link.symlink_to(auth)
            for image, credential in [('latest', auth), (IMAGE, link), (IMAGE, root / 'missing')]:
                with self.subTest(image=image, credential=credential), self.assertRaises(ValueError):
                    runner.container_launcher(image, credential, root / 'state', 'pytest')
            self.assertFalse((root / 'state').exists())

    def test_rejects_credentials_inside_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            project = root / 'project'
            project.mkdir()
            auth = project / 'auth.json'
            auth.write_text('{}')
            launch = runner.container_launcher(IMAGE, auth, root / 'state', 'pytest')
            with self.assertRaises(ValueError):
                launch(project, self.args(project))
