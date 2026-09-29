"""Inline API candidate; reuse guarded paired development runner."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('_matrix_pair_base',ROOT/'benchmarks/run_necromancer_decision_checks_01.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
base.PREVIOUS='e109ae4a'
base.CANDIDATE='80c06e2e'
_original_snapshot=base.snapshot
_original_frozen=base.frozen


def snapshot(output,condition,revision,prefix):
    if condition=='candidate':prefix='benchmarks/candidates/necromancer-inline-matrix/skills/necromancer'
    return _original_snapshot(output,condition,revision,prefix)


def frozen(output):
    result=_original_frozen(output)
    for name in ('benchmarks/run_necromancer_inline_matrix_01.py',
                 'benchmarks/NECROMANCER-INLINE-MATRIX-01-PROTOCOL.md',
                 'tests/test_necromancer_inline_matrix_01.py',
                 'benchmarks/results/necromancer-inline-matrix-native-01/control.py'):
        result['source_hashes'][name]=hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
    result['resource_revisions']={'previous':base.PREVIOUS,'candidate':base.CANDIDATE}
    return result


base.snapshot=snapshot;base.frozen=frozen
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--execute',action='store_true');args=parser.parse_args();output=args.output.resolve()
    if args.execute:base.execute(output,json.loads((output/'run.json').read_text()))
    else:base.prepare(output);print('Inline API comparison prepared; zero model calls.')
