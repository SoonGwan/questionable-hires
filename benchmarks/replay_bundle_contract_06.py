#!/usr/bin/env python3
"""Frozen checkpoint-06 reconciliation and post-timing controls, not model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_04 import fingerprint

RESOURCE = '20ec916434e5d0c2035dbc4a96c4924e271743b3'
CASES_SHA = '1c3bd0648fecfad35f65cba144f908b0ffdd39ba28e28f05963722488ffc7f65'


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 18
    cases_bytes = subprocess.check_output([
        'git', 'show', RESOURCE + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(cases_bytes).hexdigest() == CASES_SHA
    cases = {case['id']: case for case in json.loads(cases_bytes)}
    report = {'kind': 'post-timing author reconciliation and replay, not model evidence',
              'resource': RESOURCE, 'cells': [], 'checks': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        usage = next(e['usage'] for e in reversed(events) if e['type'] == 'turn.completed')
        assert usage == meta['usage'] and meta['completed'] and not meta['timed_out']
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(
            str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        for path, entry in meta['installed_resources_before'].items():
            source = subprocess.check_output(['git', 'show', RESOURCE + ':skills/' + path])
            assert hashlib.sha256(source).hexdigest() == entry['sha256']
        project = cell / 'project'
        initial = cases[meta['case']]['files']
        changed = sorted(path for path, content in initial.items()
                         if not (project / path).is_file()
                         or (project / path).read_bytes() != content.encode())
        allowed = {'boundary-fix': ['eligibility.py', 'test_eligibility.py'],
                   'necessary-state': ['form.py']}.get(meta['case'], [])
        assert changed == sorted(allowed), (name, changed)
        inventory = fingerprint(project)
        if (project / 'controlled_fetch.py').exists():
            source = subprocess.check_output([
                'git', 'show', RESOURCE + ':skills/mother-in-law/assets/controlled_fetch.py'])
            assert (project / 'controlled_fetch.py').read_bytes() == source
        report['cells'].append({
            'cell': name, 'raw_usage_resources_reconciled': True,
            'total_tokens': usage['input_tokens'] + usage['output_tokens'],
            'elapsed_seconds': meta['elapsed_seconds'],
            'changed_original_files': changed, 'retained_inventory_sha256': inventory,
            'additional_files': sorted(set(inventory) - set(initial))})

    guarded = cases['search-protected']['files']['search.py']
    assert guarded.count('        self.generation = 0') == 1
    transient = guarded.replace('        self.generation = 0',
                                '        self.generation = 0\n        self.completed_generation = 0')
    transient = transient.replace('            self.result = result',
                                  '            self.result = result\n            self.completed_generation = generation')
    transient += ('        if generation < self.generation and self.completed_generation < self.generation:\n'
                  '            self.result = result\n')
    for case in ('search-protected', 'search-order', 'necessary-state', 'boundary-fix'):
        for arm in ('baseline', 'skill'):
            name = f'{case}--{arm}--1'
            project = run / name / 'project'
            before = fingerprint(project)
            variants = ('original', 'transient') if case == 'search-protected' else (
                ('original', 'guarded') if case == 'search-order' else ('original',))
            # Reviewed retained tests for all eight cells are at project root.
            assert list(project.glob('test_*.py')), name
            for variant in variants:
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    if variant != 'original':
                        (scratch / 'search.py').write_text(transient if variant == 'transient' else guarded)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', '.', '-v']
                    expected = int(variant == 'transient' or case == 'search-order' and variant == 'original')
                    try:
                        result = subprocess.run(command, cwd=scratch, text=True,
                                                capture_output=True, timeout=15)
                        output = result.stdout + result.stderr
                        code, timed_out = result.returncode, False
                    except subprocess.TimeoutExpired as error:
                        def decoded(value):
                            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                        output = decoded(error.stdout) + decoded(error.stderr)
                        code, timed_out = None, True
                    output = output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')
                    counts = re.findall(r'Ran ([0-9]+) tests? in ', output)
                    meaningful = len(counts) == 1 and int(counts[0]) > 0
                    intended = 'AssertionError' in output and 'FAILED (failures=' in output
                    test_sources_unchanged = all(
                        (scratch / path).read_bytes() == (project / path).read_bytes()
                        for path in before if path != 'search.py')
                    report['checks'].append({
                        'cell': name, 'variant': variant, 'command': command,
                        'exit_code': code, 'expected_exit': expected, 'timed_out': timed_out,
                        'test_sources_unchanged': test_sources_unchanged,
                        'matched': not timed_out and code == expected and meaningful
                                   and test_sources_unchanged and (not expected or intended),
                        'replacement_source': None if variant == 'original' else (scratch / 'search.py').read_text(),
                        'output': output})
            assert fingerprint(project) == before
    report['retained_projects_unchanged'] = True
    report['all_matched'] = all(check['matched'] for check in report['checks'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    result = replay(args.run.resolve())
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps({'cells': len(result['cells']), 'checks': len(result['checks']),
                      'all_matched': result['all_matched']}, indent=2))
