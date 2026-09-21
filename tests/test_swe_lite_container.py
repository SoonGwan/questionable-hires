import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('swe_container', ROOT / 'benchmarks/swe_lite_container.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
IMAGE = 'sha256:' + 'a' * 64


class ContainerAdapterTests(unittest.TestCase):
    def test_execute_passes_isolated_scratch_to_container_and_lifecycle(self):
        calls = []
        owner = None
        removed = False
        def docker(command, **kwargs):
            nonlocal owner, removed
            calls.append(command)
            action = command[3]
            if action == 'create':
                owner = command[command.index('--label') + 1].split('=', 1)[1]
                return SimpleNamespace(returncode=0, stdout='container-id', stderr='')
            if action == 'rm':
                removed = True
            if action == 'inspect':
                if removed:
                    return SimpleNamespace(returncode=1, stdout='',
                        stderr='Error: No such object: ' + command[4])
                return SimpleNamespace(returncode=0, stderr='', stdout=json.dumps([{
                    'State': {'ExitCode': 0, 'OOMKilled': False},
                    'Config': {'Labels': {'qh.solver.owner': owner}},
                    'Mounts': [], 'NetworkSettings': {'Networks': {}}}]))
            return SimpleNamespace(returncode=0, stdout='', stderr='')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            args = SimpleNamespace(state=root, scratch_mode='isolated-v2',
                network='none', project='pytest', context='synthetic', memory_gib=6,
                timeout=60, auth_file=root/'auth.json', workspace=root/'project',
                image=IMAGE, command=['python', '-c', 'print(1)'])
            with patch.object(runner.subprocess, 'run', side_effect=docker), \
                    patch.object(runner.subprocess, 'call', return_value=0):
                self.assertEqual(runner.execute(args), 0)
            command = calls[0]
            self.assertIn('TMPDIR=/qh-scratch', command)
            self.assertIn('/qh-scratch:rw,nosuid,nodev,mode=0700', command)
            self.assertNotIn('TMPDIR=/testbed/.git/qh-tmp', command)
            lifecycle = json.loads((root/'lifecycle.json').read_text())
            self.assertEqual(lifecycle['scratch_path'], '/qh-scratch')
            self.assertEqual(lifecycle['scratch_mode'], 'isolated-v2')
            self.assertTrue(lifecycle['removed'])

    def test_isolated_scratch_has_no_project_config_or_host_mount(self):
        self.assertEqual(runner.scratch_arguments('isolated-v2'),
            ('/qh-scratch', ['--tmpfs', '/qh-scratch:rw,nosuid,nodev,mode=0700']))
        self.assertEqual(runner.scratch_arguments('project-config-v1'),
            ('/testbed/.git/qh-tmp', []))
        with self.assertRaises(ValueError):
            runner.scratch_arguments('unknown')
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            auth = root / 'auth.json'
            auth.write_text('{}')
            launch = runner.container_launcher(IMAGE, auth, root / 'state', 'pytest',
                scratch_mode='isolated-v2')
            command = launch(root / 'project', self.args(root / 'project'))
            self.assertEqual(command[command.index('--scratch-mode') + 1], 'isolated-v2')
            self.assertFalse((root / 'project/.git/qh-tmp').exists())

    def test_offline_requests_uses_only_fixture_network(self):
        self.assertEqual(runner.network_arguments('requests', 'none'),
            ['--network', 'qh-swelite-contract-01', '--ip', '10.255.255.5'])
        self.assertEqual(runner.network_arguments('pytest', 'none'), ['--network', 'none'])
        self.assertEqual(runner.network_arguments('requests', 'bridge'), ['--network', 'bridge'])

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
            self.assertEqual((root/'project/.git/qh-tmp/pytest.ini').read_text(), '[pytest]\n')
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
