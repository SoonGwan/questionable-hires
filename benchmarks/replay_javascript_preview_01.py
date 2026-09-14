#!/usr/bin/env python3
"""Reviewed PreviewLoader exports: raw reconciliation and untouched native controls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from replay_hostage_call_01 import inventory

RESOURCE = '4a064bc'
CASES_SHA = 'fd9d98e8557845c3f25aff22f7576c850323f7c0a815528427f7c486338f8c5c'


def replay(run, in_place_probe=False, profile='preview-01'):
    assert profile in ('preview-01', 'state-contents-01')
    adoption = profile == 'state-contents-01'
    resource = '691f896' if adoption else RESOURCE
    manifest = json.loads((run / 'run.json').read_text())
    assert manifest['finished_at'] and len(manifest['schedule']) == (1 if adoption else 2)
    source = subprocess.check_output(['git', 'show', resource + ':benchmarks/hostage-javascript-preview-cases.json'])
    assert hashlib.sha256(source).hexdigest() == CASES_SHA == manifest['cases_sha256']
    case = json.loads(source)[0]
    report = {'kind': 'author reconciliation and replay; not original model evidence',
              'resource': resource, 'reviewed_profile': profile, 'post_review_in_place_probe': in_place_probe,
              'cells': [], 'checks': []}
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
        expected = set(case['files']) | {'preview.regression.test.mjs'}
        skill = meta['arm'] == 'skill'
        test_count = 58 if adoption else (54 if skill else 33)
        if skill:
            expected.add('test-support/controlled_call.mjs')
            asset = subprocess.check_output(['git', 'show', resource + ':skills/hostage-negotiator/assets/controlled_call.mjs'])
            assert (project / 'test-support/controlled_call.mjs').read_bytes() == asset
        assert set(before) == expected
        for path in ('preview.test.mjs', 'requirements.md'):
            assert (project / path).read_text() == case['files'][path]
        final = (project / 'preview.mjs').read_text()
        owner = '#latestRequest' if skill and not adoption else '#request'
        token = 'Symbol()' if skill and not adoption else '{}'
        guard = f'if (this.{owner} === request)'
        assert final.count(guard) == 2
        assert final.count(f'const request = this.{owner} = {token};') == 1
        assert final.count('decode(bytes, signal)') == 1
        success_fault = final.replace(guard, 'if (true)', 1)
        prefix, suffix = final.split('    } catch (error) {')
        error_fault = prefix + '    } catch (error) {' + suffix.replace(guard, 'if (true)', 1)
        global_fault = ('let sharedOwner;\n' + final.replace(f'  {owner};\n', '')
                        .replace(f'this.{owner}', 'sharedOwner'))
        variants = {
            'final': final, 'original': case['files']['preview.mjs'],
            'stale_success': success_fault, 'stale_error': error_fault,
            'reused_token': final.replace(f'const request = this.{owner} = {token};',
                                         f'const request = this.{owner} = 1;'),
            'wrong_signal': final.replace('decode(bytes, signal)', 'decode(bytes, undefined)'),
            'lost_value': final.replace("status: 'loading', value: this.state.value", "status: 'loading', value: null"),
            'global_owner': global_fault,
            'skip_stale_decode': final.replace('      const value = await decode',
                f'      if (this.{owner} !== request) return undefined;\n      const value = await decode'),
        }
        if in_place_probe:
            guarded_success = (guard + " {\n        this.state = { status: 'ready', value, error: null };\n      }")
            assert final.count(guarded_success) == 1
            variants = {
                'final': final,
                'stale_success_in_place': final.replace(guarded_success,
                    "Object.assign(this.state, { status: 'ready', value, error: null });"),
            }
        if adoption:
            assert skill and not in_place_probe
            ready = "this.state = { status: 'ready', value, error: null };"
            error = "this.state = { status: 'error', value: this.state.value, error };"
            ready_mutation = "Object.assign(this.state, { status: 'ready', value, error: null });"
            error_mutation = "Object.assign(this.state, { status: 'error', value: this.state.value, error });"
            variants['valid_mutable_updates'] = final.replace(ready, ready_mutation).replace(error, error_mutation)
            variants['stale_success_in_place'] = success_fault.replace(ready, ready_mutation)
            variants['stale_error_in_place'] = error_fault.replace(error, error_mutation)
        assert all(source != final for variant, source in variants.items() if variant != 'final')
        for variant, implementation in variants.items():
            with tempfile.TemporaryDirectory(prefix='author-replay-', dir=run) as folder:
                scratch = Path(folder) / 'project'
                shutil.copytree(project, scratch)
                (scratch / 'preview.mjs').write_text(implementation)
                command = ['node', '--test', '--test-reporter=tap']
                should_pass = variant in ('final', 'valid_mutable_updates')
                deadline = 90 if adoption else 15
                try:
                    result = subprocess.run(command, cwd=scratch, capture_output=True, text=True, timeout=deadline)
                    code, output, timed_out = result.returncode, result.stdout + result.stderr, False
                except subprocess.TimeoutExpired as error:
                    def decoded(value):
                        return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
                    code, output, timed_out = None, decoded(error.stdout) + decoded(error.stderr), True
                unchanged = all((scratch / path).read_bytes() == (project / path).read_bytes()
                                for path in before if path != 'preview.mjs')
                counts = {key: int(value) for key, value in re.findall(r'^# (tests|pass|fail|cancelled|skipped) (\d+)$', output, re.M)}
                matched = (not timed_out and unchanged and counts.get('tests') == test_count
                           and counts.get('cancelled') == counts.get('skipped') == 0
                           and code == int(not should_pass)
                           and (counts.get('pass') == test_count if should_pass else counts.get('fail', 0) > 0))
                report['checks'].append({'cell': name, 'variant': variant, 'command': command,
                    'exit_code': code, 'timed_out': timed_out, 'process_deadline_seconds': deadline, 'counts': counts,
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
    parser.add_argument('--in-place-probe', action='store_true',
                        help='Separate post-review success-state mutation probe; never rewrite initial replay')
    parser.add_argument('--profile', choices=('preview-01', 'state-contents-01'), default='preview-01')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite an earlier author attempt')
    report = replay(args.run.resolve(), args.in_place_probe, args.profile)
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps({'cells': len(report['cells']), 'checks': len(report['checks']), 'all_matched': report['all_matched']}))
