import hashlib,json,pathlib,sys
import requests
source=pathlib.Path(sys.argv[1]).resolve();url=sys.argv[2];mode=sys.argv[3];ca=sys.argv[4]
assert pathlib.Path(requests.__file__).resolve().is_relative_to(source)
try:
 if mode=='environment-get':response=requests.get(url,timeout=4)
 else:
  session=requests.Session();prepared=requests.Request('GET',url).prepare()
  if mode=='explicit-send':response=session.send(prepared,verify=ca,timeout=4)
  else:response=session.send(prepared,timeout=4)
 print(json.dumps({'status':response.status_code,'mode':mode,'default_ca_sha256':hashlib.sha256(pathlib.Path(requests.certs.where()).read_bytes()).hexdigest()}));response.close()
except requests.exceptions.SSLError as error:
 print(json.dumps({'ssl_error':True,'mode':mode,'certificate_verification':'CERTIFICATE_VERIFY_FAILED' in str(error),'hostname_mismatch':'hostname' in str(error).lower() or 'doesn' in str(error).lower(),'default_ca_sha256':hashlib.sha256(pathlib.Path(requests.certs.where()).read_bytes()).hexdigest()}));sys.exit(1)
