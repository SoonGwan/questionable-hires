import gzip,hashlib,io,json,os,shutil,tarfile,time,urllib.request
from pathlib import Path
os.umask(0o077)
r=Path(__file__).resolve().parent;prior=Path('/tmp/qh-external-bundle-02-private-grading/official-image-runtime-01');old=json.loads((prior/'requests2674-manifest.json').read_text());m=json.loads((r/'manifest.json').read_text());c=(r/'config.json').read_bytes();cfg=json.loads(c)
assert hashlib.sha256((r/'manifest.json').read_bytes()).hexdigest()=='d873716d5de2e1caaf0f4046a37b9c376e6137022fd9a1b7b47a8292dc428771'
assert hashlib.sha256(c).hexdigest()=='6685f236ddea92e412c046f1276f178d34895e4efbda2830ac3ab81903364787'
assert shutil.disk_usage(r).free>8*1024**3
cached={x['digest']:Path(x['path']) for source in ('/tmp/qh-pytest5221-container01/transport.json','/tmp/qh-pytest11143-container01/transport.json') for x in json.loads(Path(source).read_text())['layers']}
repo='swebench/sweb.eval.x86_64.pytest-dev_1776_pytest-5103';token=json.load(urllib.request.urlopen('https://auth.docker.io/token?service=registry.docker.io&scope=repository:'+repo+':pull',timeout=25))['token'];start=time.monotonic();downloaded=0;rows=[];paths=[]
for i,x in enumerate(m['layers']):
 p=cached.get(x['digest']);reused=p is not None
 if p is None:
  p=r/(str(i)+'.tar.gz');assert not p.exists()
  with urllib.request.urlopen(urllib.request.Request('https://registry-1.docker.io/v2/'+repo+'/blobs/'+x['digest'],headers={'Authorization':'Bearer '+token}),timeout=40) as response,p.open('xb') as f:
   while chunk:=response.read(1024*1024):
    downloaded+=len(chunk);assert downloaded<=512*1024**2 and time.monotonic()-start<600;f.write(chunk)
 h=hashlib.sha256();size=0
 with p.open('rb') as f:
  while chunk:=f.read(1024*1024):h.update(chunk);size+=len(chunk)
 assert 'sha256:'+h.hexdigest()==x['digest'] and size==x['size']
 rows.append(dict(index=i,path=str(p),digest=x['digest'],compressed_bytes=size,reused=reused));paths.append(p);(r/'acquisition.json').write_text(json.dumps(dict(layers=rows,downloaded_bytes=downloaded),indent=2)+'\n');print(json.dumps({k:v for k,v in rows[-1].items() if k!='path'}),flush=True)
start=time.monotonic();total=0
for i,p in enumerate(paths):
 h=hashlib.sha256();size=0
 with gzip.open(p,'rb') as f:
  while chunk:=f.read(1024*1024):
   h.update(chunk);size+=len(chunk);total+=len(chunk);assert total<10*1024**3 and time.monotonic()-start<600
 assert 'sha256:'+h.hexdigest()==cfg['rootfs']['diff_ids'][i]
 rows[i].update(diff_id='sha256:'+h.hexdigest(),uncompressed_bytes=size)
config_hash=hashlib.sha256(c).hexdigest();transport=[dict(Config=config_hash+'.json',RepoTags=['qh-official-pytest5103:pair01'],Layers=['layers/'+str(i)+'.tar.gz' for i in range(len(paths))])]
with tarfile.open(r/'image.docker.tar','w',format=tarfile.PAX_FORMAT) as tf:
 for name,data in [(config_hash+'.json',c),('manifest.json',json.dumps(transport).encode())]:
  e=tarfile.TarInfo(name);e.size=len(data);e.mode=0o600;tf.addfile(e,io.BytesIO(data))
 for i,p in enumerate(paths):
  assert time.monotonic()-start<600;e=tarfile.TarInfo('layers/'+str(i)+'.tar.gz');e.size=p.stat().st_size;e.mode=0o600
  with p.open('rb') as f:tf.addfile(e,f)
archive=r/'image.docker.tar';assert archive.stat().st_size<5*1024**3;h=hashlib.sha256()
with archive.open('rb') as f:
 while chunk:=f.read(1024*1024):h.update(chunk)
report=dict(config_sha256=config_hash,layers=rows,archive_sha256=h.hexdigest(),archive_bytes=archive.stat().st_size,downloaded_bytes=downloaded,model_calls=0,image_files_extracted_on_host=0)
(r/'transport.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(result='PASS',archive_bytes=report['archive_bytes'],downloaded_bytes=downloaded)))
