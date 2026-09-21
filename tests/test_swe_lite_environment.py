import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('swe_environment', ROOT/'benchmarks/swe_lite_environment.py')
environment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(environment)


class SolverEnvironmentTests(unittest.TestCase):
    def test_export_requires_new_destination(self):
        with tempfile.TemporaryDirectory() as temp, mock.patch.object(environment, 'docker') as docker:
            with self.assertRaises(FileExistsError):
                environment.source('pytest', Path(temp))
            docker.assert_not_called()

    def test_export_keeps_generated_metadata_and_cleans_owned_container(self):
        for metadata in (False, True):
            with self.subTest(metadata=metadata), tempfile.TemporaryDirectory() as temp:
                destination = Path(temp)/'source'
                def docker(*args, **kwargs):
                    if args[0] == 'cp':
                        destination.mkdir()
                        if metadata:
                            path = destination/'src/_pytest/_version.py'
                            path.parent.mkdir(parents=True)
                            path.write_text('version = "synthetic"')
                    return SimpleNamespace(stdout=b'owned-container-id\n')
                with mock.patch.object(environment, 'docker', side_effect=docker) as calls, \
                        mock.patch.object(environment.subprocess, 'check_output', side_effect=[
                            environment.TREES['pytest']+'\n', '1\n', '', '']):
                    if metadata:
                        result = environment.source('pytest', destination)
                        self.assertEqual(result['tree'], environment.TREES['pytest'])
                    else:
                        with self.assertRaises(ValueError):
                            environment.source('pytest', destination)
                    calls.assert_any_call('rm', 'owned-container-id')

    def test_service_transfers_only_server_material_with_private_key_mode(self):
        with tempfile.TemporaryDirectory() as temp:
            fixture = Path(temp)
            for name in ('serve.sh','server.pem','server.key','ca.key'):
                (fixture/name).write_text('synthetic ' + name)
            network = [dict(Internal=True, IPAM=dict(Config=[
                dict(Subnet='10.255.255.0/24', Gateway='10.255.255.254')]))]
            def docker(*args, **kwargs):
                data = (environment.NETWORK+'\n').encode() if args[:2] == ('network','ls') else json.dumps(network).encode()
                return SimpleNamespace(stdout=data)
            with mock.patch.object(environment, 'docker', side_effect=docker) as calls, \
                    mock.patch.object(environment.subprocess, 'run'):
                environment.create_service(fixture)
            transfers = [call for call in calls.call_args_list if call.args[:1] == ('cp',)]
            self.assertEqual(len(transfers), 1)
            with tarfile.open(fileobj=io.BytesIO(transfers[0].kwargs['input'])) as archive:
                self.assertEqual(set(archive.getnames()), {'fixture/serve.sh','fixture/server.pem','fixture/server.key'})
                key = archive.getmember('fixture/server.key')
                self.assertEqual((key.mode,key.uid,key.gid), (0o600,0,0))

    def test_rejects_noninternal_network_before_creating_service(self):
        with mock.patch.object(environment.subprocess, 'run'), \
                mock.patch.object(environment, 'docker', side_effect=[
                    SimpleNamespace(stdout=(environment.NETWORK+'\n').encode()),
                    SimpleNamespace(stdout=b'[{"Internal": false}]')]) as docker:
            with self.assertRaises(ValueError):
                environment.create_service(Path('/synthetic'))
            self.assertFalse(any(c.args[:1] == ('create',) for c in docker.call_args_list))
