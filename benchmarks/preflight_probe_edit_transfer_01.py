"""Author native preflight; no model session or source-project mutation."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'benchmarks'))
import probe_edit_transfer_cases as fixture
from export import redact_paths

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=Path,required=True)
args = parser.parse_args()
if args.output.exists() or args.output.is_symlink():
    raise FileExistsError('Preflight output already exists: ' + str(args.output))

spec = importlib.util.spec_from_file_location('audit', ROOT/'skills/con-artist/scripts/audit.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)
variants, fault, edit = fixture.inputs()
records = []
for name, files in variants.items():
    with tempfile.TemporaryDirectory(prefix='probe-edit-preflight-', dir=ROOT/'benchmarks') as folder:
        root = Path(folder)
        for path, text in files.items():
            target = root/path
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(text.encode()); target.chmod(0o644)
        env = dict(os.environ, PYTHONPATH=str(root/'src'), PYTHONDONTWRITEBYTECODE='1')
        fresh = subprocess.run([sys.executable,'-B','-c',
            'import pathlib, packaging; assert pathlib.Path(packaging.__file__).resolve().is_relative_to(pathlib.Path("src").resolve()); print(packaging.__version__)'],
            cwd=root,env=env,capture_output=True,text=True,timeout=10)
        assert fresh.returncode == 0, fresh.stderr
        for form in ('replacement','edit'):
            recipe = fixture.recipe(files,fault,edit,form)
            result = audit.audit(root,recipe,python=sys.executable)
            assert result['status'] == 'observed', result
            for phase, code in dict(correct_tests=0,mutant_tests=0,correct_probe=0,mutant_probe=1).items():
                check = result['checks'][phase]
                assert check['exit_code'] == code and not check['timed_out'] and not check['output_truncated'], check
                assert 'Verified native test Specifier binding' in check['output']
                assert ('9 failed' if code else '9 passed') in check['output'], check
            assert "assert '' ==" in result['checks']['mutant_probe']['output']
            assert result['integrity']['project_guard']['unchanged'] and result['integrity']['owned_scratch_removed']
            raw = json.dumps(result).replace(folder,'<PROJECT>')
            records.append(dict(variant=name,form=form,test_file_bytes=len(files[fixture.TEST_FILE].encode()),
                compact_recipe_bytes=len(json.dumps(recipe,separators=(',',':')).encode()),
                fresh_import=dict(exit_code=fresh.returncode,stdout=fresh.stdout,stderr=fresh.stderr),result=json.loads(raw)))
report = dict(kind='author native preflight, not model performance', python=sys.version,
    fixture_sha256=hashlib.sha256(Path(fixture.__file__).read_bytes()).hexdigest(),
    helper_sha256=hashlib.sha256((ROOT/'skills/con-artist/scripts/audit.py').read_bytes()).hexdigest(),records=records)
target=args.output
with target.open('x') as out:
    out.write(redact_paths(json.dumps(report,indent=2))+'\n')
for row in records:
    print(row['variant'],row['form'],row['test_file_bytes'],row['compact_recipe_bytes'])
