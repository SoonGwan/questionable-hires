"""Six new authored audit cells using the existing exclusive scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import assertion_contract_cases as fixture

ROOT = fixture.ROOT
CURRENT = '33530f98'
PREVIOUS = '5f94777a'


def identities():
    paths = ['benchmarks/run_assertion_contract_01.py', 'benchmarks/assertion_contract_cases.py',
             'benchmarks/run_packaging_specifier_01.py', 'benchmarks/run.py',
             'benchmarks/ASSERTION-CONTRACT-01-PROTOCOL.md']
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in paths}


def configured_driver():
    spec = importlib.util.spec_from_file_location('_assertion_contract_scheduler', ROOT / 'benchmarks/run_packaging_specifier_01.py')
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    driver.fixture = fixture
    driver.RESOURCE = CURRENT
    driver.CONDITIONS = ('baseline', 'predecessor', 'current')
    driver.SCHEDULE = [(0, 'baseline'), (0, 'predecessor'), (0, 'current'),
                       (1, 'current'), (1, 'predecessor'), (1, 'baseline')]
    driver.identities = identities
    driver.validate_preflight = fixture.preflight
    def snapshot(directory):
        for condition, revision in [('current', CURRENT), ('predecessor', PREVIOUS)]:
            for line in driver.git('ls-tree', '-r', revision, '--', 'skills/con-artist').decode().splitlines():
                info, name = line.split('\t', 1)
                mode, kind, oid = info.split()
                if kind != 'blob' or mode not in ('100644', '100755'):
                    raise ValueError('Unsupported resource mode')
                target = directory.parent / condition / name
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(driver.git('cat-file', 'blob', oid))
                target.chmod(int(mode[-3:], 8))
    driver.snapshot = snapshot
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
        print('Prepared six cells; four native controls passed; no model calls.')
