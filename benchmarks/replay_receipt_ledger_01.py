#!/usr/bin/env python3
"""Replay actual ledger programs, restoring captured indexes only in owned copies."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT/'benchmarks/local-runs/receipt-ledger-01'
REV = '2d8785d'


def inventory(root):
    result = {'.': ('directory', root.stat().st_mode & 0o7777)}
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode & 0o7777
        if path.is_symlink():
            result[name] = ('link', mode, str(path.readlink()))
        elif path.is_file():
            result[name] = ('file', mode, hashlib.sha256(path.read_bytes()).hexdigest())
        else:
            result[name] = ('directory', mode)
    return result


def normalize(text, root):
    text = text.replace(str(root), '<PROJECT>')
    text = re.sub(r'\.(receipt|delivery-compare)-[^/\s"\\]+', r'.\1-<COPY>', text)
    return re.sub(r'Ran 5 tests in [0-9.]+s', 'Ran 5 tests in <TIME>s', text)


def main():
    spec = importlib.util.spec_from_file_location('runner', ROOT/'benchmarks/run.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    manifest = json.loads((RUN/'run.json').read_text())
    assert manifest['revision'].startswith(REV) and manifest.get('finished_at')
    frozen = subprocess.check_output(['git', 'show', REV+':benchmarks/receipt-ledger-cases.json'], cwd=ROOT)
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256']
    cases = {case['id']: case for case in json.loads(frozen)}
    reports = []
    for cell in sorted(RUN.glob('*--*')):
        meta = json.loads((cell/'metadata.json').read_text())
        workspace = Path(meta['workspace'])
        original_inventory = inventory(workspace)
        original_project = inventory(cell/'project')
        case = cases[meta['case']]
        expected = dict(case['files'], **case['working_files'])
        assert {p.relative_to(cell/'project').as_posix() for p in (cell/'project').rglob('*') if p.is_file()} == set(expected)
        for path, content in expected.items():
            assert (workspace/path).read_bytes() == (cell/'project'/path).read_bytes() == content.encode()
        resources = runner.resource_manifest(workspace/'.agents/skills')
        assert resources == meta['installed_resources_before'] == meta['installed_resources_after']
        for path, info in resources.items():
            blob = subprocess.check_output(['git', 'show', REV+':skills/'+path], cwd=ROOT)
            mode = subprocess.check_output(['git', 'ls-tree', REV, 'skills/'+path], cwd=ROOT).split()[0]
            assert hashlib.sha256(blob).hexdigest() == info['sha256']
            assert int(mode, 8) & 0o777 == info['mode']
        raw = (cell/'stdout.original.jsonl').read_text()
        assert raw.replace(str(workspace), '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell/'events.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert next(e['usage'] for e in reversed(events) if e['type']=='turn.completed') == meta['usage']
        items = [e['item'] for e in events if e['type']=='item.completed' and "python3 -B - <<" in e.get('item', {}).get('command', '')]
        assert len(items) == 1
        item = items[0]
        script = shlex.split(item['command'])[-1]
        assert script.startswith('python3 -B - <<')
        index_record = meta['pre_collection_index']
        index = (cell/index_record['file']).read_bytes()
        assert index_record['status'] == 'retained'
        assert len(index) == index_record['bytes'] and hashlib.sha256(index).hexdigest() == index_record['sha256']
        with tempfile.TemporaryDirectory(prefix='ledger-replay-', dir=RUN) as folder:
            copy = Path(folder)/'project'
            shutil.copytree(workspace, copy)
            (copy/'.git/index').write_bytes(index)
            (copy/'.git/index').chmod(index_record['mode'])
            before = inventory(copy)
            completed = subprocess.run(['/bin/zsh', '-lc', script], cwd=copy,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=45)
            after_inventory = inventory(copy)
            replay_changes = sorted(path for path in before.keys() | after_inventory.keys()
                                    if before.get(path) != after_inventory.get(path))
            original = normalize(item['aggregated_output'], workspace)
            replay = normalize(completed.stdout, copy)
            original_prefix_gap = False
            if meta['arm'] == 'skill':
                original_result, _ = json.JSONDecoder().raw_decode(original)
                replay_result, _ = json.JSONDecoder().raw_decode(replay)
                helper_equal = original_result == replay_result
                for phase, expected_exit in [('before', 1), ('after', 0 if meta['case'].endswith('-a') else 1)]:
                    check = original_result['checks'][phase]
                    assert check['exit_code'] == expected_exit and 'Ran 5 tests' in check['output']
                    assert len(re.findall(r'^test_.* \.\.\. ', check['output'], re.M)) == 5
                assert original_result['tree_guard']['unchanged']
            else:
                assert len(re.findall(r'^test_.* \.\.\. ', original, re.M)) == 10
                assert original.count('Ran 5 tests') == 2
                # One original capture starts after the first revision/overlay prefix.
                if meta['case'].endswith('-a'):
                    start = replay.index('IMPORT ledger ')
                    original_prefix_gap = bool(replay[:start].strip())
                    assert original == replay[start:]
                else:
                    assert original == replay
            reports.append(dict(cell=cell.name, kind='separate exact-program author replay',
                exit_code=completed.returncode, restored_index_sha256=index_record['sha256'],
                original_prefix_gap=original_prefix_gap,
                helper_object_equal=helper_equal if meta['arm']=='skill' else None,
                replay_changed_paths=replay_changes,
                original_inventories_unchanged=True,
                normalization='project/copy paths and native durations only',
                output=completed.stdout.replace(str(copy), '<REPLAY_PROJECT>')))
        assert inventory(workspace) == original_inventory and inventory(cell/'project') == original_project
    with (RUN/'author-replay.json').open('x') as stream:
        stream.write(json.dumps(reports, indent=2)+'\n')
    print(json.dumps([{key: row[key] for key in ('cell', 'exit_code', 'helper_object_equal', 'replay_changed_paths')} for row in reports], indent=2))


if __name__ == '__main__':
    main()
