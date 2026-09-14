#!/usr/bin/env python3
"""Frozen checkpoint-07 post-timing checks; never replacement model output."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from replay_hostage_call_01 import inventory

RESOURCE = 'b2816cd76645f2cd13382e27f4222a218e08f24f'
CASES_SHA = '1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65'
ADDED = {
    ('necessary-state', 'baseline'): ['test_form.py'],
    ('necessary-state', 'skill'): ['tests/controlled_call.py', 'tests/test_form.py'],
    ('rolling-schema', 'baseline'): ['release_review/verify.py', 'release_review/evidence.json'],
    ('search-diagnosis', 'baseline'): ['experiments/README.md', 'experiments/search_order.py', 'experiments/search_order_results.json'],
    ('search-diagnosis', 'skill'): ['experiments/search_completion_probe.py'],
    ('search-order', 'baseline'): ['test_search_overlap.py', 'QA_SEARCH_RESULTS.txt'],
    ('search-order', 'skill'): ['test_search.py', 'qa_controlled_fetch.py'],
    ('search-protected', 'baseline'): ['test_search_overlap.py'],
    ('search-protected', 'skill'): ['tests/test_search.py'],
}


def frozen(path):
    return subprocess.check_output(['git', 'show', RESOURCE + ':' + path])


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
        terminal = [e['usage'] for e in events if e['type'] == 'turn.completed']
        assert terminal == [meta['usage']] and meta['completed'] and not meta['timed_out']
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            assert hashlib.sha256(frozen('skills/' + path)).hexdigest() == entry['sha256']
        project = cell / 'project'
        files = inventory(project)
        initial = cases[meta['case']]['files']
        assert set(files) == set(initial) | set(ADDED.get((meta['case'], meta['arm']), [])), name
        changed = sorted(p for p, content in initial.items() if (project / p).read_bytes() != content.encode())
        assert changed == {'boundary-fix': ['eligibility.py', 'test_eligibility.py'], 'necessary-state': ['form.py']}.get(meta['case'], []), (name, changed)
        for target, asset in [('qa_controlled_fetch.py', 'mother-in-law/assets/controlled_fetch.py'),
                              ('tests/controlled_call.py', 'hostage-negotiator/assets/controlled_call.py')]:
            if target in files:
                assert (project / target).read_bytes() == frozen('skills/' + asset)
        report['cells'].append({'cell': name, 'raw_usage_resources_reconciled': True,
                                'total_tokens': meta['usage']['input_tokens'] + meta['usage']['output_tokens'],
                                'elapsed_seconds': meta['elapsed_seconds'],
                                'changed_original_files': changed, 'inventory_sha256': files})

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
            root = 'tests' if arm == 'skill' and case in ('necessary-state', 'search-protected') else '.'
            counts = {'search-order': 2, 'search-protected': 2 if arm == 'baseline' else 3,
                      'boundary-fix': 3, 'necessary-state': 7 if arm == 'baseline' else 5}
            for variant, implementation in variants.items():
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    (scratch / target).write_text(implementation)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', root, '-v']
                    try:
                        result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                        code, timed_out, output = result.returncode, False, result.stdout + result.stderr
                    except subprocess.TimeoutExpired as error:
                        def text(value):
                            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                        code, timed_out, output = None, True, text(error.stdout) + text(error.stderr)
                    expected = int(variant in ('transient', 'original', 'missing_guard', 'missing_cleanup') or case == 'search-order' and variant == 'final')
                    count_ok = re.findall(r'Ran (\d+) tests? in ', output) == [str(counts[case])]
                    unchanged = all((scratch / p).read_bytes() == (project / p).read_bytes() for p in before if p != target)
                    # Missing guard may hang the duplicate until its owned deadline;
                    # original Form lacks pending. Review exact native failures below.
                    failure_seen = any(s in output for s in ('AssertionError', 'TimeoutError', 'AttributeError'))
                    matched = code == expected and not timed_out and count_ok and unchanged and (not expected or failure_seen)
                    report['checks'].append({'cell': name, 'variant': variant, 'command': command,
                        'exit_code': code, 'expected_exit': expected, 'timed_out': timed_out,
                        'matched': matched, 'test_sources_unchanged': unchanged,
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
