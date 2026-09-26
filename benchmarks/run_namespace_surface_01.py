"""Reuse the native availability probe for documented per-call namespace exclusion."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_namespace_surface_base',ROOT/'benchmarks/run_tool_surface_01.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base.FLAGS={'apps_only':['--disable','apps'], 'apps_excluded':['--disable','apps','-c','features.code_mode.excluded_tool_namespaces=["web","imagegen","clock"]']}
base.CASE['id']='namespace-native-fix'
original_frozen=base.frozen

def frozen():
    result=original_frozen()
    for name in ('benchmarks/run_namespace_surface_01.py','benchmarks/NAMESPACE-SURFACE-01-PROTOCOL.md','tests/test_namespace_surface_01.py'):
        result['sources'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result

base.frozen=frozen
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();out=args.output.resolve()
    if args.execute:base.execute(out,json.loads((out/'run.json').read_text()))
    else:base.prepare(out);print('Two availability conditions prepared; no model calls.')
