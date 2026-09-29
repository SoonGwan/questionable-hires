import hashlib,json,tarfile,time,urllib.request
from pathlib import Path,PurePosixPath
root=Path('/tmp/qh-owned-official-layers-01')
previous=Path('/tmp/qh-external-bundle-02-private-grading/official-image-runtime-01')
plan=json.loads((root/'freeze.json').read_text())
repo='swebench/sweb.eval.x86_64.psf_1776_requests-2674'
started=time.monotonic();outcomes=[];token=None

def persist():
 (root/'outcomes.json').write_text(json.dumps(dict(checkpoint=plan['checkpoint'],models=0,external_cases=0,elapsed_seconds=round(time.monotonic()-started,3),layers=outcomes),indent=2)+'\n')

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

for entry in plan['layers']:
 index=entry['index'];phase=time.monotonic();item=dict(entry)
 try:
  if entry['action']=='download':
   if token is None:
    with urllib.request.urlopen('https://auth.docker.io/token?service=registry.docker.io&scope=repository:'+repo+':pull',timeout=15) as response:token=json.load(response)['token']
   path=root/(str(index)+'.partial');count=0;h=hashlib.sha256()
   request=urllib.request.Request('https://registry-1.docker.io/v2/'+repo+'/blobs/sha256:'+entry['sha256'],headers={'Authorization':'Bearer '+token})
   with urllib.request.urlopen(request,timeout=15) as response,path.open('xb') as f:
    while True:
     assert time.monotonic()-phase<180 and time.monotonic()-started<600,'Acquisition deadline'
     b=response.read(1024*1024)
     if not b:break
     count+=len(b);assert count<=entry['bytes'],'Oversized layer'
     f.write(b);h.update(b)
   assert count==entry['bytes'] and h.hexdigest()==entry['sha256'],'Downloaded identity mismatch'
   complete=root/(str(index)+'.tar.gz');path.rename(complete);path=complete
  elif index==0:path=Path('/tmp/qh-owned-official-python-01/base-layer.tar.gz')
  elif index==6:path=previous/'requests2674-environment-layer.tar.gz'
  else:path=previous/'requests2674-small-layers'/(str(index)+'.tar.gz')
  assert path.stat().st_size==entry['bytes'] and digest(path)==entry['sha256'],'Existing layer identity mismatch'
  counts={};expanded=0;whiteouts=0;unsafe_paths=0;absolute_symlinks=0;parent_links=0;members=0
  with tarfile.open(path,'r|gz') as archive:
   for member in archive:
    assert time.monotonic()-started<600,'Header inventory deadline'
    members+=1;assert members<200000,'Header count ceiling'
    kind=member.type.decode('ascii',errors='replace');counts[kind]=counts.get(kind,0)+1
    n=member.name
    while n.startswith('./'):n=n[2:]
    if n.startswith('/') or '..' in PurePosixPath(n).parts or '\\' in n:unsafe_paths+=1
    if PurePosixPath(n).name.startswith('.wh.'):whiteouts+=1
    if member.isreg():expanded+=member.size
    if member.issym():
     absolute_symlinks+=member.linkname.startswith('/')
     parent_links+='..' in PurePosixPath(member.linkname).parts
  item.update(success=True,elapsed_seconds=round(time.monotonic()-phase,3),headers=members,types=counts,regular_payload_bytes=expanded,whiteouts=whiteouts,unsafe_header_paths=unsafe_paths,absolute_symlinks=absolute_symlinks,parent_link_targets=parent_links)
  outcomes.append(item);persist();print(json.dumps(item),flush=True)
 except Exception as error:
  item.update(success=False,error_type=type(error).__name__,elapsed_seconds=round(time.monotonic()-phase,3));outcomes.append(item);persist()
  raise RuntimeError('Pinned acquisition/header phase failed; token, redirects and private archive paths omitted') from None
