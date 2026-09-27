import hashlib,json,os,posixpath,shutil,sys,tarfile,time
from pathlib import Path,PurePosixPath
root=Path(sys.argv[3]);root.mkdir(exist_ok=False)
ENV='opt/miniconda3/envs/testbed/'
PKG='opt/miniconda3/pkgs/'
OS=('usr/lib/x86_64-linux-gnu/','lib/x86_64-linux-gnu/')
started=time.monotonic()
def canonical(name):
 while name.startswith('./'):name=name[2:]
 if not name or name.startswith('/') or '\\' in name or any(p in ('.','..','') for p in name.split('/')):raise ValueError('Noncanonical selected archive path')
 return name

def copy_layer(layer,prefixes,destination,allow_cache=False):
 digest=hashlib.sha256()
 with Path(layer).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):digest.update(block)
 expected='0e43bc2a78057e6e6737b70d65be5424e7d737f26029c7a5bc282292ce5dffa7' if allow_cache else '39a945af8df2ad9343f141c82355d3f2c4b576d432eda34c460d630607462b60'
 assert digest.hexdigest()==expected,'Layer digest drift'
 with tarfile.open(layer,'r:gz') as t:
  members=t.getmembers();index={m.name.rstrip('/'):m for m in members}
  selected=[];copies={};links=[];skipped={};total=0
  for m in members:
   match=next((p for p in prefixes if m.name.startswith(p)),None)
   if not match or m.isdir():continue
   name=canonical(m.name);relative=canonical(name[len(match):]);target=destination/relative
   if m.isreg():copies.setdefault(name,[]).append((target,m.mode));total+=m.size
   elif m.islnk():
    link=canonical(m.linkname)
    if not any(link.startswith(p) for p in prefixes) and not (allow_cache and link.startswith(PKG)):
     skipped['external_hardlink']=skipped.get('external_hardlink',0)+1;continue
    source=index[link];assert source.isreg(),'Unresolved hardlink chain'
    copies.setdefault(link,[]).append((target,m.mode));total+=source.size
   elif m.issym():
    resolved=posixpath.normpath(m.linkname if m.linkname.startswith('/') else posixpath.join(posixpath.dirname(name),m.linkname)).lstrip('/')
    target_prefix=next((p for p in prefixes if resolved.startswith(p)),None)
    if not target_prefix:skipped['external_symlink']=skipped.get('external_symlink',0)+1;continue
    reltarget=canonical(resolved[len(target_prefix):]);links.append((target,os.path.relpath(destination/reltarget,target.parent),m.linkname.startswith('/')))
   else:skipped['special']=skipped.get('special',0)+1
  assert total<2_000_000_000 and len(copies)<30000 and shutil.disk_usage(root).free>total+100_000_000
  wrote=set();count=0
  with tarfile.open(layer,'r|gz') as stream:
   for m in stream:
    assert time.monotonic()-started<180,'Extraction deadline'
    if m.name not in copies:continue
    assert m.isreg() and m.size<200_000_000
    source=stream.extractfile(m);data=source.read();assert len(data)==m.size
    for target,mode in copies[m.name]:
     target.parent.mkdir(parents=True,exist_ok=True)
     with target.open('xb') as out:out.write(data)
     target.chmod(mode&0o777);count+=1
    wrote.add(m.name)
  assert wrote==set(copies),'Required regular payload absent'
  for target,relative,absolute in links:
   target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(relative)
  return dict(layer_sha256=digest.hexdigest(),regular_files=count,symlinks=len(links),absolute_symlinks_relocated=sum(x[2] for x in links),skipped=skipped,file_bytes=total)
result=dict(environment=copy_layer(sys.argv[1],(ENV,),root/'env',True),os_libraries=copy_layer(sys.argv[2],OS,root/'glibc'),elapsed_seconds=round(time.monotonic()-started,3),models=0,project_or_gold_extracted=False,limitation='Selected runtime subtree, not full OCI filesystem/layer application. External links skipped; absolute internal links relocated; no environment parity claim.')
(root.parent/'extraction-result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
