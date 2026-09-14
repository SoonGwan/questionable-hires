#!/usr/bin/env python3
"""Keep original schema witnesses fixed while corrupting only disposable down SQL."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_09_form import REVISION, inventory


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    previous = Path(__file__).parent / 'results/bundle-contract-09-readonly-controls/author-replay.json'
    witnesses = json.loads(previous.read_text())['checks']
    report = dict(kind='separate native rollback fault controls, not model sessions',
                  revision=REVISION, checks=[])
    for witness in witnesses:
        if not witness['cell'].startswith('rolling-schema--'):
            continue
        cell = run / witness['cell']
        project = cell / 'project'
        before = inventory(project)
        assert before == witness['inventory_sha256']
        program = witness['witness_source']
        events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
        assert any(program in shlex.split(e['item']['command'])[-1]
                   for e in events if e.get('type') == 'item.completed'
                   and e.get('item', {}).get('type') == 'command_execution')
        for name, sql in [('unchanged', ''), ('lose_inserted', 'DELETE FROM users WHERE id=3;'),
                          ('lose_updated', 'DELETE FROM users WHERE id=1;'),
                          ('corrupt_untouched', "UPDATE users SET name='corrupted' WHERE id=2;")]:
            with tempfile.TemporaryDirectory(prefix='author-schema-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                down = (scratch / '002_down.sql').read_text() + sql
                (scratch / '002_down.sql').write_text(down)
                command = [sys.executable, '-B', '-c', program]
                result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                expected = 0 if not sql else 1
                assert all((scratch / p).read_bytes() == (project / p).read_bytes()
                           for p in before if p != '002_down.sql')
                matched = result.returncode == expected and (not sql or 'AssertionError:' in result.stderr)
                report['checks'].append(dict(cell=cell.name, variant=name, expected_exit=expected,
                    exit_code=result.returncode, matched=matched, witness_source=program,
                    original_inventory_sha256=before, down_sql=down,
                    stdout=result.stdout.replace(str(scratch), '<REPLAY>'),
                    stderr=result.stderr.replace(str(scratch), '<REPLAY>')))
        assert inventory(project) == before
    report['all_matched'] = len(report['checks']) == 8 and all(c['matched'] for c in report['checks'])
    report['retained_projects_unchanged'] = True
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
    print(json.dumps(dict(checks=len(report['checks']), all_matched=report['all_matched'])))
