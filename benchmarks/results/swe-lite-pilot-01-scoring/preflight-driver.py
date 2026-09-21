"""Private author preflight: execute frozen eval scripts; display aggregate statuses only."""
import ast
from enum import Enum
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import urllib.request

root = Path(__file__).resolve().parents[2]
inputs = root / 'benchmarks/local-runs/swe-lite-pilot-01-scoring'
out = inputs / 'attempt-02'
out.mkdir(mode=0o700, exist_ok=False)
revision = '02e7a74ffd0b707aab73d203fe87bdc7c76afc8e'
def fetch(path):
    url = 'https://raw.githubusercontent.com/SWE-bench/SWE-bench/' + revision + '/' + path
    return urllib.request.urlopen(url, timeout=45).read()
parser_raw = fetch('swebench/harness/log_parsers/python.py')
constants_raw = fetch('swebench/harness/constants/__init__.py')
names = {'_SKIP_SUMMARY_COUNT', '_is_skip_summary', 'parse_log_pytest', 'parse_log_pytest_options'}
nodes = [n for n in ast.parse(constants_raw).body if isinstance(n, ast.ClassDef) and n.name == 'TestStatus']
for node in ast.parse(parser_raw).body:
    if isinstance(node, ast.FunctionDef) and node.name in names:
        nodes.append(node)
    elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
        nodes.append(node)
namespace = dict(Enum=Enum, re=re, TestSpec=object)
exec(compile(ast.Module(body=nodes, type_ignores=[]), '<pinned-parser-selection>', 'exec'), namespace)
for name in ('parse_log_pytest', 'parse_log_pytest_options'):
    assert namespace[name]('PASSED a\nFAILED b - AssertionError\nERROR c\nSKIPPED [1] elsewhere', None) == {'a':'PASSED','b':'FAILED','c':'ERROR'}
    assert namespace[name]('', None) == {}
images = {
    'psf__requests-2317': 'swebench/sweb.eval.x86_64.psf_1776_requests-2317@sha256:a0ce096d4dfa27ca8ea80ae4b38103e970d17b19066d886a550936394827c9fb',
    'pytest-dev__pytest-7432': 'swebench/sweb.eval.x86_64.pytest-dev_1776_pytest-7432@sha256:0e556e33eec3eb68e7737ea264268a758197718006336b84bb5f0c99187cf066',
}
summaries = []
for identity in ('pytest-dev__pytest-7432', 'psf__requests-2317'):
    row = json.loads((inputs / (identity + '.json')).read_text())
    for variant in ('base', 'gold'):
        cell = out / (identity + '-' + variant)
        cell.mkdir(mode=0o700)
        evaluation = cell / 'eval.sh'
        evaluation.write_text(row['eval_script'])
        patch = cell / 'candidate.patch'
        patch.write_text(row['patch'] if variant == 'gold' else '')
        os.chmod(evaluation, 0o600)
        os.chmod(patch, 0o600)
        name = 'qh-swelite-score02-' + ('pytest' if identity.startswith('pytest') else 'requests') + '-' + variant
        command = 'cd /testbed && '
        if variant == 'gold':
            command += 'git apply --check /tmp/candidate.patch && git apply /tmp/candidate.patch && '
        command += 'bash /tmp/eval.sh'
        subprocess.run(['docker', 'create', '--name', name, '--platform', 'linux/amd64',
                        '--network', 'none', '--memory', '2g', '--cpus', '2', '--pids-limit', '256',
                        '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                        '--entrypoint', '/usr/bin/timeout', images[identity],
                        '180', '/bin/bash', '-lc', command], check=True, capture_output=True)
        transfer = io.BytesIO()
        with tarfile.open(fileobj=transfer, mode='w') as archive:
            for path in (evaluation, patch):
                raw = path.read_bytes()
                info = tarfile.TarInfo(path.name)
                info.size, info.mode, info.uid, info.gid = len(raw), 0o644, 0, 0
                archive.addfile(info, io.BytesIO(raw))
        subprocess.run(['docker', 'cp', '-', name + ':/tmp/'], input=transfer.getvalue(),
                       check=True, capture_output=True)
        print(json.dumps(dict(starting=identity, variant=variant)), flush=True)
        with (cell / 'container.log').open('wb') as log:
            process = subprocess.run(['docker', 'start', '-a', name], stdout=log, stderr=subprocess.STDOUT, timeout=210)
        state, = json.loads(subprocess.check_output(['docker', 'inspect', name]))
        assert state['State']['Status'] == 'exited'
        log = (cell / 'container.log').read_text(errors='replace')
        # Exact dataset delimiters; do not infer success from final shell exit.
        starts = list(re.finditer(r'^\+ : \'>>>>> Start Test Output\'$', log, re.M))
        ends = list(re.finditer(r'^\+ : \'>>>>> End Test Output\'$', log, re.M))
        bounded = len(starts) == len(ends) == 1 and starts[0].end() < ends[0].start()
        test_log = log[starts[0].end():ends[0].start()] if bounded else ''
        parser = 'parse_log_pytest_options' if identity.startswith('psf') else 'parse_log_pytest'
        statuses = namespace[parser](test_log, None)
        groups = {}
        for field in ('FAIL_TO_PASS', 'PASS_TO_PASS'):
            groups[field] = {status:sum(statuses.get(label, 'MISSING') == status for label in row[field])
                             for status in ('PASSED','FAILED','ERROR','SKIPPED','XFAIL','MISSING')}
        summary = dict(instance_id=identity, variant=variant, container=name,
                       exit_code=state['State']['ExitCode'], bounded_test_output=bounded,
                       groups=groups, log_sha256=hashlib.sha256(log.encode()).hexdigest(),
                       parser_source_sha256=hashlib.sha256(parser_raw).hexdigest(),
                       limitation='Selected unchanged official parser AST with TestSpec annotation placeholder; not full harness grading.')
        (cell / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
        summaries.append(summary)
        print(json.dumps(summary), flush=True)
(out / 'summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
