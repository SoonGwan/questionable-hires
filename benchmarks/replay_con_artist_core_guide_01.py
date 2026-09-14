#!/usr/bin/env python3
"""Reconcile the frozen screen; replay its actual JSON without filling read gaps."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import stat
import subprocess
import sys
import tempfile

RESOURCE = 'da333ab07c80743cc550a07a5b7a463f500cc933'


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'] == RESOURCE
    assert manifest['schedule'] == ['persistence-test--skill--1']
    source = frozen('benchmarks/bundle-contract-v2-cases.json')
    assert hashlib.sha256(source).hexdigest() == manifest['cases_sha256']
    case = next(c for c in json.loads(source) if c['id'] == 'persistence-test')
    cell = run / manifest['schedule'][0]
    meta = json.loads((cell / 'metadata.json').read_text())
    raw = (cell / 'stdout.original.jsonl').read_text()
    events = [json.loads(line) for line in raw.splitlines()]
    assert meta['completed'] and not meta['timed_out'] and meta['exit_code'] == 0
    assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
    assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
    assert meta['installed_resources_before'] == meta['installed_resources_after']
    assets = {p: frozen('skills/' + p) for p in meta['installed_resources_before']}
    for name, content in assets.items():
        entry = meta['installed_resources_before'][name]
        assert hashlib.sha256(content).hexdigest() == entry['sha256']
        mode = subprocess.check_output(['git', 'ls-tree', RESOURCE, '--', 'skills/' + name]).split()[0]
        assert stat.S_IMODE(int(mode, 8)) == entry['mode']
    project = cell / 'project'
    assert not any(p.is_symlink() for p in project.rglob('*'))
    before = {p.relative_to(project).as_posix(): (p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
              for p in project.rglob('*') if p.is_file()}
    assert before == {p: (s.encode(), 0o644) for p, s in case['files'].items()}
    commands = [e['item'] for e in events if e['type'] == 'item.completed'
                and e.get('item', {}).get('type') == 'command_execution']
    item = next(c for c in commands if c['id'] == 'item_3')
    shell = shlex.split(item['command'])[2]
    prefix = "git status --short; python3 .agents/skills/con-artist/scripts/audit.py --spec - <<'JSON'\n"
    assert shell.startswith(prefix) and shell.endswith('\nJSON')
    recipe = json.loads(shell[len(prefix):-len('\nJSON')])
    observed = json.loads(item['aggregated_output'])
    expected = dict(correct_tests=0, mutant_tests=0, correct_probe=0, mutant_probe=1)

    def verify(result):
        assert result['status'] == 'observed'
        assert {k: v['exit_code'] for k, v in result['checks'].items()} == expected
        for name, check in result['checks'].items():
            assert not check['timed_out'] and not check['output_truncated']
            assert 'Verified actual test_save global save is copied service.save' in check['output']
            assert 'Verified copied import: service ' in check['output']
            assert 'Verified copied import: test_service ' in check['output']
            if name.endswith('_tests'):
                assert 'test_save (test_service.SaveTests)' in check['output']
                assert 'Ran 1 test in ' in check['output'] and '\nOK\n' in check['output']
        assert "Stored records: ['existing', 'record']" in result['checks']['correct_probe']['output']
        assert "AssertionError: Expected preserved existing record and appended new record; got ['existing']" in result['checks']['mutant_probe']['output']
        assert result['integrity'] == dict(selected_files=2,
            selected_original_bytes_and_modes_unchanged=True, owned_scratch_removed=True)

    verify(observed)
    with tempfile.TemporaryDirectory(prefix='author-audit-', dir=run) as temporary:
        root = Path(temporary)
        for name, (content, mode) in before.items():
            (root / name).write_bytes(content)
            (root / name).chmod(mode)
        for name, content in assets.items():
            dest = root / '.agents/skills' / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(content)
        process = subprocess.run([sys.executable, '-B', str(root / '.agents/skills/con-artist/scripts/audit.py'),
                                  '--spec', '-'], cwd=root, input=json.dumps(recipe),
                                 capture_output=True, text=True, timeout=40)
        assert process.returncode == 0, process.stderr
        result = json.loads(process.stdout)
        verify(result)
        assert not list(root.glob('.con-artist-*'))
        for name, (content, mode) in before.items():
            assert (root / name).read_bytes() == content
            assert stat.S_IMODE((root / name).stat().st_mode) == mode
        redacted = process.stdout.replace(str(root), '<REPLAY>').replace(str(Path.home()), '<HOME>')
    assert before == {p.relative_to(project).as_posix(): (p.read_bytes(), stat.S_IMODE(p.stat().st_mode))
                      for p in project.rglob('*') if p.is_file()}
    return dict(kind='separate author reconciliation/replay, not original model evidence',
        resource=RESOURCE, raw_usage_resources_inventory_reconciled=True,
        original_recipe=recipe, native_phase_exits=expected, replay=json.loads(redacted),
        original_project_preserved=True,
        limitation='Recorded commands do not show project-source or guide reads; replay does not establish guide adoption.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite a previous author attempt')
    result = replay(args.run.resolve())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('Reconciled original evidence; unchanged recipe reproduced all four expected phases.')
