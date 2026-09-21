"""Freeze one real-history review and run prior/baseline/current exactly once each."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import run
from preflight_urllib3_history_01 import load_source, REVISION, ROOT
from run_hostage_buffer_01 import git

CONDITIONS = ('prior', 'baseline', 'current')
RESOURCES = {'prior': '92afe96', 'current': 'f53cb65'}
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1)


def case():
    return dict(id='urllib3-retry-history', skill='necromancer', task='''Review two proposed behavior-preserving cleanups in src/urllib3/util/retry.py:Retry.is_retry.
A: move the method-allowlist rejection below the status_forcelist early return.
B: remove only self.total from the Retry-After fallback condition.
Evaluate independently, not combined, and leave every other operation unchanged.
This is a review, not authorization to fix production code.

Observe actual Retry.is_retry results for current, A-only and B-only using these
five configurations/calls (15 observations total). In every case allowed_methods=['GET'];
unspecified constructor/call arguments use defaults:
1. total=3, status_forcelist=[500]; is_retry('POST', 500).
2. total=0, no forced statuses; is_retry('GET', 429, True).
3. total=3, status_forcelist=[500]; is_retry('GET', 500).
4. total=3, no forced statuses; is_retry('GET', 429, True).
5. total=0, status_forcelist=[500]; is_retry('GET', 500).
Retain every actual value or exception. Explain separate compatibility decisions
and the relevant existing test/doc contract. Inspect the current connection-pool
caller and explain whether these predicate results alone establish an actual
network retry, including case5. No HTTP requests or full integration run is needed.

Use local ancestor history to establish when the Retry-After fallback was added:
inspect the relevant parent/child implementation and accompanying tests/docs.
Also inspect the change attributing the method check to _is_method_retryable and
an earlier operational implementation. Distinguish helper extraction/renaming from
introduction of the method restriction; first-ever origin is not required.
Cite the relevant commits. Separate observed current behavior from historical
rationale; do not invent author intent. Use only ancestors of pinned HEAD.

Use <PYTHON> with -B and this checkout's src directory on the import path.
Verify the imported implementation is local, not an installed urllib3 package.
In-memory variants or project-local disposable copies are allowed; no tool is
required. Preserve every original file byte/mode, HEAD and installed resource.
Remove all owned scratch before finishing; no lasting harness, report or code edit.
No network/HTTP requests, installations, fetching, commits or publication.
The specified interpreter/dependencies may be read/executed, not modified.'''.replace('<PYTHON>', sys.executable),
        criteria=[
            'All15 actual outputs/errors observed with local binding and independent specified changes.',
            'Separate compatibility decisions correctly explain the observations and existing test/doc contract.',
            'Current connection-pool caller inspected; predicate results distinguished from actual network retry, including zero-budget forced status.',
            'Retry-After fallback introduction and method-helper extraction established with relevant ancestor parent/child evidence, without invented origin or intent.',
            'Original bytes/modes, HEAD and installed resources preserved; scratch removed; no out-of-scope actions.'])


def source_identity(source):
    load_source(source)
    def sg(*args):
        return subprocess.check_output(['git', '-C', str(source), *args], text=True, timeout=20).strip()
    if sg('status', '--porcelain=v1') or sg('rev-parse', '--is-shallow-repository') != 'false':
        raise ValueError('Requires a clean full-history checkout')
    return dict(revision=REVISION, tree=sg('rev-parse', 'HEAD^{tree}'),
                ancestors_sha256=hashlib.sha256(sg('rev-list', 'HEAD').encode()).hexdigest())


def identities():
    names = ('benchmarks/run_urllib3_history_01.py', 'benchmarks/preflight_slugify_native_01.py',
             'benchmarks/run.py', 'benchmarks/URLLIB3-HISTORY-01-PROTOCOL.md',
             'tests/test_urllib3_history_runner.py')
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
    for condition, revision in RESOURCES.items():
        for entry in git('ls-tree', '-r', revision, '--', 'skills/necromancer').decode().splitlines():
            info, name = entry.split('\t', 1)
            mode, kind, oid = info.split()
            if kind != 'blob' or mode not in ('100644', '100755'):
                raise ValueError('Unsupported resource')
            path = output / condition / name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream:
                stream.write(git('cat-file', 'blob', oid))
            path.chmod(int(mode[-3:], 8))
    manifest = dict(frozen(source, output), resource_revisions={c: git('rev-parse', rev).decode().strip() for c, rev in RESOURCES.items()},
        completed_cells=[], stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for directory in (output, *(output / c for c in CONDITIONS)):
        (directory / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared one full-history request / three sessions; no model calls.')


if __name__ == '__main__':
    main()
