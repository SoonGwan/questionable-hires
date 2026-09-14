#!/usr/bin/env python3
"""Replay retained diagnosis and literal persistence commands after model timing."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile

from replay_bundle_contract_09_form import REVISION, CASES_SHA
from replay_receipt_ledger_01 import inventory


def normalize(text, workspace):
    text = text.replace(str(workspace), '<WORKSPACE>').replace(str(Path.home()), '<HOME>')
    text = re.sub(r'\.(lost-write-audit|con-artist)-[^/\s"\\]+', r'.\1-<COPY>', text)
    return re.sub(r'Ran 1 test in [0-9.]+s', 'Ran 1 test in <TIME>s', text).strip()


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    frozen = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(frozen).hexdigest() == CASES_SHA == manifest['cases_sha256']
    cases = {c['id']: c for c in json.loads(frozen)}
    report = dict(kind='separate author replay; missing original output remains missing', revision=REVISION, checks=[])
    for case in ('persistence-test', 'search-diagnosis'):
        for arm in ('baseline', 'skill'):
            cell = run / (case + '--' + arm + '--1')
            meta = json.loads((cell / 'metadata.json').read_text())
            workspace = Path(meta['workspace'])
            original = inventory(workspace)
            project = inventory(cell / 'project')
            for path, content in cases[case]['files'].items():
                assert (workspace / path).read_bytes() == (cell / 'project' / path).read_bytes() == content.encode()
            events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            items = [e['item'] for e in events if e.get('type') == 'item.completed'
                     and e.get('item', {}).get('type') == 'command_execution']
            if case == 'persistence-test':
                candidates = [i for i in items if ('--spec' in i['command'] or "python3 -B - <<" in i['command'])]
                assert len(candidates) == 1
                item = candidates[0]
                script = shlex.split(item['command'])[-1]
                original_output = item['aggregated_output']
            else:
                path = 'experiment_search.py' if arm == 'baseline' else 'experiments/search_order_probe.py'
                script = 'python3 -B ' + path
                original_output = ((cell / 'project/experiment_search.results.json').read_text() if arm == 'baseline'
                                   else next(i['aggregated_output'] for i in items if i['command'].endswith("experiments/search_order_probe.py'")))
                if arm == 'baseline':
                    assert any(original_output.strip() in i['aggregated_output'] for i in items)
            index = meta['pre_collection_index']
            raw_index = (cell / index['file']).read_bytes()
            assert index['status'] == 'retained' and hashlib.sha256(raw_index).hexdigest() == index['sha256']
            with tempfile.TemporaryDirectory(prefix='author-audit-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(workspace, scratch)
                (scratch / '.git/index').write_bytes(raw_index)
                (scratch / '.git/index').chmod(index['mode'])
                before = inventory(scratch)
                result = subprocess.run(['/bin/zsh', '-lc', script], cwd=scratch,
                                        capture_output=True, text=True, timeout=45)
                after = inventory(scratch)
                changes = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
                output = normalize(result.stdout + result.stderr, scratch)
                captured = normalize(original_output, workspace)
                report['checks'].append(dict(cell=cell.name, command=script,
                    exit_code=result.returncode, changed_copy_paths=changes,
                    original_output=normalize(original_output, workspace),
                    replay_output=output, normalized_full_output_equal=(captured == output),
                    captured_output_contained=bool(captured) and captured in output))
            assert inventory(workspace) == original and inventory(cell / 'project') == project
    report['original_workspaces_and_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([{k: c[k] for k in ('cell', 'exit_code', 'changed_copy_paths', 'normalized_full_output_equal', 'captured_output_contained')} for c in report['checks']], indent=2))
