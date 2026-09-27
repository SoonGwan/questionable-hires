import hashlib,importlib.util,json,os,selectors,signal,subprocess,sys,urllib.parse
from pathlib import Path
os.chdir('/testbed');sys.path[0]=''
import requests
prefix='/tmp/qh-http-service-lib';env=os.environ.copy();env['PIP_CONFIG_FILE']='/dev/null'
install=subprocess.run([sys.executable,'-B','-m','pip','install','--no-index','--no-deps','--no-cache-dir','--disable-pip-version-check','--no-compile','--target',prefix]+[str(p) for p in sorted(Path('/_qh_probe_01/layers/wheels').glob('*.whl'))],capture_output=True,timeout=30,env=env)
result=dict(checkpoint='owned-linux-tls-01',models=0,selected_test_calls=0,install_exit=install.returncode,install_stdout_sha256=hashlib.sha256(install.stdout).hexdigest(),install_stderr_sha256=hashlib.sha256(install.stderr).hexdigest(),project_path=requests.__file__,project_file_sha256=hashlib.sha256(Path(requests.__file__).read_bytes()).hexdigest(),service_prefix=prefix,client_service_packages_absent={n:importlib.util.find_spec(n) is None for n in ('httpbin','flask','werkzeug')})
if install.returncode==0:
 serviceenv=os.environ.copy();serviceenv['PYTHONPATH']=prefix
 process=subprocess.Popen([sys.executable,'-B','/_qh_probe_01/layers/server.py'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=serviceenv,cwd='/tmp',start_new_session=True)
 try:
  with selectors.DefaultSelector() as selector:
   selector.register(process.stdout,selectors.EVENT_READ);assert selector.select(10),'Service ready deadline'
   line=process.stdout.readline();assert line,'Service failed before ready'
  ready=json.loads(line);result['service_ready']=ready
  response=requests.get(ready['url']+'get',params={'control':'owned-linux-service'},timeout=3);payload=response.json()
  result['http']=dict(status=response.status_code,args=payload.get('args'),url=payload.get('url'))
  ca='/_qh_probe_01/layers/certs/cacert.pem';tlsurl=ready['url'].replace('http:','https:')+'get'
  response=requests.get(tlsurl,params={'control':'owned-linux-service'},verify=ca,timeout=3);payload=response.json()
  result['trusted_https']=dict(status=response.status_code,args=payload.get('args'),url=payload.get('url'))
  try:
   requests.get(tlsurl,timeout=3);result['untrusted_tls']=dict(rejected=False)
  except requests.exceptions.SSLError as error:
   text=str(error).lower();result['untrusted_tls']=dict(rejected=True,type=type(error).__name__,verification_message=any(s in text for s in ('certificate verify failed','certificate_verify_failed','self signed')))
  except Exception as error:result['untrusted_tls']=dict(rejected=False,type=type(error).__name__)
  try:
   requests.get(tlsurl.replace('127.0.0.1','127.1'),verify=ca,timeout=3);result['wrong_hostname']=dict(rejected=False)
  except requests.exceptions.SSLError as error:
   text=str(error).lower();result['wrong_hostname']=dict(rejected=True,type=type(error).__name__,hostname_message=('127.1' in text and ('match' in text or 'not valid' in text)))
  except Exception as error:result['wrong_hostname']=dict(rejected=False,type=type(error).__name__)

 except Exception as error:result['service_error']=type(error).__name__
 finally:
  try:stdout,stderr=process.communicate(input=b'\n',timeout=10)
  except subprocess.TimeoutExpired:
   os.killpg(process.pid,signal.SIGTERM)
   try:stdout,stderr=process.communicate(timeout=3)
   except subprocess.TimeoutExpired:os.killpg(process.pid,signal.SIGKILL);stdout,stderr=process.communicate(timeout=3)
   result['forced_cleanup']=True
  result['service_exit']=process.returncode;result['service_stderr_sha256']=hashlib.sha256(stderr).hexdigest()
  result['service_stderr_error_categories']={n:stderr.decode(errors='replace').count(n) for n in ('ModuleNotFoundError','ImportError','TypeError','AttributeError')}
  result['service_cleanup']=json.loads(stdout.splitlines()[-1]) if stdout.splitlines() and stdout.splitlines()[-1].startswith(b'{') else None
print('QH_SERVICE_OBSERVATION');print(json.dumps(result,sort_keys=True))
