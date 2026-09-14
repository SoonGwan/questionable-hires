#!/usr/bin/env python3
"""Reconcile a frozen Friday screen and replay its actual assertion program."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tempfile

RESOURCE = '37686ac'


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def replay(run):
    run = run.resolve()
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'].startswith(RESOURCE)
    assert manifest['schedule'] == ['rolling-schema--skill--1']
    case_bytes = frozen('benchmarks/bundle-contract-v2-cases.json')
    assert hashlib.sha256(case_bytes).hexdigest() == manifest['cases_sha256']
    case = next(c for c in json.loads(case_bytes) if c['id'] == 'rolling-schema')
    cell = run / manifest['schedule'][0]
    meta = json.loads((cell / 'metadata.json').read_text())
    raw = (cell / 'stdout.original.jsonl').read_text()
    events = [json.loads(line) for line in raw.splitlines()]
    assert meta['completed'] and not meta['timed_out']
    assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
    assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
    assert meta['installed_resources_before'] == meta['installed_resources_after']
    assets = {name: frozen('skills/' + name) for name in meta['installed_resources_before']}
    for name, content in assets.items():
        assert hashlib.sha256(content).hexdigest() == meta['installed_resources_before'][name]['sha256']
    project = cell / 'project'
    assert not any(p.is_symlink() for p in project.rglob('*'))
    retained = {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob('*') if p.is_file()}
    assert retained == {name: text.encode() for name, text in case['files'].items()}
    commands = [e['item'] for e in events if e['type'] == 'item.completed'
                and e.get('item', {}).get('type') == 'command_execution']
    item = next(c for c in commands if c['id'] == 'item_5')
    args = shlex.split(item['command'])
    shell_code = args[2]
    prefix = "python3 - <<'PY'\n"
    assert shell_code.startswith(prefix) and shell_code.endswith('\nPY')
    code = shell_code[len(prefix):-len('\nPY')]
    tree = ast.parse(code)
    recipes = [n.value for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == 'recipe' for t in n.targets)]
    assert len(recipes) == 1
    recipe = ast.literal_eval(recipes[0])
    observed = json.loads(item['aggregated_output'].splitlines()[0])
    assert item['exit_code'] == 0 and observed['complete'] and len(observed['phases']) == 4
    assert all(set(p['checks']) == {'old reader', 'new reader'} for p in observed['phases'])
    report = dict(kind='separate author reconciliation/replay, not model output', resource=RESOURCE,
        reconciled=True, original_recipe=recipe, original_program=code, original_observations=observed,
        inventory_sha256={name: hashlib.sha256(content).hexdigest() for name, content in retained.items()}, checks=[])
    for variant in ('original_release', 'rollback_loses_inserted_row'):
        with tempfile.TemporaryDirectory(prefix='friday-replay-', dir=run) as temporary:
            root = Path(temporary)
            for name, content in retained.items():
                (root / name).write_bytes(content)
            for name, content in assets.items():
                target = root / '.agents/skills' / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            if variant != 'original_release':
                with (root / '002_down.sql').open('a') as stream:
                    stream.write('DELETE FROM users WHERE id = 3;\n')
            before = {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = subprocess.run(['python3', '-B', '-'], input=code, cwd=root,
                                    capture_output=True, text=True, timeout=20)
            output = result.stdout + result.stderr
            expected = int(variant != 'original_release')
            assert result.returncode == expected, output
            if not expected:
                assert json.loads(result.stdout.splitlines()[0]) == observed
                assert 'PASS: all reader outcomes' in output
            else:
                assert 'AssertionError:' in output and "'rows': [(1, 'Updated by new schema'), (2, 'Unchanged')]" in output
                assert 'PASS: all reader outcomes' not in output
            assert before == {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            report['checks'].append(dict(variant=variant, exit_code=result.returncode, expected_exit=expected,
                program_unchanged=True, files_unchanged=True,
                output=output.replace(str(root), '<REPLAY>').replace(str(Path.home()), '<HOME>')))
    assert retained == {p.relative_to(project).as_posix(): p.read_bytes() for p in project.rglob('*') if p.is_file()}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.run)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('Raw/resources/files reconciled; original passes, data-loss rollback rejected.')
