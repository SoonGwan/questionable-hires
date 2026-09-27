"""Retained actual outcomes candidate; reuse frozen real-source paired runner."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_retained_transfer_base',ROOT/'benchmarks/run_urllib3_inline_transfer_02.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base.RESOURCES={'previous':('e109ae4a','skills/necromancer'),'candidate':('837988d5','benchmarks/candidates/necromancer-retained-matrix/skills/necromancer')}
_original_frozen=base.frozen
_original_preflight=base.preflight
CONTROL='benchmarks/results/necromancer-retained-matrix-native-01/control.py'

def frozen(source,output):
    result=_original_frozen(source,output)
    names=['benchmarks/run_necromancer_retained_matrix_01.py','benchmarks/NECROMANCER-RETAINED-MATRIX-01-PROTOCOL.md','tests/test_necromancer_retained_matrix_01.py',CONTROL]
    names += ['benchmarks/candidates/necromancer-retained-matrix/skills/necromancer/'+n for n in ['SKILL.md','scripts/call_matrix.py','references/call-matrix.md']]
    for n in names:result['source_hashes'][n]=hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
    return result

def preflight(source):
    previous=_original_preflight(source);before=base.fixture_identity(source)
    with tempfile.TemporaryDirectory(prefix='retained-transfer01-',dir=ROOT/'benchmarks/local-runs') as temp:
        project=Path(temp)/'project';base.run.prepare_repository(source,project)
        assert base.fixture_identity(project)==before
        observed=subprocess.run([sys.executable,'-B',str(ROOT/CONTROL),'--source',str(project)],cwd=project,capture_output=True,text=True,timeout=30)
        if observed.returncode:raise ValueError('Retained candidate native gate failed')
        actual=json.loads(observed.stdout)
        assert actual['actual_package_calls']==15 and all(actual['boundaries'].values())
        assert base.fixture_identity(project)==before
    assert base.fixture_identity(source)==before
    return dict(original_copy_gate=previous,retained_candidate_copy_gate=actual)

base.frozen=frozen;base.preflight=preflight
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();source=args.source.resolve();output=args.output.resolve()
    if args.execute:base.execute(source,output,json.loads((output/'run.json').read_text()))
    else:base.prepare(source,output);print('Retained matrix01 prepared; zero model calls.')
