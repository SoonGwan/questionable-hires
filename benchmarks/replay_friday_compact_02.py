#!/usr/bin/env python3
"""Separate unchanged-program replay; never replace original model evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'benchmarks/local-runs/friday-compact-model-02'
FROZEN = '135c4df'


def inventory(root):
    return {p.relative_to(root).as_posix(): [hashlib.sha256(p.read_bytes()).hexdigest(),
                                          p.stat().st_mode & 0o777]
            for p in root.rglob('*') if p.is_file()}


def main():
    spec = importlib.util.spec_from_file_location('runner', ROOT / 'benchmarks/run.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    manifest = json.loads((RUN / 'run.json').read_text())
    assert manifest['revision'].startswith(FROZEN) and manifest.get('finished_at')
    case_bytes = subprocess.check_output(['git', 'show', FROZEN + ':benchmarks/bundle-contract-v2-cases.json'], cwd=ROOT)
    assert hashlib.sha256(case_bytes).hexdigest() == manifest['cases_sha256']
    case = next(c for c in json.loads(case_bytes) if c['id'] == 'rolling-schema')
    report = {'kind': 'separate author replay, not original model output', 'cells': {}}
    for arm in ('baseline', 'skill'):
        cell = RUN / ('rolling-schema--' + arm + '--1')
        project = cell / 'project'
        before = inventory(project)
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert next(e['usage'] for e in reversed(events) if e['type'] == 'turn.completed') == meta['usage']
        assert meta['completed'] and meta['resource_diagnostics'] == {'changed_paths': []}
        for name, contents in case['files'].items():
            assert (project / name).read_bytes() == contents.encode()
        if arm == 'skill':
            installed = Path(meta['workspace']) / '.agents/skills'
            assert runner.resource_manifest(installed) == meta['installed_resources_before'] == meta['installed_resources_after']
            for name, detail in meta['installed_resources_before'].items():
                frozen = subprocess.check_output(['git', 'show', FROZEN + ':skills/' + name], cwd=ROOT)
                assert hashlib.sha256(frozen).hexdigest() == detail['sha256']
        item = next(e['item'] for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('id') == 'item_6')
        assert item['exit_code'] == 0
        with tempfile.TemporaryDirectory(prefix='qh-friday-replay-', dir=RUN) as folder:
            copy = Path(folder) / 'project'
            shutil.copytree(project, copy)
            if arm == 'baseline':
                command = ['python3', '-B', 'review/verify_release.py']
                process = subprocess.run(command, cwd=copy, capture_output=True, text=True, timeout=20)
                replay = json.loads(process.stdout)
                original = json.loads(item['aggregated_output'])
                # Environment version is not a result discrepancy; retain it.
                original_version = original.pop('sqlite_version')
                replay_version = replay.pop('sqlite_version')
                assert replay == original
                match = {'observations_match': True, 'original_sqlite': original_version,
                         'replay_sqlite': replay_version}
            else:
                shell = shlex.split(item['command'])
                assert shell[:2] == ['/bin/zsh', '-lc']
                process = subprocess.run(shell, cwd=copy, capture_output=True, text=True, timeout=20)
                assert process.stdout == item['aggregated_output']
                match = {'complete_output_matches': True}
            assert process.returncode == 0 and not process.stderr
            assert inventory(copy) == before
        assert inventory(project) == before
        report['cells'][arm] = dict(match, exit_code=process.returncode,
            stdout=process.stdout, stderr=process.stderr, originals_unchanged=True,
            raw_events_usage_reconciled=True, resources_reconciled=True)
    target = RUN / 'author-replay.json'
    with target.open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({arm: {k: v for k, v in row.items() if k not in ('stdout', 'stderr')}
                      for arm, row in report['cells'].items()}, indent=2))


if __name__ == '__main__':
    main()
