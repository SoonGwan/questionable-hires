#!/usr/bin/env python3
"""Retained search QA controls; never substitute for original model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

from replay_bundle_contract_09_form import REVISION, CASES_SHA, inventory


def replay(run):
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['revision'] == REVISION and manifest['finished_at']
    frozen = subprocess.check_output(['git', 'show', REVISION + ':benchmarks/bundle-contract-v2-cases.json'])
    assert hashlib.sha256(frozen).hexdigest() == manifest['cases_sha256'] == CASES_SHA
    cases = {c['id']: c for c in json.loads(frozen)}
    guarded = cases['search-protected']['files']['search.py']
    transient = guarded.replace('        self.generation = 0',
        '        self.generation = 0\n        self.completed_generation = 0')
    transient = transient.replace('            self.result = result',
        '            self.result = result\n            self.completed_generation = generation')
    transient += ('        if generation < self.generation and self.completed_generation < self.generation:\n'
                  '            self.result = result\n')
    clearing = guarded.replace('        self.generation += 1',
                               '        self.result = None\n        self.generation += 1')
    report = dict(kind='separate native author controls, not original model execution',
                  revision=REVISION, cases_sha256=CASES_SHA, cells=[], checks=[])
    additions = {
        ('search-order', 'baseline'): {'test_search_overlap.py', 'search_qa_results.txt'},
        ('search-order', 'skill'): {'test_search.py', 'controlled_fetch.py'},
        ('search-protected', 'baseline'): {'test_search_local.py'},
        ('search-protected', 'skill'): {'tests/test_search.py', 'tests/controlled_fetch.py'},
    }
    for case in ('search-order', 'search-protected'):
        for arm in ('baseline', 'skill'):
            name = case + '--' + arm + '--1'
            cell, project = run / name, run / name / 'project'
            meta = json.loads((cell / 'metadata.json').read_text())
            def redact(text):
                return text.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>')
            before = inventory(project)
            assert set(before) == set(cases[case]['files']) | additions[case, arm]
            assert all((project / p).read_text() == source for p, source in cases[case]['files'].items())
            if arm == 'skill':
                path = 'controlled_fetch.py' if case == 'search-order' else 'tests/controlled_fetch.py'
                asset = subprocess.check_output(['git', 'show', REVISION + ':skills/mother-in-law/assets/controlled_fetch.py'])
                assert (project / path).read_bytes() == asset
            events = [json.loads(line) for line in (cell / 'events.jsonl').read_text().splitlines()]
            native = [e['item'] for e in events if e.get('type') == 'item.completed'
                      and e.get('item', {}).get('type') == 'command_execution'
                      and 'unittest' in e['item'].get('command', '')]
            count = 2 if case == 'search-order' else 4 if arm == 'baseline' else 3
            assert len(native) == 1
            output = native[0]['aggregated_output']
            original_counts = re.findall(r'Ran (\d+) tests? in ', output)
            assert original_counts == [str(count)]
            report['cells'].append(dict(cell=name, inventory_sha256=before,
                retained_sources={p: redact((project / p).read_text()) for p in sorted(before)},
                source_export_note='Source inventory hashes identify originals; exported text redacts local paths.',
                original_native_command=native[0], original_test_counts=original_counts))
            variants = ({'original_stale': (cases[case]['files']['search.py'], 1),
                         'valid_guarded': (guarded, 0), 'valid_intermediate_old': (transient, 0)}
                        if case == 'search-order' else
                        {'original_guarded': (guarded, 0), 'transient_stale': (transient, 1),
                         'clear_existing_on_start': (clearing, 1)})
            for variant, (source, expected) in variants.items():
                with tempfile.TemporaryDirectory(prefix='author-search-', dir=run) as temporary:
                    scratch = Path(temporary) / 'project'
                    shutil.copytree(project, scratch)
                    (scratch / 'search.py').write_text(source)
                    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s',
                               'tests' if case == 'search-protected' and arm == 'skill' else '.', '-v']
                    try:
                        result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=20)
                        code, output, timed_out = result.returncode, result.stdout + result.stderr, False
                    except subprocess.TimeoutExpired as error:
                        def text(value):
                            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                        code, output, timed_out = None, text(error.stdout) + text(error.stderr), True
                    counts = re.findall(r'Ran (\d+) tests? in ', output)
                    unchanged = all((scratch / p).read_bytes() == (project / p).read_bytes()
                                    for p in before if p != 'search.py')
                    matched = (code == expected and not timed_out and counts == [str(count)]
                               and unchanged and (expected == 0 or 'AssertionError:' in output))
                    report['checks'].append(dict(cell=name, variant=variant, command=command,
                        implementation=source, expected_exit=expected, exit_code=code,
                        expected_test_count=count, observed_test_counts=counts,
                        timed_out=timed_out, test_sources_unchanged=unchanged, matched=matched,
                        output=output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')))
            assert inventory(project) == before
    report['retained_projects_unchanged'] = True
    report['all_matched'] = all(c['matched'] for c in report['checks'])
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.run.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(dict(checks=len(report['checks']), all_matched=report['all_matched'])))
