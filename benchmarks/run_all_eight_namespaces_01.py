"""Reuse the all-eight scheduler for one new namespace-transfer mechanism."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_eight_namespace_scheduler',ROOT/'benchmarks/run_all_eight_apps_01.py')
runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
runner.MODELS={'apps_only':'gpt-6-astra','apps_excluded':'gpt-6-astra'}
runner.FLAGS={'apps_only':['--disable','apps'], 'apps_excluded':['--disable','apps','-c','features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]']}
runner.base.CONDITIONS=tuple(runner.MODELS)
runner.base.RESOURCES={c:'0333a084' for c in runner.MODELS}
runner.base.SCHEDULE=[(i,c) for i in range(8) for c in (runner.base.CONDITIONS if i%2==0 else runner.base.CONDITIONS[::-1])]
original_identities=runner.identities

def identities():
    result=original_identities()
    for name in ('benchmarks/run_all_eight_namespaces_01.py','benchmarks/ALL-EIGHT-NAMESPACES-01-PROTOCOL.md','tests/test_all_eight_namespaces_01.py'):
        result['execution_sources'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result

runner.base.identities=identities
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();out=args.output.resolve()
    if args.execute:runner.execute(out,json.loads((out/'run.json').read_text()))
    else:runner.base.prepare(out);print('Sixteen current-resource namespace cells prepared; no model calls.')
