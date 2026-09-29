"""Package previously verified blobs; never extract image paths on the host."""
import gzip,hashlib,io,json,tarfile,time
from pathlib import Path
out=Path(__file__).resolve().parent
prior=Path('/tmp/qh-external-bundle-02-private-grading/official-image-runtime-01')
source=Path('/tmp/qh-owned-official-layers-01')
manifest_bytes=(prior/'requests2674-manifest.json').read_bytes()
config_bytes=(prior/'requests2674-config.json').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest()=='c83bd92b48356279e868d16d51ec15ca1481fa1bc97968e7a8d935df062f0bf2'
config_hash=hashlib.sha256(config_bytes).hexdigest()
assert config_hash=='1cf3ffbd1932395d2603da9b51dbb7383dc9f64044d241e3cd6b418d5fe56821'
manifest=json.loads(manifest_bytes);config=json.loads(config_bytes)
assert len(manifest['layers'])==len(config['rootfs']['diff_ids'])==10
started=time.monotonic();rows=[];paths=[];total=0
def digest(path,compressed=False):
 global total
 h=hashlib.sha256();size=0
 with (gzip.open(path,'rb') if compressed else path.open('rb')) as f:
  while block:=f.read(1024*1024):
   assert time.monotonic()-started<570
   h.update(block);size+=len(block)
   if compressed:total+=len(block);assert total<10*1024**3
 return h.hexdigest(),size
for i,layer in enumerate(manifest['layers']):
 if i in (1,2,8):p=source/(str(i)+'.tar.gz')
 elif i==0:p=Path('/tmp/qh-owned-official-python-01/base-layer.tar.gz')
 elif i==6:p=prior/'requests2674-environment-layer.tar.gz'
 else:p=prior/'requests2674-small-layers'/(str(i)+'.tar.gz')
 raw,raw_size=digest(p);assert 'sha256:'+raw==layer['digest'] and raw_size==layer['size']
 diff,size=digest(p,True);assert 'sha256:'+diff==config['rootfs']['diff_ids'][i]
 paths.append(p);rows.append(dict(index=i,sha256=raw,compressed_bytes=raw_size,diff_id='sha256:'+diff,uncompressed_bytes=size))
 print(json.dumps(rows[-1]),flush=True)
config_name=config_hash+'.json'
transport=[dict(Config=config_name,RepoTags=['qh-official-requests2674:runtime01'],Layers=['layers/'+str(i)+'.tar.gz' for i in range(10)])]
archive_path=out/'image.docker.tar'
with tarfile.open(archive_path,'w',format=tarfile.PAX_FORMAT) as archive:
 for name,data in [(config_name,config_bytes),('manifest.json',json.dumps(transport,separators=(',',':')).encode())]:
  entry=tarfile.TarInfo(name);entry.size=len(data);entry.mode=0o600;archive.addfile(entry,io.BytesIO(data))
 for i,p in enumerate(paths):
  assert time.monotonic()-started<570
  entry=tarfile.TarInfo('layers/'+str(i)+'.tar.gz');entry.size=p.stat().st_size;entry.mode=0o600
  with p.open('rb') as f:archive.addfile(entry,f)
assert archive_path.stat().st_size<5*1024**3
archive_hash,size=digest(archive_path)
report=dict(config_sha256=config_hash,layers=rows,archive_sha256=archive_hash,archive_bytes=size,seconds=round(time.monotonic()-started,3),model_calls=0,image_files_extracted_on_host=0)
(out/'transport.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(result='PASS',archive_bytes=size,seconds=report['seconds'])))
