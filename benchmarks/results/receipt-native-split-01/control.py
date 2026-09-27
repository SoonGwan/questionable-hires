"""Unmodified Receipt caller regressions on ordinary/split Git-free copies."""
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_native_split_candidate import apply, CONSTANTS
from export import redact_paths

MODULES = ('test_receipt_helper', 'test_receipt_tree_guard', 'test_receipt_guard_evidence',
           'test_receipt_native_invocation', 'test_receipt_assertion_observation',
           'test_receipt_module_bindings', 'test_receipt_multiple_before',
           'test_receipt_pytest_loading', 'test_receipt_node_compare', 'test_receipt_recipe_errors')
PYTHON = '/tmp/qh-validation-env/bin/python'
NODE_DIRECTORY = '/tmp/qh-release-node24-20260928/node-v24.16.0-darwin-arm64/bin'


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    if (OUT / 'results.json').exists():
        raise FileExistsError('Retain original outcomes, never overwrite')
    source = ROOT / 'skills/receipt/scripts/compare.py'
    recorded = dict(checkpoint='receipt-native-split-01', models=0,
        source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        transform_sha256=hashlib.sha256((ROOT/'benchmarks/receipt_native_split_candidate.py').read_bytes()).hexdigest(),
        controls=[], limitation='Native correctness/packaging controls, not token/time gains. Unmodified single-file relocation remains a required compatibility check.')
    with tempfile.TemporaryDirectory(prefix='qh-native-split-') as temporary:
        for arm in ('previous', 'candidate'):
            root = Path(temporary) / arm
            shutil.copytree(ROOT / 'skills/receipt', root / 'skills/receipt',
                            ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
            for directory, patterns in (('tests', ('*.py',)), ('benchmarks', ('*.py','*.json'))):
                (root/directory).mkdir()
                for pattern in patterns:
                    for path in (ROOT/directory).glob(pattern):
                        shutil.copy2(path,root/directory/path.name)
            if arm == 'candidate':
                recorded['candidate_bytes'] = apply(root / 'skills/receipt')
                previous = module(source, 'previous_split_control')
                candidate = module(root / 'skills/receipt/scripts/compare.py', 'candidate_split_control')
                assert all(getattr(previous,name)==getattr(candidate,name) for name in CONSTANTS)
                recorded['native_program_strings_identical'] = True
                recorded['candidate_sha256'] = {name:hashlib.sha256((root/'skills/receipt/scripts'/name).read_bytes()).hexdigest() for name in ('compare.py','native.py')}
            process = subprocess.run([PYTHON,'-B','-m','unittest','-v',*MODULES],
                cwd=root/'tests',env=dict(os.environ,PATH=NODE_DIRECTORY+os.pathsep+os.environ.get('PATH','')),
                text=True,capture_output=True,timeout=180)
            log = OUT/(arm+'.txt')
            log.write_text(redact_paths(process.stdout+process.stderr))
            recorded['controls'].append(dict(arm=arm,exit_code=process.returncode,
                log_sha256=hashlib.sha256(log.read_bytes()).hexdigest(),modules=list(MODULES)))
            (OUT/'results.json').write_text(json.dumps(recorded,indent=2)+'\n')
            print(arm,process.returncode,flush=True)
    return 0 if all(row['exit_code']==0 for row in recorded['controls']) else 1


if __name__ == '__main__':
    raise SystemExit(main())
