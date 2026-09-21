"""One neutral model smoke session; never a scored skill comparison."""
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'benchmarks'))
import run
from swe_lite_container import container_launcher

output = ROOT / 'benchmarks/local-runs/swe-lite-cli-connectivity-01'
output.mkdir(mode=0o700, exist_ok=False)
auth = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'auth.json'
launch = container_launcher(
    'sha256:34f351fda2c7ba6644ebacc03822fbc78d8e0a294cba5360fe91c76460633923',
    auth, output / 'runtime-state', 'pytest', network='bridge', timeout=90)
def launcher(workspace, args):
    return launch(workspace, args[:-1] + ['-c', 'web_search="disabled"', args[-1]])
case = dict(id='runtime-connectivity', skill='con-artist',
    files={'README.md': 'Neutral execution probe. No issue, solution or skill files.\n'},
    task='This is an execution probe, not a development task. Run a local Python command '
         'that prints its Python version and current directory, then writes exactly '
         'runtime-ready followed by a newline to observed.txt in the current project. '
         'Read observed.txt back using a tool and report its content. Do not inspect '
         'credentials, runtime configuration, other directories or network resources. '
         'Do not make any other project changes.')
(output / 'protocol.json').write_text(json.dumps(dict(case=case, model='gpt-6-astra',
    effort='medium', outer_timeout=110, container_timeout=90,
    purpose='neutral CLI connectivity; not skill or external-task evidence'), indent=2) + '\n')
result = run.run_cell(case, 'baseline', 1, output, 'gpt-6-astra', 'medium', 110, [],
    launcher=launcher, workspace_root=output/'workspaces', persist_session=True)
path = Path(result['workspace']) / 'observed.txt'
summary = {key: result[key] for key in ('completed', 'timed_out', 'exit_code',
    'limit_detected', 'usage', 'elapsed_seconds', 'capture_diagnostics')}
summary['expected_file'] = path.is_file() and path.read_text() == 'runtime-ready\n'
summary['session_files'] = len(list((output/'runtime-state/sessions').rglob('*.jsonl')))
(output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
