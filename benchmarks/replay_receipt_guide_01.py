#!/usr/bin/env python3
"""Replay the literal measured recipe separately, retaining native evidence."""
import ast
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'benchmarks/local-runs/receipt-guide-model-01'
REV = '885a1f5'


def inventory(root):
    return {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(),
                                          p.stat().st_mode & 0o777)
            for p in root.rglob('*') if p.is_file()}


def main():
    global RUN, REV
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile', choices=['guide-01', 'output-choice-01'], default='guide-01')
    args = parser.parse_args()
    output_choice = args.profile == 'output-choice-01'
    if output_choice:
        RUN = ROOT / 'benchmarks/local-runs/receipt-output-choice-01'
        REV = '15a2e38'
    module = importlib.util.spec_from_file_location('runner', ROOT / 'benchmarks/run.py')
    runner = importlib.util.module_from_spec(module)
    module.loader.exec_module(runner)
    manifest = json.loads((RUN / 'run.json').read_text())
    assert manifest['revision'].startswith(REV) and manifest.get('finished_at')
    frozen = subprocess.check_output(['git', 'show', REV + ':benchmarks/receipt-src-cases.json'], cwd=ROOT)
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256']
    case = json.loads(frozen)[0]
    cell = RUN / 'src-settings-fix--skill--1'
    meta = json.loads((cell / 'metadata.json').read_text())
    workspace = Path(meta['workspace'])
    snapshot = inventory(workspace)
    project_snapshot = inventory(cell / 'project')
    expected_files = dict(case['files'], **case['working_files'])
    assert set(project_snapshot) == set(expected_files)
    for path, content in expected_files.items():
        assert (cell / 'project' / path).read_bytes() == content.encode()
        assert (workspace / path).read_bytes() == content.encode()
    resources = runner.resource_manifest(workspace / '.agents/skills')
    assert resources == meta['installed_resources_before'] == meta['installed_resources_after']
    for path, info in resources.items():
        data = subprocess.check_output(['git', 'show', REV + ':skills/' + path], cwd=ROOT)
        mode = subprocess.check_output(['git', 'ls-tree', REV, 'skills/' + path], cwd=ROOT).split()[0]
        assert hashlib.sha256(data).hexdigest() == info['sha256']
        assert int(mode, 8) & 0o777 == info['mode']
    raw = (cell / 'stdout.original.jsonl').read_text()
    assert raw.replace(str(workspace), '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
    events = [json.loads(line) for line in raw.splitlines()]
    assert next(e['usage'] for e in reversed(events) if e['type'] == 'turn.completed') == meta['usage']
    item_id = 'item_7' if output_choice else 'item_5'
    item = next(e['item'] for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('id') == item_id)
    recipe = ast.literal_eval(re.search(r'spec = (\{.*?\n\})\n(?:result|print)', item['command'], re.S).group(1))
    original, _ = json.JSONDecoder().raw_decode(item['aggregated_output'])
    options = [] if output_choice else ['--pretty']
    assert ('--pretty' in item['command']) == bool(options)
    with tempfile.TemporaryDirectory(prefix='qh-receipt-replay-', dir=RUN) as folder:
        copy = Path(folder) / 'project'
        shutil.copytree(workspace, copy)
        copied_before = inventory(copy)
        process = subprocess.run(['python3', '-B', '.agents/skills/receipt/scripts/compare.py',
                                  '--source', '.', '--spec', '-', *options], cwd=copy,
                                 input=json.dumps(recipe), capture_output=True, text=True, timeout=40)
        assert process.returncode == 0 and not process.stderr
        replay = json.loads(process.stdout)
        def normalized(result, prefix):
            result = json.loads(json.dumps(result))
            for phase, expected_exit in [('before', 1), ('after', 0)]:
                check = result['checks'][phase]
                assert check['exit_code'] == expected_exit and not check['timed_out'] and not check['output_truncated']
                assert len(re.findall(r'^test_.* \.\.\. ', check['output'], re.M)) == 5
                assert 'Ran 5 tests' in check['output']
                output = check['output'].replace(prefix, '<PROJECT>')
                output = re.sub(r'\.receipt-[^/]+/', '.receipt-<COPY>/', output)
                check['output'] = re.sub(r'Ran 5 tests in [0-9.]+s', 'Ran 5 tests in <TIME>s', output)
            return result
        assert normalized(original, str(workspace)) == normalized(replay, str(copy))
        assert inventory(copy) == copied_before
        safe_replay = json.loads(json.dumps(replay).replace(str(copy), '<REPLAY_PROJECT>'))
    assert inventory(workspace) == snapshot and inventory(cell / 'project') == project_snapshot
    report = {'kind': 'separate author recipe replay, not original model evidence',
              'profile': args.profile,
              'recipe': recipe, 'exit_code': 0, 'observations_match': True,
              'normalization': 'only project/copy paths and native test durations',
              'raw_usage_resources_reconciled': True, 'original_inventories_unchanged': True,
              'replay': safe_replay}
    with (RUN / 'author-replay.json').open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print('Literal recipe replay matches native outcomes, fields and inventories.')


if __name__ == '__main__':
    main()
