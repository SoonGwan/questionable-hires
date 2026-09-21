"""Four frozen real-source audit cells; no retries, replacements or resumption."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import run
import packaging_specifier_cases as fixture

ROOT = fixture.ROOT
RESOURCE = 'c8fd471'
CONDITIONS = ('baseline', 'current')
SCHEDULE = [(0, 'baseline'), (0, 'current'), (1, 'current'), (1, 'baseline')]
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout_seconds=360, jobs=1, repeats=1)
EVIDENCE = ROOT / 'benchmarks/results/packaging-specifier-01-preflight'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], timeout=20)


def environment():
    return dict(python=sys.executable, version=sys.version,
                dependencies=subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'],
                                                     text=True, timeout=20).splitlines())


def validate_preflight():
    expected = json.loads((EVIDENCE / 'capture.json').read_text())
    summary = json.loads((EVIDENCE / 'summary.json').read_text())
    actual = environment()
    if actual['version'] != summary['python'] or actual['dependencies'] != expected['dependencies']:
        raise ValueError('Use the recorded preflight runtime/dependencies')
    for name, count in [('single', 1), ('multiple', 3)]:
        report = json.loads((EVIDENCE / (name + '.json')).read_text())
        if report['status'] != 'observed' or len(report['audits']) != count:
            raise ValueError('Incomplete native author controls')
        for index, audit in enumerate(report['audits']):
            checks = audit['checks']
            if audit['status'] != 'observed' or set(checks) != {'correct_tests', 'mutant_tests'}:
                raise ValueError('Unexpected native phases')
            for phase, code in [('correct_tests', 0), ('mutant_tests', 1)]:
                check = checks[phase]
                if check['exit_code'] != code or check['timed_out'] or check.get('output_truncated'):
                    raise ValueError('Unusable native control')
                if 'observation_ref' not in check:
                    if (phase == 'correct_tests' and '806 passed' not in check['output']) or (phase == 'mutant_tests' and 'AssertionError' not in check['output']):
                        raise ValueError('Missing native assertion/count evidence')
    return expected


def identities():
    paths = ['benchmarks/run_packaging_specifier_01.py', 'benchmarks/packaging_specifier_cases.py',
             'benchmarks/packaging-specifier-01-source.json', 'benchmarks/run.py',
             'benchmarks/PACKAGING-SPECIFIER-01-SELECTION.md', 'benchmarks/PACKAGING-SPECIFIER-01-PROTOCOL.md',
             'tests/test_packaging_specifier_cases.py', 'tests/test_packaging_specifier_runner.py']
    paths += [p.relative_to(ROOT).as_posix() for p in EVIDENCE.iterdir() if p.is_file()]
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(paths)}


def snapshot(directory):
    for line in git('ls-tree', '-r', RESOURCE, '--', 'skills/con-artist').decode().splitlines():
        info, name = line.split('\t', 1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported pinned resource')
        path = directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file', 'blob', oid))
        path.chmod(int(mode[-3:], 8))
    if not (directory / 'skills/con-artist/SKILL.md').is_file():
        raise ValueError('Pinned entrypoint missing')


def frozen(output):
    if 'REQUEST_RETRIES' in os.environ:
        raise ValueError('Unexpected REQUEST_RETRIES; do not change host settings')
    return dict(identities=identities(), cases=fixture.cases(Path(sys.executable).absolute()),
                settings=dict(SETTINGS), schedule=[list(x) for x in SCHEDULE], environment=environment(),
                resource_digests={c:run.resource_digest(output / c / 'skills') for c in CONDITIONS})


def prepare(output):
    if output.exists():
        raise FileExistsError(output)
    controls = validate_preflight()
    output.mkdir(parents=True, exist_ok=False)
    for condition in CONDITIONS:
        (output / condition / 'skills').mkdir(parents=True)
    snapshot(output / 'current')
    manifest = dict(frozen(output), resource_revision=git('rev-parse', RESOURCE).decode().strip(),
                    preflight_capture=controls, completed_cells=[], stopped_after_limit=False,
                    prepared_at=datetime.now(timezone.utc).isoformat())
    for directory in (output, *(output / c for c in CONDITIONS)):
        (directory / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


def execute(output, manifest):
    if (any(manifest.get(k) != v for k,v in frozen(output).items())
            or manifest['completed_cells'] or manifest['stopped_after_limit']):
        raise ValueError('Frozen inputs changed or execution already attempted')
    with (output / 'execution-started.json').open('x') as stream:
        json.dump(dict(revision=git('rev-parse', 'HEAD').decode().strip(),
                       started_at=datetime.now(timezone.utc).isoformat()), stream)
    disabled = run.disabled_skills()
    for index, condition in SCHEDULE:
        if any(manifest.get(k) != v for k,v in frozen(output).items()):
            raise ValueError('Frozen inputs changed between cells; do not restart')
        case = manifest['cases'][index]
        print('Starting ' + case['id'] + ' / ' + condition, flush=True)
        result = run.run_cell(case, 'baseline' if condition == 'baseline' else 'skill', 1,
            output / condition, SETTINGS['model'], SETTINGS['effort'], SETTINGS['timeout_seconds'],
            disabled, skills_root=output / condition / 'skills',
            workspace_root=output / 'workspaces' / condition, persist_session=True)
        manifest['completed_cells'].append(dict(case_id=case['id'], condition=condition,
            **{k:result[k] for k in ('completed','timed_out','limit_detected','usage','elapsed_seconds')}))
        manifest['stopped_after_limit'] = bool(result['limit_detected'])
        (output / 'run.json').write_text(json.dumps(manifest, indent=2) + '\n')
        print(json.dumps(manifest['completed_cells'][-1]), flush=True)
        if result['limit_detected']:
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
        prepare(output)
        print('Prepared two requests/four sessions; no model calls.')
