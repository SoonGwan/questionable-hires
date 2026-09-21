"""Prepare solver-only source copies and the existing local HTTP/TLS fixture."""
import io
import json
from pathlib import Path
import subprocess
import tarfile
import uuid

CONTEXT = 'colima-qh-bench'
NETWORK = 'qh-swelite-contract-01'
SERVICE = 'qh-swelite-httpbin-tls-01'
HTTPBIN = 'sha256:599fe5e5073102dbb0ee3dbb65f049dab44fa9fc251f6835c9990f8fb196a72b'
IMAGES = {
    'requests': 'sha256:18a37ed6f5179b655c81ae5c5d9c47c1d8677762cba417ee661c5c66dc2c2d8d',
    'pytest': 'sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923',
}
TREES = {
    'requests': '980e006268fb816b7d2686baef7242418d895d9a',
    'pytest': '877d433795f3d7288b9edd5696724bb2d8e47f88',
}


def docker(*args, **kwargs):
    return subprocess.run(['docker', '--context', CONTEXT, *args],
                          check=True, capture_output=True, timeout=60, **kwargs)


def source(project, destination):
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    name = 'qh-swe-source-' + uuid.uuid4().hex
    container = docker('create', '--name', name, '--pull', 'never', '--platform',
        'linux/amd64', '--network', 'none', IMAGES[project], '/bin/true').stdout.decode().strip()
    try:
        docker('cp', container + ':/testbed', str(destination))
    finally:
        docker('rm', container)
    def git(*args):
        return subprocess.check_output(['git', '-C', str(destination), *args], text=True).strip()
    if (git('rev-parse', 'HEAD^{tree}') != TREES[project]
            or git('rev-list', '--all', '--count') != '1' or git('remote')
            or git('status', '--porcelain')):
        raise ValueError('Unexpected exported base source')
    if project == 'pytest' and not (destination/'src/_pytest/_version.py').is_file():
        raise ValueError('Missing installed/generated pytest metadata')
    return dict(image=IMAGES[project], tree=TREES[project], commits=1, remotes=0)


def create_service(fixture):
    """Exclusive creation. Never update/reuse an existing service silently."""
    fixture = Path(fixture)
    subprocess.run(['openssl', 'x509', '-checkend', '86400', '-noout', '-in',
                    str(fixture/'server.pem')], check=True, capture_output=True)
    networks = docker('network', 'ls', '--format', '{{.Name}}').stdout.decode().splitlines()
    if NETWORK not in networks:
        docker('network', 'create', '--internal', '--subnet', '10.255.255.0/24',
               '--gateway', '10.255.255.254', NETWORK)
    network, = json.loads(docker('network', 'inspect', NETWORK).stdout)
    if not network['Internal'] or network['IPAM']['Config'] != [
            {'Subnet': '10.255.255.0/24', 'Gateway': '10.255.255.254'}]:
        raise ValueError('Unexpected fixture network contract')
    docker('create', '--name', SERVICE, '--pull', 'never', '--platform', 'linux/amd64',
        '--network', NETWORK, '--ip', '10.255.255.4',
        '--network-alias', 'httpbin', '--network-alias', 'httpbin.org',
        '--network-alias', 'www.google.co.uk', '--network-alias', 'wrong.httpbin.test',
        '--memory', '512m', '--cpus', '1', '--pids-limit', '128',
        '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
        '--entrypoint', '/bin/bash', HTTPBIN, '/fixture/serve.sh')
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        for name in ('serve.sh', 'server.pem', 'server.key'):
            data = (fixture/name).read_bytes()
            info = tarfile.TarInfo('fixture/' + name)
            info.size, info.uid, info.gid = len(data), 0, 0
            info.mode = 0o600 if name.endswith('.key') else 0o644
            archive.addfile(info, io.BytesIO(data))
    docker('cp', '-', SERVICE + ':/', input=stream.getvalue())
    docker('start', SERVICE)
    return dict(context=CONTEXT, network=NETWORK, service=SERVICE, image=HTTPBIN,
                ip='10.255.255.4', host_mounts=[], published_ports=[])
