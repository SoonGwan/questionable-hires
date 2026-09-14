#!/usr/bin/env python3
"""Preserve exact-program replay disagreements with original captured outputs."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import shlex
import stat
import subprocess
import sys
import tempfile

RESOURCE = '360775feaed941d7461bb3922f3f6902dbd7034c'
PROFILES = {
    'sqlite-01': (RESOURCE, [('baseline', 'item_5', 'PY'), ('skill', 'item_6', 'JSON')],
                  'test_durability_audit.py'),
    'probe-routing-01': ('bcc6713', [('skill', 'item_5', 'JSON')], 'test_persistence_audit.py'),
}


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def inventory(root):
    assert not any(p.is_symlink() for p in root.rglob('*'))
    return {p.relative_to(root).as_posix(): (hashlib.sha256(p.read_bytes()).hexdigest(), stat.S_IMODE(p.stat().st_mode))
            for p in root.rglob('*') if p.is_file()}


def replay(run, profile='sqlite-01'):
    revision, selections, probe_name = PROFILES[profile]
    resource = subprocess.check_output(['git', 'rev-parse', revision]).decode().strip()
    def frozen(path):
        return subprocess.check_output(['git', 'show', resource + ':' + path])
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'] == resource
    assert manifest['schedule'] == [f'sqlite-commit-audit--{arm}--1' for arm, _, _ in selections]
    source = frozen('benchmarks/con-artist-sqlite-cases.json')
    assert hashlib.sha256(source).hexdigest() == manifest['cases_sha256']
    case = json.loads(source)[0]
    report = dict(kind='separate exact-program author replay; not replacement model output', resource=resource, cells=[])
    for arm, item_id, delimiter in selections:
        cell = run / f'sqlite-commit-audit--{arm}--1'
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert meta['completed'] and not meta['timed_out']
        assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        assets = {p: frozen('skills/' + p) for p in meta['installed_resources_before']}
        for name, content in assets.items():
            entry = meta['installed_resources_before'][name]
            assert hashlib.sha256(content).hexdigest() == entry['sha256']
            mode = subprocess.check_output(['git', 'ls-tree', resource, '--', 'skills/' + name]).split()[0]
            assert stat.S_IMODE(int(mode, 8)) == entry['mode']
        before = inventory(cell / 'project')
        assert before == {p: (hashlib.sha256(s.encode()).hexdigest(), 0o644) for p, s in case['files'].items()}
        item = next(e['item'] for e in events if e['type'] == 'item.completed' and e.get('item', {}).get('id') == item_id)
        shell = shlex.split(item['command'])[2]
        body = shell.split("<<'" + delimiter + "'\n", 1)[1]
        assert body.endswith('\n' + delimiter)
        body = body[:-len('\n' + delimiter)]
        if arm == 'skill':
            recipe = json.loads(body)  # Pass the original JSON bytes unchanged below.
            probe_source = recipe['probe_files'][probe_name]
            binary = lambda s: [n.value.hex() for n in ast.walk(ast.parse(s))
                                if isinstance(n, ast.Constant) and isinstance(n.value, bytes)]
            literals = dict(probe=binary(probe_source), fixture=binary(case['files']['test_receipts.py']))
            assert '00ff6e6577' in literals['probe'] and '00ff6e6577' in literals['fixture']
            report['decoded_binary_literals_hex'] = literals
        with tempfile.TemporaryDirectory(prefix='sqlite-replay-', dir=run) as temporary:
            root = Path(temporary)
            for name, content in case['files'].items():
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)
            for name, content in assets.items():
                p = root / '.agents/skills' / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(content)
            original = inventory(root)
            command = ([sys.executable, '-B', '-'] if arm == 'baseline' else
                       [sys.executable, '-B', '.agents/skills/con-artist/scripts/audit.py', '--spec', '-'])
            try:
                process = subprocess.run(command, input=body, cwd=root, capture_output=True, text=True, timeout=40)
                code, timed_out, stdout, stderr = process.returncode, False, process.stdout, process.stderr
            except subprocess.TimeoutExpired as error:
                def text(value):
                    return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                code, timed_out, stdout, stderr = None, True, text(error.stdout), text(error.stderr)
            assert inventory(root) == original
            def redact(value):
                return value.replace(str(root), '<REPLAY>').replace(str(Path.home()), '<HOME>')
            report['cells'].append(dict(arm=arm, raw_resources_originals_reconciled=True,
                original_body=body, body_sha256=hashlib.sha256(body.encode()).hexdigest(),
                original_exit=item['exit_code'], replay_exit=code, timed_out=timed_out,
                stdout=redact(stdout), stderr=redact(stderr), replay_inputs_unchanged=True,
                limitation='Exit agreement alone does not prove matching native evidence; inspect all phases.'))
        assert inventory(cell / 'project') == before
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--profile', choices=PROFILES, default='sqlite-01')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier attempt')
    report = replay(args.run.resolve(), args.profile)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([dict(arm=c['arm'], original_exit=c['original_exit'], replay_exit=c['replay_exit']) for c in report['cells']]))
