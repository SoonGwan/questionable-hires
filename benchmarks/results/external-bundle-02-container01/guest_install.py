import hashlib,json,subprocess,time
from pathlib import Path
started=time.monotonic()
versions={'docker.io':'26.1.5+dfsg1-9+deb13u1','docker-cli':'26.1.5+dfsg1-9+deb13u1','containerd':'1.7.24~ds1-6+deb13u1','runc':'1.1.15+ds1-2+b4','tini':'0.19.0-3+b8'}
pins=[name+'='+version for name,version in versions.items()]
def run(args):
 r=subprocess.run(args,capture_output=True,text=True,timeout=max(1,570-(time.monotonic()-started)))
 print(json.dumps(dict(command=args,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)),flush=True)
 if r.returncode:raise SystemExit(r.returncode)
 return r.stdout
run(['apt-get','--yes','--download-only','--no-install-recommends','install',*pins])
rows=[]
for p in sorted(Path('/var/cache/apt/archives').glob('*.deb')):
 name,version=subprocess.check_output(['dpkg-deb','-f',str(p),'Package','Version'],text=True).splitlines()
 name=name.removeprefix('Package: ');version=version.removeprefix('Version: ')
 assert versions.get(name)==version,(name,version)
 metadata=subprocess.check_output(['apt-cache','show',name+'='+version],text=True)
 expected={s.split(': ',1)[1] for s in metadata.splitlines() if s.startswith('SHA256: ')}
 digest=hashlib.sha256(p.read_bytes()).hexdigest();assert digest in expected
 rows.append(dict(package=name,version=version,bytes=p.stat().st_size,sha256=digest))
assert {r['package'] for r in rows}==set(versions)
assert sum(r['bytes'] for r in rows)<=256*1024**2
print(json.dumps(dict(verified_debs=rows)),flush=True)
run(['apt-get','--yes','--no-download','--no-install-recommends','install',*pins])
run(['systemctl','disable','docker.service','docker.socket','containerd.service'])
run(['systemctl','start','docker.service'])
run(['docker','version','--format','{{json .}}'])
print(json.dumps(dict(result='PASS',seconds=round(time.monotonic()-started,3))),flush=True)
