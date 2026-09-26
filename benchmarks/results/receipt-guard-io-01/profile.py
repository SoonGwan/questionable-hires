from pathlib import Path
import hashlib,importlib.util,json,statistics,subprocess,tempfile,time
ROOT=Path('<HOME>/Documents/GitHub/questionable-hires')
source=ROOT/'skills/receipt/scripts/compare.py'
old=subprocess.check_output(['git','-C',str(ROOT),'show','d4bacdf6:skills/receipt/scripts/compare.py'])
with tempfile.TemporaryDirectory(prefix='qh-receipt-guard-io-') as temporary:
 root=Path(temporary);oldfile=root/'old.py';oldfile.write_bytes(old)
 def load(name,path):
  spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
 before=load('before',oldfile);after=load('after',source);oldfile.unlink()
 data=bytes(range(256))*32768
 (root/'selected.bin').write_bytes(data);(root/'selected.bin').chmod(0o600)
 (root/'unselected.bin').write_bytes(bytes(range(256))*4096)
 (root/'empty').mkdir();(root/'link').symlink_to('missing-target')
 expected={'selected.bin':(data,0o600)}
 def original():
  for name,(content,mode) in expected.items():
   path=root/name
   assert not path.is_symlink() and path.is_file()
   assert before.read_limited(path,len(content))==content
   assert path.stat().st_mode & 0o777==mode
  return before.tree_inventory(root)
 def candidate():return after.tree_inventory(root,selected=expected)
 assert original()==candidate()
 rows=[]
 for index in range(20):
  times={}
  for name,call in ((('before',original),('after',candidate)) if index%2==0 else (('after',candidate),('before',original))):
   started=time.perf_counter();result=call();times[name]=time.perf_counter()-started
  rows.append(dict(index=index,**times))
 b=statistics.median(r['before'] for r in rows);a=statistics.median(r['after'] for r in rows)
 report=dict(before_revision='d4bacdf6',before_sha256=hashlib.sha256(old).hexdigest(),candidate_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),selected_bytes=len(data),other_regular_bytes=1048576,rows=rows,median_before_seconds=b,median_after_seconds=a,median_change_percent=(a/b-1)*100,limitation='Author isolated final preservation-pass timings only,20 alternating warmed shared-filesystem pairs on one synthetic9MiB tree. Same complete inventory and exact selected-byte/mode verification; not native test timings, model tokens, whole-task speed, independent samples or broad all-eight improvement.')
 Path('<TEMP>').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
