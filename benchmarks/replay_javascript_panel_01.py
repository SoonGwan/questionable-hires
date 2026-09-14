#!/usr/bin/env python3
"""Post-timing raw reconciliation and untouched native JS regression controls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from replay_hostage_call_01 import inventory

RESOURCE = '3949ef6'
CASES_SHA = '20545c1e08faf86c67f228c935dce74e947fb1faf983dcce0becbe99290c199c'


def replay(run, resource=RESOURCE, layout='panel-01'):
    assert layout in ('panel-01', 'usage-first-01')
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and len(manifest['schedule']) == 2
    source = subprocess.check_output(['git', 'show', resource + ':benchmarks/hostage-javascript-panel-cases.json'])
    assert hashlib.sha256(source).hexdigest() == CASES_SHA == manifest['cases_sha256']
    case = json.loads(source)[0]
    report = {'kind': 'author reconciliation and replay, not original model evidence',
              'resource': resource, 'reviewed_layout': layout, 'cells': [], 'checks': []}
    for name in manifest['schedule']:
        cell = run / name
        meta = json.loads((cell / 'metadata.json').read_text())
        raw = (cell / 'stdout.original.jsonl').read_text()
        events = [json.loads(line) for line in raw.splitlines()]
        assert [e['usage'] for e in events if e['type'] == 'turn.completed'] == [meta['usage']]
        assert meta['completed'] and not meta['timed_out']
        assert raw.replace(meta['workspace'], '<WORKSPACE>').replace(str(Path.home()), '<HOME>') == (cell / 'events.jsonl').read_text()
        assert meta['installed_resources_before'] == meta['installed_resources_after']
        for path, entry in meta['installed_resources_before'].items():
            content = subprocess.check_output(['git', 'show', resource + ':skills/' + path])
            assert hashlib.sha256(content).hexdigest() == entry['sha256']
        project = cell / 'project'
        before = inventory(project)
        usage_baseline = layout == 'usage-first-01' and meta['arm'] == 'baseline'
        regression = 'panel.regression.test.mjs' if usage_baseline else 'panel.pending.test.mjs'
        test_count = 6 if usage_baseline else 7
        expected = set(case['files']) | {regression}
        if meta['arm'] == 'skill':
            expected.add('test-support/controlled_call.mjs')
            asset = subprocess.check_output(['git', 'show', resource + ':skills/hostage-negotiator/assets/controlled_call.mjs'])
            assert (project / 'test-support/controlled_call.mjs').read_bytes() == asset
        assert set(before) == expected
        for path in ('panel.test.mjs', 'requirements.md'):
            assert (project / path).read_text() == case['files'][path]
        final = (project / 'panel.mjs').read_text()
        guard = '    if (this.pending) return undefined;\n'
        cleanup = '      this.pending = false;'
        assert final.count(guard) == final.count(cleanup) == final.count('save(signal)') == 1
        variants = {'final': final, 'original': case['files']['panel.mjs'],
                    'missing_guard': final.replace(guard, ''),
                    'missing_cleanup': final.replace(cleanup, '      // deliberately missing cleanup'),
                    'wrong_signal': final.replace('save(signal)', 'save(undefined)')}
        for variant, implementation in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as temporary:
                scratch = Path(temporary) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'panel.mjs').write_text(implementation)
                command = ['node', '--test', '--test-reporter=tap']
                try:
                    result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=15)
                    code, output, timed_out = result.returncode, result.stdout + result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def decoded(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, output, timed_out = None, decoded(error.stdout) + decoded(error.stderr), True
                unchanged = all((scratch / path).read_bytes() == (project / path).read_bytes()
                                for path in before if path != 'panel.mjs')
                counts = {key: int(value) for key, value in re.findall(r'^# (tests|pass|fail|cancelled|skipped) (\d+)$', output, re.M)}
                matched = (not timed_out and unchanged and counts.get('tests') == test_count
                           and counts.get('cancelled') == counts.get('skipped') == 0
                           and code == int(variant != 'final')
                           and (counts.get('pass') == test_count if variant == 'final' else counts.get('fail', 0) > 0))
                report['checks'].append({'cell': name, 'variant': variant, 'command': command,
                    'exit_code': code, 'timed_out': timed_out, 'counts': counts,
                    'matched': matched, 'test_sources_unchanged': unchanged,
                    'replacement_source': implementation,
                    'output': output.replace(str(scratch), '<REPLAY>').replace(str(Path.home()), '<HOME>')})
        assert inventory(project) == before
        report['cells'].append({'cell': name, 'raw_resources_reconciled': True,
            'total_tokens': meta['usage']['input_tokens'] + meta['usage']['output_tokens'],
            'elapsed_seconds': meta['elapsed_seconds'], 'inventory_sha256': before})
    report['all_matched'] = all(check['matched'] for check in report['checks'])
    report['retained_projects_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--resource', default=RESOURCE,
                        help='Frozen resource revision; unchanged fixture and explicit reviewed layout only')
    parser.add_argument('--layout', choices=('panel-01', 'usage-first-01'), default='panel-01')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.run.resolve(), args.resource, args.layout)
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps({'cells': len(report['cells']), 'checks': len(report['checks']), 'all_matched': report['all_matched']}))
