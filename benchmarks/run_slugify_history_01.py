"""Freeze one real-history review and run baseline/current exactly once each."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import run
from preflight_slugify_native_01 import load_source, REVISION, ROOT
from run_hostage_buffer_01 import git

CONDITIONS = ('baseline', 'current')
RESOURCE = '92afe96'
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1)


def case():
    return dict(id='slugify-replacement-history', skill='necromancer', task='''Review the two user-specific replacement passes in slugify/slugify.py:slugify.
A proposed behavior-preserving cleanup would remove one apparently duplicate pass.
Evaluate removing the early pass only and removing the late pass only, independently;
leave every other operation, argument and caller unchanged. Do not implement a fix.

Observe actual slugify() results for current code and both independent removals,
using these three inputs for every variant (nine observations total):
1. text='10 | 20 %', replacements=[['|', 'or'], ['%', 'percent']].
2. text='FOO', replacements=[['foo', 'bar']].
3. text='Plain Text', default arguments.
Retain each actual return value or exception. Explain what the observations and
intervening operations establish about compatibility; preserving behavior here
means preserving current results, not assuming every result is a documented promise.

Separately establish the introduction of each pass from local ancestor history:
inspect the relevant parent/child implementation and accompanying tests/docs when
present, cite the introducing commits, and distinguish observed current effects
from documented historical rationale. Do not invent intent absent from the evidence.
Use only ancestors of pinned HEAD, not other branches, issues or remote services.
Recommend separately whether each deletion is behavior-preserving and identify
the behavior to preserve. No requirement to preserve the exact implementation.

Use <PYTHON> with -B (text-unidecode is already installed). Ensure behavioral
observations use this project's implementation, not an installed slugify package.
In-memory changes or project-local disposable copies are allowed; tool choice is yours.
Preserve every original file byte/mode, HEAD, and installed skill resource. Remove
all owned scratch before finishing; no lasting report, harness or production/test edit.
No network, dependency installation, fetching, commits or publication. The specified
interpreter/dependencies may be read/executed but not modified.'''.replace('<PYTHON>', sys.executable),
        criteria=[
            'All nine actual outputs/errors observed against this project and independent specified removals.',
            'Separate compatibility decisions correctly explained through intervening operations and current results.',
            'Both introducing ancestor commits established by relevant parent/child implementation evidence.',
            'Relevant accompanying tests/docs inspected; current behavior distinguished from historical rationale without invented intent.',
            'Original bytes/modes, HEAD and installed resources preserved; owned scratch removed and no out-of-scope changes.'])


def source_identity(source):
    load_source(source)
    def sg(*args):
        return subprocess.check_output(['git', '-C', str(source), *args], text=True, timeout=20).strip()
    if sg('status', '--porcelain=v1') or sg('rev-parse', '--is-shallow-repository') != 'false':
        raise ValueError('Requires a clean full-history checkout')
    return dict(revision=REVISION, tree=sg('rev-parse', 'HEAD^{tree}'),
                ancestors_sha256=hashlib.sha256(sg('rev-list', 'HEAD').encode()).hexdigest())


def identities():
    names = ('benchmarks/run_slugify_history_01.py', 'benchmarks/preflight_slugify_native_01.py',
             'benchmarks/run.py', 'benchmarks/SLUGIFY-HISTORY-01-PROTOCOL.md',
             'tests/test_slugify_history_runner.py')
    return {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in names}


def frozen(source, output):
    return dict(identities=identities(), source_identity=source_identity(source), case=case(),
        schedule=list(CONDITIONS), settings=SETTINGS, python_version=sys.version,
        resource_digests={c: run.resource_digest(output / c / 'skills') for c in CONDITIONS})


def execute(source, output, manifest):
    if any(manifest.get(k) != v for k, v in frozen(source, output).items()) or manifest['completed_cells'] or manifest['stopped_after_limit']:
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
            revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for condition in CONDITIONS:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(case(), 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', project_source=source, persist_session=True)
        manifest['completed_cells'].append(dict(condition=condition,
            **{k: result[k] for k in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        manifest['stopped_after_limit'] = bool(result['limit_detected'])
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected']:
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    source, output = args.source.resolve(), args.output.resolve()
    if args.execute:
        execute(source, output, json.loads((output / 'run.json').read_text()))
        return
    source_identity(source)
    output.mkdir(parents=True, exist_ok=False)
    for condition in CONDITIONS:
        (output / condition / 'skills').mkdir(parents=True)
    for entry in git('ls-tree', '-r', RESOURCE, '--', 'skills/necromancer').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported resource')
        path = output / 'current' / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))
    manifest = dict(frozen(source, output), resource_revision=git('rev-parse', RESOURCE).decode().strip(),
        completed_cells=[], stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for directory in (output, *(output / c for c in CONDITIONS)):
        (directory / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared one full-history request / two sessions; no model calls.')


if __name__ == '__main__':
    main()
