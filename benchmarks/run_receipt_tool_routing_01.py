"""Same supplied tool, previous/candidate entry routing: four frozen cells."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('_receipt_tool_routing_base', ROOT/'benchmarks/run_receipt_tool_bridge_01.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
runner.base.CONDITIONS = ('previous','candidate')
runner.base.RESOURCES = {'previous':'08a18aed','candidate':'44c4ff5e'}
runner.base.SCHEDULE = [(0,'previous'),(0,'candidate'),(1,'candidate'),(1,'previous')]
runner.BRIDGE_CONDITIONS = runner.base.CONDITIONS
original_identities = runner.base.identities

def identities():
    result = original_identities()
    for name in ('benchmarks/run_receipt_tool_routing_01.py','benchmarks/RECEIPT-TOOL-ROUTING-01-PROTOCOL.md'):
        result['execution_sources'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    return result
runner.base.identities = identities

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if args.execute: runner.execute(output,json.loads((output/'run.json').read_text()))
    else:
        runner.base.prepare(output)
        print('Prepared four same-tool entry-routing cells; zero models.')
