"""New frozen native split comparison; reuse the exclusive six-cell scheduler."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import native_split_cases_02 as fixture

ROOT=fixture.ROOT

def identities():
    names=['benchmarks/run_native_split_02.py','benchmarks/native_split_cases_02.py',
           'benchmarks/native_split_source_02.json','benchmarks/native_split_source_02_manifest.json',
           'benchmarks/run_assertion_contract_01.py','benchmarks/run_packaging_specifier_01.py',
           'benchmarks/run.py','benchmarks/NATIVE-SPLIT-02-PROTOCOL.md',
           'tests/test_native_split_cases.py']
    return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}

spec=importlib.util.spec_from_file_location('_native_split_scheduler_adapter',ROOT/'benchmarks/run_assertion_contract_01.py')
adapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(adapter)
adapter.CURRENT='6c099d68';adapter.PREVIOUS='33530f98';adapter.fixture=fixture;adapter.identities=identities
driver=adapter.configured_driver()
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if args.execute:driver.execute(output,json.loads((output/'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared six cells; eight native author controls passed; no model calls.')
