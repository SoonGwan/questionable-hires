#!/usr/bin/env python3
"""Unmodified-test author replay, outside timed model execution."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_04 import GUARDED, fingerprint


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest.get('finished_at') and len(manifest['schedule']) == 2
    fixture = json.loads((Path(__file__).parent / 'bundle-contract-cases.json').read_text())
    originals = next(case['files'] for case in fixture if case['id'] == 'search-order')
    report = {'kind': 'author replay after timing; not model evidence', 'cells': []}
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
        project = cell / 'project'
        before = fingerprint(project)
        for path, source in originals.items():
            assert (project / path).read_bytes() == source.encode()
        row = {'cell': name, 'usage_events_resources_reconciled': True,
               'originals_preserved': True, 'total_tokens': usage['input_tokens'] + usage['output_tokens'],
               'elapsed_seconds': meta['elapsed_seconds'], 'replays': []}
        for variant in ('original', 'guarded'):
            with tempfile.TemporaryDirectory(prefix='author-contract-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                if variant == 'guarded':
                    (scratch / 'search.py').write_text(GUARDED)
                args = (['discover', '-s', 'qa', '-p', 'test_search_overlap.py', '-v']
                        if meta['arm'] == 'baseline' else ['-v', 'test_search'])
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest', *args],
                                        cwd=scratch, capture_output=True, text=True, timeout=15)
                output = (result.stdout + result.stderr).replace(str(scratch), '<REPLAY>').replace(
                    str(Path.home()), '<HOME>')
                row['replays'].append({'variant': variant, 'exit_code': result.returncode,
                                       'output': output})
                # Record either valid pass or ordinary failure without assuming
                # the candidate will succeed. Review the actual assertion below.
                assert result.returncode in (0, 1), output
                assert 'Ran ' in output and 'TypeError' not in output and 'RuntimeWarning' not in output
                if result.returncode == 1:
                    assert 'AssertionError' in output and 'failures=1' in output, output
        assert fingerprint(project) == before
        row['retained_project_unchanged'] = True
        report['cells'].append(row)
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
    print(json.dumps([{**{k: v for k, v in row.items() if k != 'replays'},
                       'replays': [{k: v for k, v in check.items() if k != 'output'}
                                   for check in row['replays']]}
                      for row in result['cells']], indent=2))
