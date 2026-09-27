import glob,json,os,py_compile,sys
from pathlib import Path
source=Path('owned_bytecode_input.py');source.write_text('value = 17\n')
actual=py_compile.compile(str(source),doraise=True)
source.unlink()
expected=glob.glob('__pycache__/owned_bytecode_input.*.pyc')
print(json.dumps({'pycache_prefix_is_none':sys.pycache_prefix is None,'dont_write_bytecode':sys.dont_write_bytecode,'expected_cache_count':len(expected),'actual_inside_project':Path(actual).resolve().is_relative_to(Path.cwd())}))
assert len(expected)==1
