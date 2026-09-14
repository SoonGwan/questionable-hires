#!/usr/bin/env python3
"""Checkpoint-08 author controls; never replacement original model evidence."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile

from replay_hostage_call_01 import inventory

RESOURCE = 'de3cbc0288cc27ee1c3f04811b062f9e56b9357e'
CASES_SHA = '1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65'
ADDED = {
    ('necessary-state', 'baseline'): ['test_form.py'],
    ('necessary-state', 'skill'): ['tests/__init__.py', 'tests/controlled_call.py', 'tests/test_form.py'],
    ('rolling-schema', 'baseline'): ['review/verify_release.py', 'review/verification.json'],
    ('search-diagnosis', 'baseline'): ['experiments/README.md', 'experiments/search_completion_order.py', 'experiments/search_completion_order.results.json'],
    ('search-diagnosis', 'skill'): ['experiments/search_order_probe.py'],
    ('search-order', 'baseline'): ['test_search_overlap.py', 'qa-results.txt'],
    ('search-order', 'skill'): ['test_search.py'],
    ('search-protected', 'baseline'): ['test_search_race.py'],
    ('search-protected', 'skill'): ['test_search.py'],
}


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


def transport_classes(source):
    """Compare copied runtime AST while permitting omitted usage docstrings."""
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
    return {n.name: ast.dump(n) for n in tree.body
            if isinstance(n, ast.ClassDef) and n.name in ('Request', 'ControlledFetch')}


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and manifest['revision'] == RESOURCE
    assert len(manifest['schedule']) == len(set(manifest['schedule'])) == 18
    source = frozen('benchmarks/bundle-contract-v2-cases.json')
    assert hashlib.sha256(source).hexdigest() == manifest['cases_sha256'] == CASES_SHA
    cases = {c['id']: c for c in json.loads(source)}
    report = {'kind': 'separate post-timing author reconciliation and replay',
              'resource': RESOURCE, 'cells': [], 'checks': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
        assert meta['completed'] and not meta['timed_out'] and meta['exit_code'] == 0
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            assert hashlib.sha256(frozen('skills/' + path)).hexdigest() == entry['sha256']
            mode = subprocess.check_output(['git', 'ls-tree', RESOURCE, '--', 'skills/' + path]).split()[0]
            assert stat.S_IMODE(int(mode, 8)) == entry['mode']
        project = cell / 'project'
        files = inventory(project)
        initial = cases[meta['case']]['files']
        assert set(files) == set(initial) | set(ADDED.get((meta['case'], meta['arm']), [])), name
        changed = sorted(p for p, content in initial.items() if (project / p).read_bytes() != content.encode())
        assert changed == {'boundary-fix': ['eligibility.py', 'test_eligibility.py'], 'necessary-state': ['form.py']}.get(meta['case'], []), (name, changed)
        assert all(stat.S_IMODE((project / p).stat().st_mode) == 0o644 for p in initial), name
        if meta['arm'] == 'skill' and meta['case'] == 'necessary-state':
            assert (project / 'tests/controlled_call.py').read_bytes() == frozen('skills/hostage-negotiator/assets/controlled_call.py')
        if meta['arm'] == 'skill' and meta['case'] in ('search-order', 'search-protected'):
            assert transport_classes((project / 'test_search.py').read_bytes()) == transport_classes(frozen('skills/mother-in-law/assets/controlled_fetch.py'))
        report['cells'].append({'cell': name, 'raw_usage_resources_reconciled': True,
            'total_tokens': meta['usage']['input_tokens'] + meta['usage']['output_tokens'],
            'elapsed_seconds': meta['elapsed_seconds'], 'changed_original_files': changed,
            'original_modes_preserved': True, 'inventory_sha256': files,
            'original_capture_diagnostics': meta['capture_diagnostics']})

    guarded = cases['search-protected']['files']['search.py']
    transient = guarded.replace('        self.generation = 0', '        self.generation = 0\n        self.completed_generation = 0')
    transient = transient.replace('            self.result = result', '            self.result = result\n            self.completed_generation = generation')
    transient += ('        if generation < self.generation and self.completed_generation < self.generation:\n'
                  '            self.result = result\n')
    for case in ('search-order', 'search-protected', 'boundary-fix', 'necessary-state'):
        for arm in ('baseline', 'skill'):
            name = f'{case}--{arm}--1'
            project = run / name / 'project'
            before = inventory(project)
            target = 'form.py' if case == 'necessary-state' else 'eligibility.py' if case == 'boundary-fix' else 'search.py'
            final = (project / target).read_text()
            variants = {'final': final}
            if case == 'search-order':
                variants['guarded'] = guarded
            elif case == 'search-protected':
                variants['transient'] = transient
            else:
                variants['original'] = cases[case]['files'][target]
            if case == 'necessary-state':
                guard = '        if self.pending:\n            return' + (' None' if arm == 'baseline' else '') + '\n'
                cleanup = '        finally:\n            self.pending = False'
                assert final.count(guard) == final.count(cleanup) == 1
                variants['missing_guard'] = final.replace(guard, '')
                variants['missing_cleanup'] = final.replace(cleanup, '        finally:\n            pass')
                variants['valid_duplicate_false'] = final.replace(guard, '        if self.pending:\n            return False\n')
            count = {'search-order': 2, 'search-protected': 3 if arm == 'baseline' else 7,
                     'boundary-fix': 3, 'necessary-state': 6}[case]
            for variant, implementation in variants.items():
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    (scratch / target).write_text(implementation)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', '.', '-v']
                    try:
                        result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                        code, timed_out, output = result.returncode, False, result.stdout + result.stderr
                    except subprocess.TimeoutExpired as error:
                        def text(value):
                            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                        code, timed_out, output = None, True, text(error.stdout) + text(error.stderr)
                    expected = int(variant in ('transient', 'original', 'missing_guard', 'missing_cleanup') or case == 'search-order' and variant == 'final')
                    count_ok = re.findall(r'Ran (\d+) tests? in ', output) == [str(count)]
                    unchanged = all((scratch / p).read_bytes() == (project / p).read_bytes() for p in before if p != target)
                    failure_seen = any(s in output for s in ('AssertionError', 'TimeoutError', 'AttributeError'))
                    matched = code == expected and not timed_out and count_ok and unchanged and (not expected or failure_seen)
                    report['checks'].append({'cell': name, 'variant': variant, 'command': command,
                        'exit_code': code, 'expected_exit': expected, 'timed_out': timed_out,
                        'expected_test_count': count, 'matched': matched, 'test_sources_unchanged': unchanged,
                        'replacement_source': implementation,
                        'output': output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')})
            assert inventory(project) == before
    report['all_matched'] = all(c['matched'] for c in report['checks'])
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
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps({'cells': len(report['cells']), 'checks': len(report['checks']), 'all_matched': report['all_matched']}))
