import io
from pathlib import Path
import subprocess
import tarfile

root = Path(__file__).resolve().parents[2]
fixture = root / 'benchmarks/local-runs/swe-lite-tls-01'
def transfer(name, pairs, destination):
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w') as archive:
        for path, target in pairs:
            raw = path.read_bytes()
            info = tarfile.TarInfo(target)
            info.size, info.mode, info.uid, info.gid = len(raw), 0o644, 0, 0
            archive.addfile(info, io.BytesIO(raw))
    subprocess.run(['docker','cp','-', name + ':' + destination], input=stream.getvalue(),check=True)
service = 'qh-swelite-httpbin-tls-01'
subprocess.run(['docker','create','--pull','never','--name',service,'--platform','linux/amd64',
                '--network','qh-swelite-contract-01','--ip','10.255.255.4',
                '--network-alias','httpbin','--network-alias','httpbin.org',
                '--network-alias','www.google.co.uk','--network-alias','wrong.httpbin.test',
                '--memory','512m','--cpus','1','--pids-limit','128',
                '--cap-drop','ALL','--security-opt','no-new-privileges',
                '--entrypoint','/bin/bash',
                'kennethreitz/httpbin@sha256:599fe5e5073102dbb0ee3dbb65f049dab44fa9fc251f6835c9990f8fb196a72b',
                '/tmp/serve.sh'],check=True)
# Copy under /tmp, then the controlled startup makes a fixture directory; no host mount.
transfer(service, [(fixture / file, file) for file in ('serve.sh','server.key','server.pem')], '/tmp/')
# serve.sh refers to /fixture: provide files there through Docker's archive extraction.
stream = io.BytesIO()
with tarfile.open(fileobj=stream,mode='w') as archive:
    for name in ('server.key','server.pem'):
        raw = (fixture/name).read_bytes()
        info = tarfile.TarInfo('fixture/' + name)
        info.size,info.mode,info.uid,info.gid = len(raw),0o644,0,0
        archive.addfile(info,io.BytesIO(raw))
subprocess.run(['docker','cp','-',service+':/'],input=stream.getvalue(),check=True)
subprocess.run(['docker','start',service],check=True)
client = 'qh-swelite-requests-tls-controls-01'
command = ('set -e; python -B -m pip install --no-index --no-deps --find-links /opt/compat '
           'pytest==4.6.11 pluggy==0.13.1 atomicwrites==1.4.1 py==1.11.0 six==1.17.0 '
           'attrs==23.2.0 more-itertools==9.1.0 packaging==24.2 wcwidth==0.2.13 certifi==2024.8.30; '
           'python -B /fixture/check.py; '
           'python -B -m pytest -p no:cacheprovider -q --tb=short test_requests.py')
subprocess.run(['docker','create','--pull','never','--name',client,'--platform','linux/amd64',
                '--network','qh-swelite-contract-01','--ip','10.255.255.5',
                '--memory','2g','--cpus','2','--pids-limit','256','--cap-drop','ALL',
                '--security-opt','no-new-privileges','-e','HTTPBIN_URL=http://httpbin/',
                '-e','PYTHONDONTWRITEBYTECODE=1','-e','PYTEST_DISABLE_PLUGIN_AUTOLOAD=1',
                '--entrypoint','/usr/bin/timeout',
                'sha256:f4ede93d2747ddc21d276572cbd2e1df5ea60df8d5d99247f073797bab3e539f',
                '120','/bin/bash','-lc',command],check=True)
subprocess.run(['docker','cp',str(root/'benchmarks/local-runs/swe-lite-pilot-01-requests-pytest'),
                client+':/opt/compat'],check=True)
transfer(client,[(fixture/'ca.pem','fixture/ca.pem'),(fixture/'check.py','fixture/check.py')],'/')
print('Created fixed service/client containers; run docker start -a ' + client,flush=True)
