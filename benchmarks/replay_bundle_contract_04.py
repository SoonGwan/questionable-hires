#!/usr/bin/env python3
"""Post-run author checks, never a replacement for measured model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


GUARDED = '''class Search:
    def __init__(self):
        self.result = None
        self._generation = 0
    async def run(self, query, fetch):
        self._generation += 1
        generation = self._generation
        result = await fetch(query)
        if generation == self._generation:
            self.result = result
'''


def fingerprint(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 18
    report = {'kind': 'author replay after all model timing; not model evidence',
              'cells': [], 'replays': []}
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
        report['cells'].append({'cell': name, 'usage_events_resources_reconciled': True,
                                'total_tokens': usage['input_tokens'] + usage['output_tokens'],
                                'elapsed_seconds': meta['elapsed_seconds']})

    for case in ('search-order', 'necessary-state'):
        for arm in ('baseline', 'skill'):
            name = f'{case}--{arm}--1'
            project = run / name / 'project'
            before = fingerprint(project)
            variants = ('original', 'guarded', 'original-contract-only',
                        'guarded-contract-only') if case == 'search-order' else ('original',)
            for variant in variants:
                with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    if variant.startswith('guarded'):
                        (scratch / 'search.py').write_text(GUARDED)
                    if case == 'search-order':
                        tests = 'qa' if arm == 'baseline' else 'tests'
                        if variant.endswith('contract-only'):
                            test = scratch / tests / ('test_search_overlap.py' if arm == 'baseline'
                                                     else 'test_search.py')
                            source = test.read_text()
                            old = ('            self.assertEqual(search.result, values[first])'
                                   if arm == 'baseline' else
                                   '        self.assertEqual(self.search.result, first_result)')
                            new = ('            if first == queries[-1]:\n    ' + old
                                   if arm == 'baseline' else
                                   '        if reverse:\n    ' + old)
                            assert source.count(old) == 1
                            test.write_text(source.replace(old, new))
                        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', tests, '-v']
                    else:
                        command = [sys.executable, '-B', '-m', 'unittest', '-v']
                    result = subprocess.run(command, cwd=scratch, capture_output=True,
                                            text=True, timeout=15)
                    output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                        str(Path.home()), '<HOME>')
                    expected_exit = 0 if case == 'necessary-state' or variant == 'guarded-contract-only' else 1
                    assert result.returncode == expected_exit, output
                    if expected_exit:
                        assert 'AssertionError' in output and 'failures=1' in output, output
                    assert 'TypeError' not in output and 'RuntimeWarning' not in output, output
                    report['replays'].append({'cell': name, 'variant': variant,
                                              'exit_code': result.returncode, 'output': output})
            assert fingerprint(project) == before
    report['retained_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = replay(args.run.resolve())
    with args.output.open('x') as output:
        json.dump(result, output, indent=2)
        output.write('\n')
    print(json.dumps([{k: v for k, v in row.items() if k != 'output'}
                      for row in result['replays']], indent=2))
