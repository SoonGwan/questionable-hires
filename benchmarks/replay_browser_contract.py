#!/usr/bin/env python3
"""Author replay of retained browser checks; no model sessions or credentials."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import uuid


IMAGE = 'questionable-hires/browser-codex:0.153.4-pw1.63.0'
CHROMIUM = '/ms-playwright/chromium-1243/chrome-linux-arm64/chrome'


def fingerprints(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def variant(source, success, failure):
    additions = [('const requests = [];', 'const requests = [];\nlet generation = 0;'),
                 ('  const query = input.value;',
                  '  const query = input.value;\n  const requestGeneration = ++generation;')]
    if success:
        additions.append(('    results.textContent = records.join',
                          '    if (requestGeneration !== generation) return;\n    results.textContent = records.join'))
    if failure:
        additions.append(('    error.textContent = failure.message;',
                          '    if (requestGeneration !== generation) return;\n    error.textContent = failure.message;'))
    for old, new in additions:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    return source


def replay(project, scratch_parent, context):
    before = fingerprints(project)
    source = (project / 'index.html').read_text()
    fixture = Path(__file__).parent / 'browser/model-project/index.html'
    assert source == fixture.read_text(), 'Retained production differs from supplied fixture'
    image_id = subprocess.check_output(['docker', '--context', context, 'image', 'inspect',
                                       IMAGE, '--format', '{{.Id}}'], text=True).strip()
    report = {'kind': 'author browser replay, not model timing', 'image': IMAGE,
              'image_id': image_id, 'source_sha256': before['index.html'],
              'harness_sha256': before['qa/catalog.mjs'], 'variants': []}
    variants = [('original', source), ('guarded', variant(source, True, True)),
                ('success-only-guard', variant(source, True, False)),
                ('failure-only-guard', variant(source, False, True))]
    for name, contents in variants:
        with tempfile.TemporaryDirectory(prefix='browser-contract-', dir=scratch_parent) as temporary:
            scratch = Path(temporary) / 'project'
            shutil.copytree(project, scratch)
            (scratch / 'index.html').write_text(contents)
            evidence_path = scratch / 'qa/catalog-evidence.json'
            # A retained old evidence file must not masquerade as this execution.
            if evidence_path.exists():
                evidence_path.unlink()
            container_name = 'qh-browser-replay-' + uuid.uuid4().hex
            command = ['docker', '--context', context, 'run', '--rm', '--init',
                       '--name', container_name, '--network', 'none', '--ipc=host',
                       '-v', f'{scratch}:/work:rw', '-w', '/work',
                       '-e', f'PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH={CHROMIUM}',
                       IMAGE, 'timeout', '45s', 'node', 'qa/catalog.mjs']
            try:
                result = subprocess.run(command, capture_output=True, text=True, timeout=60)
            finally:
                # Only this invocation's uniquely named container is targeted.
                subprocess.run(['docker', '--context', context, 'rm', '-f', container_name],
                               capture_output=True, text=True, timeout=10)
                remaining = subprocess.check_output(
                    ['docker', '--context', context, 'ps', '-a', '--filter',
                     f'name=^/{container_name}$', '--format', '{{.Names}}'],
                    text=True, timeout=10).strip()
                if remaining:
                    raise RuntimeError('Owned replay container removal unconfirmed: ' + container_name)
            assert hashlib.sha256((scratch / 'qa/catalog.mjs').read_bytes()).hexdigest() == before['qa/catalog.mjs']
            assert evidence_path.is_file(), result.stdout + result.stderr
            evidence = json.loads(evidence_path.read_text())
            assert result.returncode in (0, 1), result.stdout + result.stderr
            assert len(evidence['cases']) == 4
            assert all(case['observations'] and case['cleanup'] for case in evidence['cases'])
            assert all(case['outcome'] in ('PASS', 'FAIL') for case in evidence['cases'])
            assert evidence['cleanup'] == {'contexts': 'closed', 'browser': 'closed'}
            report['variants'].append({'variant': name, 'exit_code': result.returncode,
                                       'evidence': evidence, 'stdout': result.stdout,
                                       'stderr': result.stderr})
    assert fingerprints(project) == before, 'Retained artifacts changed'
    report['retained_project_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--scratch-parent', type=Path, required=True)
    parser.add_argument('--context', default='colima')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = replay(args.project.resolve(), args.scratch_parent.resolve(), args.context)
    with args.output.open('x') as output:
        json.dump(report, output, indent=2)
        output.write('\n')
    print(json.dumps([{'variant': row['variant'], 'exit_code': row['exit_code'],
                       'cases': [case['outcome'] for case in row['evidence']['cases']],
                       'cleanup': row['evidence']['cleanup']} for row in report['variants']], indent=2))
