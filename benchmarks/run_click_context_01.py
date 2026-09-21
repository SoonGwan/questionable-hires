"""Prepare and run one frozen Click audit pair, retaining original sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import run
from preflight_click_context import REVISION, observe
from run_httpx import freeze_skill

ROOT = Path(__file__).resolve().parents[1]
RESOURCE = 'f253f38'
SCHEDULE = ['baseline', 'skill']
TASK = '''Audit whether tests/test_context.py protects Context resource unwinding
when two nested resources both decline to suppress an exception from the body.
Establish whether the original exception propagates and whether both resources
actually exit in reverse registration order. Include single-resource propagation
and nested-resource suppression as neighboring controls.
Demonstrate existing test sensitivity with a narrow isolated behavioral mutation
in actual src/click/core.py. Execute the unchanged relevant existing tests against
correct and faulty copies. If coverage is missing, verify the same focused added
assertions against both variants; if adequate, identify the detecting assertions
without demanding redundant tests. Explain the actual exercised path, not just
the presence of pytest.raises or a green exit. Report native test identities,
counts, assertions and exits; confirm the native test process imports the actual
copy-local Click implementation. A rewritten simulation or setup failure is not
mutation detection. Do not assume other unsupported input behavior.
Keep originals, Git HEAD/index, file modes and installed skill resources unchanged.
All disposable copies, tests and diagnostics must be project-local and removed
at completion, including failure paths; leave no harness or report. No production
fix, dependency installation, network, commit, stash, reset or publication.
Use the supplied Python interpreter with bytecode disabled. For pytest use
PYTHONPATH=src and PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 from each copy root, with
-p no:cacheprovider. Preserve the project's other pytest settings. Source is a
shallow checkout; this task does not require history-origin claims.'''
CRITERIA = [
    'Actual copy-local implementation is used by native tests in correct/faulty variants; mutation targets the requested behavior, not setup or test edits.',
    'Unchanged existing tests run in both variants and sensitivity claims identify the actual executed cleanup path and native results.',
    'If needed, identical focused added assertions pass correct and reject faulty behavior with actual exception propagation and reverse-order exits; no setup failure substitutes.',
    'Single-resource propagation and nested suppression controls execute with correct observations; diagnosis remains scoped to demonstrated coverage.',
    'Original files/modes, Git HEAD/index and skill resources preserved; owned scratch removed and no out-of-scope operations.'
]


def identities():
    names = ['run_click_context_01.py', 'preflight_click_context.py', 'run.py',
             'run_httpx.py', 'CLICK-CONTEXT-01-PROTOCOL.md']
    return {name: hashlib.sha256((ROOT / 'benchmarks' / name).read_bytes()).hexdigest() for name in names}


def environment(python):
    return {key: subprocess.check_output([str(python), *args], text=True).strip()
            for key, args in [('version', ['--version']), ('dependencies', ['-m', 'pip', 'freeze'])]}


def case(python):
    return dict(id='nested-resource-audit', skill='con-artist', criteria=CRITERIA,
                task=TASK + '\nPreinstalled Python: ' + str(python))


def validate(manifest, source, output, python):
    if (manifest['identities'] != identities() or manifest['case'] != case(python)
            or manifest['schedule'] != SCHEDULE
            or manifest['source_digest'] != run.resource_digest(source)
            or manifest['resource_digest'] != run.resource_digest(output / 'skills')
            or manifest['environment'] != environment(python)):
        raise ValueError('Frozen inputs, source, resources or environment changed')


def execute(manifest, source, output, python):
    validate(manifest, source, output, python)
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat()), stream)
    disabled = run.disabled_skills()
    for arm in SCHEDULE:
        print('Starting ' + arm, flush=True)
        result = run.run_cell(manifest['case'], arm, 1, output,
                              'gpt-6-astra', 'medium', 360, disabled,
                              skills_root=output / 'skills', project_source=source,
                              persist_session=True)
        manifest['completed_cells'].append(dict(arm=arm, **{key: result[key] for key in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        if result['limit_detected']:
            manifest['stopped_after_limit'] = True
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
    python = Path(sys.executable).absolute()
    if args.execute:
        execute(json.loads((output / 'run.json').read_text()), source, output, python)
        return
    controls = observe(source)
    output.mkdir(parents=True, exist_ok=False)
    freeze_skill(ROOT, RESOURCE, output / 'skills/con-artist')
    manifest = dict(upstream_revision=REVISION, resource_revision=RESOURCE,
                    case=case(python), schedule=SCHEDULE, identities=identities(),
                    source_digest=run.resource_digest(source), resource_digest=run.resource_digest(output / 'skills'),
                    interpreter=str(python), environment=environment(python), native_preflight=controls,
                    model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1,
                    completed_cells=[], stopped_after_limit=False,
                    prepared_at=datetime.now(timezone.utc).isoformat())
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared two cells; native controls passed; no model calls.')


if __name__ == '__main__':
    main()
