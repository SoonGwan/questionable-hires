"""Reuse the frozen four-cell scheduler with configuration-specific inputs."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import config_layers_cases as fixture

ROOT = fixture.ROOT
EVIDENCE = ROOT / 'benchmarks/results/config-layers-01-preflight.json'


def identities():
    paths = ['benchmarks/run_config_layers_01.py', 'benchmarks/config_layers_cases.py',
             'benchmarks/run_packaging_specifier_01.py', 'benchmarks/run.py',
             'benchmarks/CONFIG-LAYERS-01-SELECTION.md', 'benchmarks/CONFIG-LAYERS-01-PROTOCOL.md',
             'benchmarks/results/config-layers-01-preflight.json',
             'tests/test_config_layers_cases.py', 'tests/test_config_layers_runner.py',
             'tests/test_packaging_specifier_runner.py']
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}


def validate_preflight():
    report = json.loads(EVIDENCE.read_text())
    if report['python'] != sys.version:
        raise ValueError('Use the recorded native preflight interpreter')
    for key, path in [('helper_sha256', ROOT / 'skills/con-artist/scripts/audit.py'),
                      ('fixture_sha256', Path(fixture.__file__))]:
        if report[key] != hashlib.sha256(path.read_bytes()).hexdigest():
            raise ValueError('Native preflight input identity changed')
    if report['fresh_import']['exit_code'] or not report['originals_unchanged']:
        raise ValueError('Native source/import controls did not pass')
    for label, count in [('single', 1), ('multiple', 4)]:
        result = report['cases'][label]
        if result['status'] != 'observed' or len(result['audits']) != count:
            raise ValueError('Incomplete native author controls')
        for index, audit in enumerate(result['audits']):
            checks = audit['checks']
            if audit['status'] != 'observed' or checks['correct_tests']['exit_code'] != 0:
                raise ValueError('Invalid correct baseline')
            expected = int(index == 3)
            if checks['mutant_tests']['exit_code'] != expected:
                raise ValueError('Changed native outcomes')
            if not expected and (checks['correct_probe']['exit_code'] != 0
                                 or checks['mutant_probe']['exit_code'] != 1):
                raise ValueError('Missing stronger assertion controls')
            for check in checks.values():
                if check['timed_out'] or check.get('output_truncated'):
                    raise ValueError('Incomplete native output')
                if check['exit_code'] == 1 and 'AssertionError:' not in check['output']:
                    raise ValueError('Failure is not an assertion')
    return report


def configured_driver():
    # Load a private module instance; do not mutate the historical runner imported
    # by its own tests. Reuse its scheduling/exclusive-start implementation.
    spec = importlib.util.spec_from_file_location('_config_four_cell_driver',
        ROOT / 'benchmarks/run_packaging_specifier_01.py')
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.fixture = fixture
    driver.RESOURCE = 'e1e1ef8'
    driver.identities = identities
    driver.validate_preflight = validate_preflight
    return driver


driver = configured_driver()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared two configuration tasks/four sessions; no model calls.')
