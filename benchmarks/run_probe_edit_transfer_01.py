"""Configure the existing exclusive scheduler for six frozen probe-edit cells."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import probe_edit_transfer_model_cases as fixture

ROOT = fixture.ROOT
CURRENT = 'aed8a27'
PREVIOUS = '23f06d2'
EVIDENCE = ROOT/'benchmarks/results/probe-edit-transfer-01-preflight.json'


def load_driver(name):
    spec = importlib.util.spec_from_file_location(name,ROOT/'benchmarks/run_packaging_specifier_01.py')
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    return driver


def identities():
    paths = ['benchmarks/run_probe_edit_transfer_01.py','benchmarks/run_packaging_specifier_01.py',
        'benchmarks/run.py','benchmarks/probe_edit_transfer_model_cases.py','benchmarks/probe_edit_transfer_cases.py',
        'benchmarks/packaging_specifier_cases.py','benchmarks/packaging-specifier-01-source.json',
        'benchmarks/results/packaging-specifier-01-preflight/summary.json',
        'benchmarks/PROBE-EDIT-TRANSFER-01-SELECTION.md','benchmarks/PROBE-EDIT-TRANSFER-01-PROTOCOL.md',
        'benchmarks/results/probe-edit-transfer-01-preflight.json',
        'tests/test_probe_edit_transfer_cases.py','tests/test_probe_edit_transfer_runner.py']
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}


def validate_preflight():
    report = json.loads(EVIDENCE.read_text())
    if report['python'] != sys.version:
        raise ValueError('Use preflight Python version')
    for key,path in [('fixture_sha256',ROOT/'benchmarks/probe_edit_transfer_cases.py'),
                     ('helper_sha256',ROOT/'skills/con-artist/scripts/audit.py')]:
        if report[key] != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Changed author preflight inputs')
    if {(r['variant'],r['form']) for r in report['records']} != {(v,f) for v in ('full','prefix') for f in ('replacement','edit')}:
        raise ValueError('Missing native controls')
    for row in report['records']:
        if row['fresh_import']['exit_code'] or row['result']['status'] != 'observed':
            raise ValueError('Native import/comparison incomplete')
        checks = row['result']['checks']
        if set(checks) != {'correct_tests','mutant_tests','correct_probe','mutant_probe'}:
            raise ValueError('Missing native phase')
        for phase,check in checks.items():
            code = int(phase == 'mutant_probe')
            if (check['exit_code'] != code or check['timed_out'] or check['output_truncated']
                    or ('9 failed' if code else '9 passed') not in check['output']):
                raise ValueError('Invalid native phase outcome')
        if not row['result']['integrity']['project_guard']['unchanged']:
            raise ValueError('Source guard failed')
    return dict(evidence_sha256=hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
                current_revision=CURRENT, predecessor_revision=PREVIOUS)


def configured_driver():
    driver = load_driver('_probe_edit_six_cells')
    predecessor = load_driver('_probe_edit_previous_snapshot')
    driver.fixture = fixture
    driver.RESOURCE = CURRENT
    predecessor.RESOURCE = PREVIOUS
    driver.CONDITIONS = ('baseline','predecessor','current')
    driver.SCHEDULE = [(0,'baseline'),(0,'predecessor'),(0,'current'),
                       (1,'current'),(1,'predecessor'),(1,'baseline')]
    driver.identities = identities
    driver.validate_preflight = validate_preflight
    original_snapshot = driver.snapshot
    def snapshot(directory):
        if directory.name != 'current':
            raise ValueError('Snapshot requires the current condition directory')
        original_snapshot(directory)
        predecessor.snapshot(directory.parent/'predecessor')
    driver.snapshot = snapshot
    return driver


driver = configured_driver()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output,json.loads((output/'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared six cells; no model calls.')
