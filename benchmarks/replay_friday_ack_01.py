#!/usr/bin/env python3
"""Replay four retained programs without modifying measured projects or logs."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'benchmarks/local-runs/friday-ack-01'
REV = '76c251c'


def inventory(root):
    return {p.relative_to(root).as_posix(): {
        'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'mode': p.stat().st_mode & 0o777}
        for p in root.rglob('*') if p.is_file()}


def main():
    spec = importlib.util.spec_from_file_location('runner', ROOT / 'benchmarks/run.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    manifest = json.loads((RUN / 'run.json').read_text())
    assert manifest['revision'].startswith(REV) and manifest.get('finished_at')
    frozen = subprocess.check_output(['git', 'show', REV + ':benchmarks/friday-ack-cases.json'], cwd=ROOT)
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256']
    cases = {c['id']: c for c in json.loads(frozen)}
    report = {'kind': 'separate author replay; original evidence unchanged', 'cells': {}}
    for name in manifest['schedule']:
        cell = RUN / name
        meta = json.loads((cell / 'metadata.json').read_text())
        project = cell / 'project'
        before = inventory(project)
        case = cases[meta['case']]
        for path, source in case['files'].items():
            assert (project / path).read_bytes() == source.encode()
        raw = (cell / 'stdout.original.jsonl').read_text()
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert next(e['usage'] for e in reversed(events) if e['type'] == 'turn.completed') == meta['usage']
        assert meta['completed'] and meta['resource_diagnostics'] == {'changed_paths': []}
        installed = Path(meta['workspace']) / '.agents/skills'
        assert runner.resource_manifest(installed) == meta['installed_resources_before'] == meta['installed_resources_after']
        for path, detail in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', REV + ':skills/' + path], cwd=ROOT)
            mode = subprocess.check_output(['git', 'ls-tree', REV, 'skills/' + path], cwd=ROOT).split()[0]
            assert hashlib.sha256(source).hexdigest() == detail['sha256']
            assert (int(mode, 8) & 0o777) == detail['mode']
        commands = [e['item'] for e in events if e['type'] == 'item.completed'
                    and e.get('item', {}).get('type') == 'command_execution']
        item = next(i for i in commands if 'python3' in i['command'])
        assert item['exit_code'] == 0
        with tempfile.TemporaryDirectory(prefix='qh-ack-replay-', dir=RUN) as folder:
            copy = Path(folder) / 'project'
            shutil.copytree(project, copy)
            copied_before = inventory(copy)
            process = subprocess.run(shlex.split(item['command']), cwd=copy,
                                     capture_output=True, text=True, timeout=30)
            assert process.returncode == 0 and not process.stderr
            if meta['case'].endswith('control'):
                assert process.stdout == item['aggregated_output']
                assert inventory(copy) == copied_before
                normalization = 'none; complete stdout equal'
            else:
                original, end = json.JSONDecoder().raw_decode(item['aggregated_output'])
                replay, replay_end = json.JSONDecoder().raw_decode(process.stdout)
                if meta['arm'] == 'skill':
                    assert Path(original.pop('database')).name == Path(replay.pop('database')).name == 'review.sqlite'
                    normalization = 'only generated database directory differs'
                else:
                    assert item['aggregated_output'][end:].strip().startswith('Results: ')
                    assert process.stdout[replay_end:].strip().startswith('Results: ')
                    normalization = 'only trailing generated Results path differs'
                assert replay == original
                after = inventory(copy)
                assert all(after[path] == value for path, value in copied_before.items())
            output = process.stdout.replace(str(copy), '<REPLAY_PROJECT>')
        assert inventory(project) == before
        report['cells'][name] = {'exit_code': 0, 'stdout': output, 'stderr': '',
            'comparison': normalization, 'observations_match': True,
            'raw_usage_events_resources_reconciled': True, 'originals_unchanged': True,
            'original_project_inventory': before}
    with (RUN / 'author-replay.json').open('x') as stream:
        stream.write(json.dumps(report, indent=2) + '\n')
    print(json.dumps({name: row['comparison'] for name, row in report['cells'].items()}, indent=2))


if __name__ == '__main__':
    main()
