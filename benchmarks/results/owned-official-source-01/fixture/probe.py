import hashlib,json,os,stat,subprocess,sys
from pathlib import Path,PurePosixPath
os.chdir('/testbed');env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
command=['/usr/bin/git','-c','safe.directory=/testbed']
def invoke(args):
 return subprocess.run(command+args,capture_output=True,timeout=15,env=env)
head=invoke(['rev-parse','HEAD']);working=invoke(['diff','--quiet','HEAD','--']);cached=invoke(['diff','--cached','--quiet','HEAD','--']);entries=invoke(['ls-files','--stage','-z'])
result=dict(checkpoint='owned-official-source-01',models=0,external_cases=0,cwd=os.getcwd(),executable=sys.executable,git_path=command[0],git_exits=dict(head=head.returncode,working=working.returncode,cached=cached.returncode,entries=entries.returncode),head=head.stdout.decode().strip() if head.returncode==0 else None,native_stderr_hashes={n:hashlib.sha256(p.stderr).hexdigest() for n,p in [('head',head),('working',working),('cached',cached),('entries',entries)]})
expected=json.loads(Path('/_qh_probe_01/layers/base-table.json').read_text());seen=set();comparison=dict(missing=0,extra=0,data_mismatch=0,mode_mismatch=0)
counts=dict(tracked=0,regular=0,symlinks=0,unsupported=0,unmerged=0,missing=0,blob_mismatch=0,mode_mismatch=0);manifest=hashlib.sha256()
if entries.returncode==0:
 for entry in entries.stdout.split(b'\0'):
  if not entry:continue
  header,name=entry.split(b'\t',1);mode,blob,stage=header.split();path=Path(os.fsdecode(name))
  assert not path.is_absolute() and '..' not in PurePosixPath(os.fsdecode(name)).parts
  counts['tracked']+=1
  if stage!=b'0':counts['unmerged']+=1;continue
  if mode not in (b'100644',b'100755',b'120000'):counts['unsupported']+=1;continue
  try:
   info=path.lstat()
   if mode==b'120000':
    if not stat.S_ISLNK(info.st_mode):counts['mode_mismatch']+=1;continue
    data=os.fsencode(os.readlink(path));counts['symlinks']+=1
   else:
    if not stat.S_ISREG(info.st_mode):counts['mode_mismatch']+=1;continue
    assert info.st_size<20*1024*1024
    data=path.read_bytes();counts['regular']+=1
    if bool(info.st_mode&0o111)!=(mode==b'100755'):counts['mode_mismatch']+=1
   key=os.fsdecode(name);seen.add(key)
   if key not in expected:comparison['extra']+=1
   else:
    comparison['mode_mismatch']+=mode.decode()!=expected[key]['mode']
    comparison['data_mismatch']+=hashlib.sha256(data).hexdigest()!=expected[key]['sha256']
   actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest().encode()
   counts['blob_mismatch']+=actual!=blob
   manifest.update(name+b'\0'+mode+b'\0'+hashlib.sha256(data).digest())
  except FileNotFoundError:counts['missing']+=1
comparison['missing']=len(set(expected)-seen)
result['base_comparison']=comparison
result['base_table_sha256']=hashlib.sha256(Path('/_qh_probe_01/layers/base-table.json').read_bytes()).hexdigest()
result.update(counts=counts,tracked_manifest_sha256=manifest.hexdigest())
print('QH_SOURCE_OBSERVATION');print(json.dumps(result,sort_keys=True))
