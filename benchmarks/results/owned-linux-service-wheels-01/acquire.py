import email,hashlib,json,struct,time,urllib.parse,urllib.request,zipfile
from pathlib import Path,PurePosixPath
root=Path('/tmp/qh-owned-linux-service-wheels-01');started=time.monotonic();outcomes=[];total=0
for line in (root/'requirements.txt').read_text().splitlines():
 name,version=line.split('==');item=dict(name=name,version=version)
 try:
  assert time.monotonic()-started<180
  with urllib.request.urlopen('https://pypi.org/pypi/'+name+'/'+version+'/json',timeout=15) as response:raw=response.read(2*1024*1024)
  metadata=json.loads(raw);assert metadata['info']['version']==version
  candidates=[]
  for entry in metadata['urls']:
   filename=entry['filename']
   if entry['packagetype']!='bdist_wheel' or entry.get('yanked',False):continue
   if name=='MarkupSafe':valid='-cp39-cp39-' in filename and 'manylinux' in filename and 'x86_64' in filename
   else:valid=filename.endswith('-none-any.whl') and ('-py3-' in filename or '-py2.py3-' in filename)
   if valid:candidates.append(entry)
  assert candidates,'No exact-version compatible wheel'
  entry=sorted(candidates,key=lambda e:e['filename'])[0];assert urllib.parse.urlsplit(entry['url']).hostname=='files.pythonhosted.org'
  assert entry['size']<20*1024*1024 and total+entry['size']<50*1024*1024
  path=root/'wheels'/entry['filename'];h=hashlib.sha256();count=0
  with urllib.request.urlopen(entry['url'],timeout=15) as response,path.with_suffix('.partial').open('xb') as output:
   while True:
    assert time.monotonic()-started<180
    b=response.read(1024*1024)
    if not b:break
    count+=len(b);assert count<=entry['size'];h.update(b);output.write(b)
  assert count==entry['size'] and h.hexdigest()==entry['digests']['sha256'],'Wheel identity mismatch'
  path.with_suffix('.partial').rename(path);total+=count;native=[];requires=[]
  with zipfile.ZipFile(path) as archive:
   assert sum(i.file_size for i in archive.infolist())<50*1024*1024
   for info in archive.infolist():
    assert not info.filename.startswith('/') and '..' not in PurePosixPath(info.filename).parts and '\\' not in info.filename
    if info.filename.endswith('.so'):
     data=archive.read(info);assert data[:6]==b'\x7fELF\x02\x01' and struct.unpack_from('<H',data,18)[0]==62
     native.append(dict(bytes=len(data),machine=62,sha256=hashlib.sha256(data).hexdigest()))
    if info.filename.endswith('.dist-info/METADATA'):
     message=email.message_from_bytes(archive.read(info));assert message['Version']==version
     requires=message.get_all('Requires-Dist',[])
  item.update(success=True,filename=entry['filename'],bytes=count,sha256=h.hexdigest(),pypi_metadata_sha256=hashlib.sha256(raw).hexdigest(),requires_dist=requires,native_elf_headers=native)
 except Exception as error:
  item.update(success=False,error_type=type(error).__name__)
  outcomes.append(item);(root/'outcomes.json').write_text(json.dumps(dict(wheels=outcomes,models=0,installed=False,elapsed_seconds=round(time.monotonic()-started,3)),indent=2)+'\n')
  raise RuntimeError('Frozen wheel acquisition failed; URL/response details omitted') from None
 outcomes.append(item);(root/'outcomes.json').write_text(json.dumps(dict(wheels=outcomes,models=0,installed=False,elapsed_seconds=round(time.monotonic()-started,3)),indent=2)+'\n')
 print(json.dumps(item),flush=True)
