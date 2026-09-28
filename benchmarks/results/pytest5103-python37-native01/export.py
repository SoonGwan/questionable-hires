import hashlib,json,os,subprocess,tarfile
from pathlib import Path
r=Path('/testbed');m=json.loads(Path('/qh/source-manifest.json').read_text())
assert all(hashlib.sha256((r/n).read_bytes()).hexdigest()==v['sha256'] for n,v in m.items())
head=subprocess.check_output(['git','-C',str(r),'rev-parse','HEAD'],text=True).strip()
assert head=='5df4d131d551b79b9fcf258482eaa4f59bf238b8'
entries=[r/n for n in m]+[p for p in (r/'.git').rglob('*') if p.is_file()]
assert not any(p.is_symlink() for p in (r/'.git').rglob('*'))
assert all(p.is_file() and not p.is_symlink() for p in entries)
assert sum(p.stat().st_size for p in entries)<512*1024**2
with tarfile.open('/tmp/source.tar','w') as tf:
 for p in entries:tf.add(str(p),arcname=str(p.relative_to(r)),recursive=False)
p=Path('/tmp/source.tar');record=dict(source_files=len(m),git_head=head,files=len(entries),archive_bytes=p.stat().st_size,archive_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),source_bytes_match=True)
assert record['archive_bytes']<512*1024**2
print(json.dumps(record),flush=True)
