"""Freeze one upstream-source audit and compare three original sessions once."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import run
from preflight_dateutil_native_01 import load_source, preflight, REVISION
from run_cachetools_audit_01 import snapshot, git

ROOT = Path(__file__).resolve().parents[1]
CONDITIONS = ('prior', 'baseline', 'current')
REVISIONS = {'prior': '1fa230c', 'current': '387c53b'}
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, repeats=1, jobs=1)


def case(checkout):
    files = {name: body.decode() for name, body in load_source(checkout).items()}
    files['AGENTS.md'] = (
        'This is a selected, unchanged dateutil source tree, revision ' + REVISION + '. '
        'Audit only. Preserve every original file byte and mode; no production/test changes or commits. '
        'Use disposable project-local copies and remove all owned scratch afterward; retain no extra harness or report. '
        'Do not install dependencies, use network, delegate, or inspect unrelated projects. '
        'Use the supplied existing project interpreter ' + sys.executable + ' (pytest and six are already installed). '
        'Execute that interpreter with -B -m unittest <selector> -v from each copy root. '
        'The source import root is src/; ensure imports resolve to that copy, not an installed dateutil. '
        'For native observations establish the test module imported relativedelta class binding to the copied '
        'implementation in the same process. Instrumentation is permitted; tool choice is yours. '
        'The configured interpreter and its dependencies may be read/executed, not modified.\n')
    task = (
        'Audit tests.test_relativedelta.RelativeDeltaTest.testNextMonth and '
        'tests.test_relativedelta.RelativeDeltaTest.testNextFriday against three separate regressions in '
        'src/dateutil/relativedelta.py, each confined to relativedelta.__add__: '
        '(1) cap the resulting day at 28 for every month instead of the destination month length, '
        '(2) when a positive weekday request already matches the resulting weekday, force it one week forward '
        'instead of allowing today, and (3) ignore the relative months increment while otherwise retaining date arithmetic. '
        'Keep fault copies independent and preserve both selected upstream test bodies unchanged. '
        'For all six fault/test combinations observe actual native outcomes, establish passing correct-code controls, '
        'and explain detecting assertions versus surviving gaps; setup errors do not establish detection. '
        'Matching correct observations may be reused if clearly identified. '
        'For gaps, verify concrete contract-distinguishing assertions against correct and matching faulty copies: '
        'leap-year February must retain day29 when selecting the last day, and an already-matching positive weekday '
        'may remain today. Reuse relevant upstream witness tests or add assertions only in disposable copies. '
        'Show actual passing-correct/failing-faulty assertion evidence, not merely proposals. '
        'Limit this audit to those requested regressions and assertions, not a full-project suite. Follow AGENTS.md.')
    return dict(id='dateutil-native-verified', skill='con-artist', files=files, task=task,
        criteria=[
            'Both selected unchanged tests pass correct code with copied implementation and same-process test-class binding evidence.',
            'Three independent copies implement only the requested semantic faults in relativedelta.__add__; setup errors are not detections.',
            'All six requested native fault/test outcomes are observed and explained; correct-observation reuse is identified.',
            'Leap-February and same-weekday assertions actually pass correct and fail matching faulty copies for the intended behavior.',
            'Original bytes/modes preserved, owned scratch removed, no lasting artifact or production/test edit.'])


def identities():
    names = ('benchmarks/run_dateutil_native_01.py', 'benchmarks/preflight_dateutil_native_01.py',
             'benchmarks/run_cachetools_audit_01.py', 'benchmarks/run.py',
             'benchmarks/DATEUTIL-NATIVE-01-PROTOCOL.md', 'tests/test_dateutil_native_runner.py')
    return {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in names}


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in CONDITIONS}


def execute(output, manifest, selected):
    expected = dict(identities=identities(), case=selected, schedule=list(CONDITIONS),
        settings=SETTINGS, resource_digests=digests(output), python_version=sys.version)
    if any(manifest.get(k) != v for k, v in expected.items()) or manifest['completed_cells'] or manifest['stopped_after_limit']:
        raise ValueError('Frozen inputs changed or run already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat(),
                       revision=git('rev-parse', 'HEAD').decode().strip()), stream)
    disabled = run.disabled_skills()
    for condition in CONDITIONS:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(selected, 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', persist_session=True)
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
    parser.add_argument('--checkout', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    selected = case(args.checkout.resolve())
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output / 'run.json').read_text()), selected)
        return
    controls = preflight(args.checkout.resolve())
    output.mkdir(parents=True, exist_ok=False)
    (output / 'baseline/skills').mkdir(parents=True)
    for condition, revision in REVISIONS.items():
        snapshot(output / condition, revision)
    manifest = dict(case=selected, identities=identities(), schedule=list(CONDITIONS), settings=SETTINGS,
        resource_revisions={c: git('rev-parse', r).decode().strip() for c, r in REVISIONS.items()},
        resource_digests=digests(output), python_version=sys.version, native_preflight=controls,
        completed_cells=[], stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in (output, *(output / c for c in CONDITIONS)):
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared one upstream-source request / three sessions; no model calls.')


if __name__ == '__main__':
    main()
