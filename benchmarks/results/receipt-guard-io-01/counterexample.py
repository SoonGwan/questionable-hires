from pathlib import Path
import importlib.util,json,os,subprocess,sys,tempfile
from unittest.mock import patch
ROOT=Path('<HOME>/Documents/GitHub/questionable-hires')
sys.path.insert(0,str(ROOT/'tests'))
import test_receipt_helper as fixture
source=subprocess.check_output(['git','-C',str(ROOT),'show','d4bacdf6:skills/receipt/scripts/compare.py'])
rows=[]
with tempfile.TemporaryDirectory(prefix='qh-guard-counter-') as tmp:
 oldpath=Path(tmp)/'before.py';oldpath.write_bytes(source)
 for label,script in [('before',oldpath),('prototype',ROOT/'skills/receipt/scripts/compare.py')]:
  spec=importlib.util.spec_from_file_location(label,script);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  case=fixture.ReceiptHelperTests('runTest');case.setUp()
  try:
   watched=case.root/'notes.txt';watched.write_bytes(b'original');watched.chmod(0o600)
   native=module.run_check;fdopen=os.fdopen;state=dict(checks=0,mutated=False,results=[])
   class Stream:
    def __init__(self,stream):self.stream=stream
    def __enter__(self):return self
    def __exit__(self,*args):return self.stream.__exit__(*args)
    def fileno(self):return self.stream.fileno()
    def read(self,size):
     data=self.stream.read(size)
     if data and state['checks']==2 and not state['mutated']:
      watched.write_bytes(b'changed!');state['mutated']=True
     return data
   identity=watched.stat()
   def open_stream(fd,*args):
    stat=os.fstat(fd);stream=fdopen(fd,*args)
    return Stream(stream) if (stat.st_dev,stat.st_ino)==(identity.st_dev,identity.st_ino) else stream
   def checks(*args,**kwargs):
    result=native(*args,**kwargs);state['checks']+=1
    state['results'].append(dict(exit_code=result['exit_code'],suite_observation=result.get('suite_observation')))
    return result
   with patch.object(module,'run_check',side_effect=checks),patch.object(module.os,'fdopen',side_effect=open_stream):
    try:
     result=module.compare(case.root,dict(case.recipe,watch=['notes.txt'],guard_tree=True))
     outcome=dict(accepted=True,tree_guard_unchanged=result['tree_guard']['unchanged'])
    except RuntimeError as error:outcome=dict(accepted=False,error=str(error))
   rows.append(dict(condition=label,**outcome,mutated=state['mutated'],final_bytes=watched.read_text(),native_results=state['results']))
  finally:case.doCleanups()
assert rows[0]['accepted'] is False and rows[1]['accepted'] is True and all(r['mutated'] for r in rows)
Path('<TEMP>').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
