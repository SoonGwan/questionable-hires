"""Frozen real-source Landlord transfer; prior/current/no-skill original sessions."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

import run
from preflight_click_defaults import observe
from preflight_click_context import REVISION
from run_click_context_01 import environment
from run_httpx import freeze_skill

ROOT = Path(__file__).resolve().parents[1]
RESOURCES = {'prior': '4416263', 'current': '1ae3ee0'}
SCHEDULE = ['current', 'baseline', 'prior']
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360)
TASK = '''Review a proposed simplification in src/click/core.py: in
Parameter.get_default, replace `if value is None and not ctx._default_map_has(self.name):`
with `if value is None:`; in Parameter.consume_value, replace
`if default_map_value is not None or ctx._default_map_has(self.name):`
with `if default_map_value is not None:`. Everything else stays unchanged.
Would this preserve default resolution? Recommend keep, simplify or remove with
actual caller/policy reasoning, source references and a viable alternative.
Trace one concrete future maintenance change, not just a line-count comparison.

Run the relevant existing tests in tests/test_defaults.py and observe actual
CliRunner resolution for a string --name option with default='fallback' and an
explicit environment variable. Include: CLI value with environment and map also
present; environment with map present; map values None, empty string, zero;
missing map entry; stored click._utils.UNSET; and a map factory returning None.
Record values and parameter sources, and the factory's invocation count. Explain
how those observations bear on the proposal. Preserve normal controls. You may
analyze the proposed change statically after observing current behavior; applying
it in a disposable copy is optional, not required. Distinguish execution from
inference, and confirm native observations import this checkout's Click.

Review only: originals, file modes, Git HEAD/index and installed skill resources
must remain unchanged. Work only within the project. Remove any owned local
scratch on completion or failure; no permanent tests/report. No dependencies,
network, production fix, commits, resets or publication. Source is shallow; no
history-origin claim is requested. Use the supplied interpreter with -B. For
pytest use PYTHONPATH=src, PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 and -p no:cacheprovider,
retaining other project settings. CliRunner's in-process environment isolation
is permitted; do not change external settings.'''
CRITERIA = [
    'Traces lookup/default/consume caller semantics and recommends a contract-preserving design, not merely fewer lines.',
    'Runs relevant native existing tests and all eight requested actual CliRunner scenarios, recording values/sources and factory count with normal controls.',
    'Explains explicit None versus missing/UNSET, false values and callable resolution using supported observations and proposal analysis, not simulated code.',
    'Provides source-grounded viable alternative and concrete maintenance tradeoff; distinguishes original execution from unexecuted proposal effects.',
    'Native observations use actual checkout Click; originals/modes/Git/resources preserved, owned scratch removed, no unauthorized action.',
]


def case(python):
    return dict(id='click-default-resolution-design', skill='landlord', criteria=list(CRITERIA),
                task=TASK + '\nPreinstalled Python: ' + str(python))


def identities():
    names = ['run_click_defaults_01.py', 'preflight_click_defaults.py',
             'preflight_click_context.py', 'run_click_context_01.py', 'run.py',
             'run_httpx.py', 'CLICK-DEFAULTS-01-PROTOCOL.md']
    return {n: hashlib.sha256((ROOT / 'benchmarks' / n).read_bytes()).hexdigest() for n in names}


def digests(output):
    return {c: run.resource_digest(output / c / 'skills') for c in SCHEDULE}


def execute(manifest, source, output, python):
    if (manifest['identities'] != identities() or manifest['case'] != case(python)
            or manifest['schedule'] != SCHEDULE or manifest['settings'] != SETTINGS
            or manifest['source_digest'] != run.resource_digest(source)
            or manifest['resource_digests'] != digests(output)
            or manifest['environment'] != environment(python)
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs/settings changed or already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump({'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = run.disabled_skills()
    for condition in SCHEDULE:
        print('Starting ' + condition, flush=True)
        result = run.run_cell(manifest['case'], 'baseline' if condition == 'baseline' else 'skill',
            1, output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills', project_source=source,
            persist_session=True)
        manifest['completed_cells'].append(dict(condition=condition, **{k: result[k] for k in
            ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        if result['limit_detected']: manifest['stopped_after_limit'] = True
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected']: break
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
    (output / 'baseline/skills').mkdir(parents=True)
    for condition, revision in RESOURCES.items():
        freeze_skill(ROOT, revision, output / condition / 'skills/landlord', skill_name='landlord')
    manifest = dict(upstream_revision=REVISION, resource_revisions=RESOURCES, case=case(python),
        schedule=SCHEDULE, identities=identities(), source_digest=run.resource_digest(source),
        resource_digests=digests(output), environment=environment(python), interpreter=str(python),
        native_preflight=controls, settings=SETTINGS, repeats=1, jobs=1, completed_cells=[],
        stopped_after_limit=False, prepared_at=datetime.now(timezone.utc).isoformat())
    for destination in [output, *(output / c for c in SCHEDULE)]:
        (destination / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared three original sessions; native positive/negative controls verified; no model calls.')


if __name__ == '__main__':
    main()
