"""Inline direct-file excerpt candidate; reuse frozen real-source paired runner."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_file_regions_transfer_base',ROOT/'benchmarks/run_urllib3_inline_transfer_02.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base.RESOURCES={'previous':('8b1d8163','skills/necromancer'),'candidate':('97c15593','benchmarks/candidates/necromancer-file-regions/skills/necromancer')}
_original_frozen=base.frozen
_original_preflight=base.preflight
CONTROL='benchmarks/candidates/necromancer-file-regions/skills/necromancer/scripts/python_regions.py'

def frozen(source,output):
    result=_original_frozen(source,output)
    names=['benchmarks/run_necromancer_file_regions_01.py','benchmarks/NECROMANCER-FILE-REGIONS-01-PROTOCOL.md','tests/test_necromancer_file_regions_01.py',CONTROL]
    names += ['benchmarks/candidates/necromancer-file-regions/skills/necromancer/'+n for n in ['SKILL.md','scripts/python_regions.py','references/python-regions.md']]
    for n in names:result['source_hashes'][n]=hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
    return result

def preflight(source):
    previous=_original_preflight(source);before=base.fixture_identity(source)
    with tempfile.TemporaryDirectory(prefix='file-regions-transfer01-',dir=ROOT/'benchmarks/local-runs') as temp:
        project=Path(temp)/'project';base.run.prepare_repository(source,project)
        assert base.fixture_identity(project)==before
        observed=subprocess.run([sys.executable,'-I','-B',str(ROOT/CONTROL),'--path',str(project/'src/urllib3/util/retry.py'),'--name','Retry.is_retry','--name','Retry._is_method_retryable'],cwd=project,capture_output=True,text=True,timeout=30)
        if observed.returncode:raise ValueError('File-region candidate native gate failed')
        actual=json.loads(observed.stdout)
        assert actual['complete'] and len(actual['regions'])==2
        assert actual['source_sha256']==hashlib.sha256((project/'src/urllib3/util/retry.py').read_bytes()).hexdigest()
        assert base.fixture_identity(project)==before
    assert base.fixture_identity(source)==before
    return dict(original_copy_gate=previous,file_regions_candidate_copy_gate=actual)

base.frozen=frozen;base.preflight=preflight
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--source',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();source=args.source.resolve();output=args.output.resolve()
    if args.execute:base.execute(source,output,json.loads((output/'run.json').read_text()))
    else:base.prepare(source,output);print('File regions01 prepared; zero model calls.')
