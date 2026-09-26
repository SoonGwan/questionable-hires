"""Frozen same-resource eight-role apps-availability comparison; reuse existing preparation."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_eight_apps_base_01', ROOT / 'benchmarks/run_all_eight_current_04.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
MODELS = {'default': 'gpt-6-astra', 'apps_off': 'gpt-6-astra'}
FLAGS = {'default': [], 'apps_off': ['--disable', 'apps']}
from unittest.mock import patch
from run_tool_surface_01 import process_wrapper
base.CONDITIONS = tuple(MODELS)
base.RESOURCES = {condition: '6701069f' for condition in MODELS}
base.SCHEDULE = [(index, condition) for index in range(8)
                 for condition in (base.CONDITIONS if index % 2 == 0 else base.CONDITIONS[::-1])]
base.SETTINGS = dict(effort='medium', timeout_seconds=360, jobs=1, repeats=1)
original_identities, original_frozen = base.identities, base.frozen


def identities():
    result = original_identities()
    for name in ('benchmarks/run_all_eight_apps_01.py', 'benchmarks/ALL-EIGHT-APPS-01-PROTOCOL.md',
                 'tests/test_all_eight_apps_01.py', 'benchmarks/run_tool_surface_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    result = original_frozen(output)
    result['condition_models'] = dict(MODELS)
    result['condition_flags'] = {k: list(v) for k, v in FLAGS.items()}
    result['cli_version'] = base.subprocess.check_output(['codex', '--version'], text=True).strip()
    return result


base.identities, base.frozen = identities, frozen


def execute(output, manifest):
    if (any(manifest.get(key) != value for key, value in frozen(output).items())
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(revision=base.git('rev-parse', 'HEAD').decode().strip(),
                       started_at=datetime.now(timezone.utc).isoformat()), stream)
    disabled = base.run.disabled_skills()
    for index, condition in base.SCHEDULE:
        if any(manifest.get(key) != value for key, value in frozen(output).items()):
            raise ValueError('Frozen inputs changed between cells; do not restart')
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        with patch.object(base.run.subprocess, 'Popen', new=process_wrapper(base.run.subprocess.Popen, FLAGS[condition])):
            result = base.run.run_cell(case, 'skill', 1, output / condition,
                MODELS[condition], base.SETTINGS['effort'], base.SETTINGS['timeout_seconds'], disabled,
                skills_root=output / condition / 'skills', workspace_root=output / 'workspaces' / condition,
                persist_session=True)
        manifest['completed_cells'].append(dict(case_id=case['id'], condition=condition,
            **{key: result[key] for key in ('completed', 'timed_out', 'limit_detected', 'usage', 'elapsed_seconds')}))
        manifest['stopped_after_limit'] = bool(result['limit_detected'])
        manifest['stopped_after_uncompleted'] = not result['completed']
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected'] or not result['completed']:
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output / 'run.json').read_text()))
    else:
        base.prepare(output)
        print('Prepared16 same-resource apps cells; exposed development controls, no model calls.')
