"""Six serial history-review cells using the existing exclusive scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

import interpreter_route_cases_01 as fixture

ROOT = fixture.ROOT
spec = importlib.util.spec_from_file_location('_interpreter_route_scheduler',
                                            ROOT/'benchmarks/run_packaging_specifier_01.py')
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
driver.fixture = fixture
driver.RESOURCE = 'e918d02d'
driver.CONDITIONS = ('baseline','predecessor','current')
driver.SCHEDULE = [(0,'baseline'),(0,'predecessor'),(0,'current'),
                   (1,'current'),(1,'predecessor'),(1,'baseline')]
driver.validate_preflight = fixture.preflight
driver.environment = lambda: dict(python=sys.version,platform=platform.platform(),
                                  scope='Host staging runtime; model must resolve its project-compatible interpreter')


def identities():
    names = ['benchmarks/run_interpreter_route_01.py','benchmarks/interpreter_route_cases_01.py',
             'benchmarks/interpreter_route_source_01.json','benchmarks/INTERPRETER-ROUTE-01-PROTOCOL.md',
             'benchmarks/run_packaging_specifier_01.py','benchmarks/run.py',
             'tests/test_controlled_fetch_asset.py','tests/test_interpreter_route_runner.py',
             'tests/test_packaging_specifier_runner.py']
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}


def snapshot(directory):
    for condition, revision in [('current','e918d02d'),('predecessor','75183f2f')]:
        for line in driver.git('ls-tree','-r',revision,'--','skills/necromancer').decode().splitlines():
            head,name = line.split('\t',1)
            mode,kind,oid = head.split()
            if kind!='blob' or mode not in ('100644','100755'):
                raise ValueError('Unsupported pinned resource')
            path = directory.parent/condition/name
            path.parent.mkdir(parents=True,exist_ok=True)
            with path.open('xb') as stream:
                stream.write(driver.git('cat-file','blob',oid))
            path.chmod(int(mode[-3:],8))


driver.identities = identities
driver.snapshot = snapshot

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output,json.loads((output/'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared six cells with native author controls; no model calls.')
