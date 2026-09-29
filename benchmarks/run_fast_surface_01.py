"""Bounded same-model tier screen; reuse namespace and native probe controls."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_fast_namespace_base',ROOT/'benchmarks/run_namespace_surface_01.py')
namespace=importlib.util.module_from_spec(spec);spec.loader.exec_module(namespace)
base=namespace.base
shared=list(base.FLAGS['apps_excluded'])
base.FLAGS={'lean_standard':[*shared,'-c','service_tier="default"'], 'lean_fast':[*shared,'-c','service_tier="fast"']}
base.CASE['id']='fast-native-fix'
original_frozen=base.frozen

def frozen():
    result=original_frozen()
    for name in ('benchmarks/run_fast_surface_01.py','benchmarks/FAST-SURFACE-01-PROTOCOL.md','tests/test_fast_surface_01.py'):
        result['sources'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result

base.frozen=frozen
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();out=args.output.resolve()
    if args.execute:base.execute(out,json.loads((out/'run.json').read_text()))
    else:base.prepare(out);print('Two tier conditions prepared; no model calls.')
