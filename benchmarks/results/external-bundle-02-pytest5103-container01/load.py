from pathlib import Path
import subprocess,os,json,time
root=Path(__file__).resolve().parent;runtime=Path('/tmp/qh-linux-runtime01');env=dict(os.environ,LIMA_HOME=str(runtime/'state'));cli=str(runtime/'tools/bin/limactl')
expected=json.loads((root/'transport.json').read_text());start=time.monotonic();rows=[]
for name,args,timeout in [('space',['df','-B1','/var/lib/docker'],15),('archive-sha',['sha256sum','/home/qh/pytest5103-image.docker.tar'],30),('load',['sudo','docker','image','load','--input','/home/qh/pytest5103-image.docker.tar'],600),('inspect',['sudo','docker','image','inspect','qh-official-pytest5103:pair01'],20),('driver',['sudo','docker','info','--format','{{.Driver}}'],20)]:
 r=subprocess.run([cli,'shell','--tty=false','--workdir=/','author',*args],env=env,cwd=root,capture_output=True,timeout=timeout)
 (root/(name+'.stdout')).write_bytes(r.stdout);(root/(name+'.stderr')).write_bytes(r.stderr)
 rows.append(dict(step=name,exit_code=r.returncode));(root/'load-steps.json').write_text(json.dumps(rows,indent=2)+'\n')
 assert r.returncode==0,(name,r.stderr.decode()[-1000:])
 if name=='space':assert int(r.stdout.decode().splitlines()[-1].split()[3])>8*1024**3
 if name=='archive-sha':assert r.stdout.decode().split()[0]==expected['archive_sha256']
 if name=='inspect':
  d=json.loads(r.stdout)[0];assert d['Id']=='sha256:'+expected['config_sha256'];assert d['RootFS']['Layers']==[x['diff_id'] for x in expected['layers']]
  assert d['Architecture']=='amd64' and d['Os']=='linux' and not d['Config'].get('Volumes')
  (root/'loaded-identity.json').write_text(json.dumps(dict(image_id=d['Id'],diff_ids=d['RootFS']['Layers'],os=d['Os'],architecture=d['Architecture'],declared_volumes=d['Config'].get('Volumes')),indent=2)+'\n')
print(json.dumps(dict(result='PASS',seconds=round(time.monotonic()-start,3),driver=r.stdout.decode().strip())))
