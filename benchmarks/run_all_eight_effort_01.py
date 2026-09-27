"""Same-resource eight-role effort comparison using the existing scheduler."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    '_eight_effort_scheduler', ROOT / 'benchmarks/run_all_eight_apps_01.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
EFFORTS = {'medium': 'medium', 'low': 'low'}
runner.MODELS = {condition: 'gpt-6-astra' for condition in EFFORTS}
runner.FLAGS = {condition: ['--disable', 'apps', '-c',
    'features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]']
    for condition in EFFORTS}
runner.base.CONDITIONS = tuple(EFFORTS)
runner.base.RESOURCES = {condition: '7172b50c' for condition in EFFORTS}
runner.base.SCHEDULE = [(index, condition) for index in range(8)
    for condition in (runner.base.CONDITIONS if index % 2 == 0
                      else runner.base.CONDITIONS[::-1])]
original_identities, original_frozen = runner.identities, runner.frozen


def identities():
    result = original_identities()
    for name in ('benchmarks/run_all_eight_effort_01.py',
                 'benchmarks/ALL-EIGHT-EFFORT-01-PROTOCOL.md',
                 'tests/test_all_eight_effort_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'condition_efforts': dict(EFFORTS)}


runner.base.identities, runner.base.frozen = identities, frozen


def execute(output, manifest):
    def unchanged():
        return all(manifest.get(key) == value for key, value in frozen(output).items())
    if (not unchanged() or manifest['completed_cells']
            or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump({'revision': runner.base.git('rev-parse', 'HEAD').decode().strip(),
                   'started_at': datetime.now(timezone.utc).isoformat()}, stream)
    disabled = runner.base.run.disabled_skills()
    for index, condition in runner.base.SCHEDULE:
        if not unchanged():
            raise ValueError('Frozen inputs changed between cells; do not restart')
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        with patch.object(runner.base.run.subprocess, 'Popen', new=runner.process_wrapper(
                runner.base.run.subprocess.Popen, runner.FLAGS[condition])):
            result = runner.base.run.run_cell(case, 'skill', 1, output / condition,
                runner.MODELS[condition], EFFORTS[condition],
                runner.base.SETTINGS['timeout_seconds'], disabled,
                skills_root=output / condition / 'skills',
                workspace_root=output / 'workspaces' / condition, persist_session=True)
        manifest['completed_cells'].append({'case_id': case['id'], 'condition': condition,
            **{key: result[key] for key in ('completed', 'timed_out', 'limit_detected',
                                           'usage', 'elapsed_seconds')}})
        manifest['stopped_after_limit'] = bool(result['limit_detected'])
        manifest['stopped_after_uncompleted'] = not result['completed']
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected'] or not result['completed']:
            break
    manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
    (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')


runner.execute, runner.frozen, runner.EFFORTS = execute, frozen, EFFORTS


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        execute(output, json.loads((output / 'run.json').read_text()))
    else:
        runner.base.prepare(output)
        print('Sixteen effort cells prepared; zero model calls.')
