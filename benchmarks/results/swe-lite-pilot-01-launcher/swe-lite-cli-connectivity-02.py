"""Repeat only neutral infrastructure probe after the recorded OOM failure."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run
from swe_lite_container import container_launcher
output = ROOT / 'benchmarks/local-runs/swe-lite-cli-connectivity-02'
output.mkdir(mode=0o700, exist_ok=False)
auth = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'auth.json'
protocol = json.loads((output.parent/'swe-lite-cli-connectivity-01/protocol.json').read_text())
protocol.update(context='colima-qh-bench', vm_memory_gib=8, container_memory_gib=6,
    identities={name: hashlib.sha256((ROOT/'benchmarks'/name).read_bytes()).hexdigest()
                for name in ('run.py', 'swe_lite_container.py')})
(output/'protocol.json').write_text(json.dumps(protocol, indent=2) + '\n')
with tempfile.TemporaryDirectory(prefix='qh-runtime-auth-', dir=output.parent) as credentials:
    copied_auth = Path(credentials)/'auth.json'
    shutil.copyfile(auth, copied_auth)
    copied_auth.chmod(0o600)
    launch = container_launcher(
        'sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923',
        copied_auth, output/'runtime-state', 'pytest', network='bridge', timeout=90,
        context='colima-qh-bench', memory_gib=6)
    def launcher(workspace, args):
        return launch(workspace, args[:-1] + ['-c', 'web_search="disabled"', args[-1]])
    result = run.run_cell(protocol['case'], 'baseline', 1, output, 'gpt-6-astra', 'medium', 110, [],
        launcher=launcher, workspace_root=output/'workspaces', persist_session=True)
path = Path(result['workspace'])/'observed.txt'
summary = {key: result[key] for key in ('completed','timed_out','exit_code','limit_detected','usage','elapsed_seconds')}
summary.update(expected_file=path.is_file() and path.read_text() == 'runtime-ready\n',
    session_files=len(list((output/'runtime-state/sessions').rglob('*.jsonl'))),
    temporary_credential_removed=not Path(credentials).exists())
(output/'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
