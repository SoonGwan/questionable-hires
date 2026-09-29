import hashlib,json,os,subprocess,sys
os.chdir('/testbed');sys.path[0]=''
result=dict(checkpoint='owned-official-project-01',cwd=os.getcwd(),executable=sys.executable,prefix=sys.prefix,models=0,external_cases=0)
try:
 import requests
 result['project']=dict(path=requests.__file__,version=requests.__version__,sha256=hashlib.sha256(open(requests.__file__,'rb').read()).hexdigest())
except Exception as error:result['project_error']=type(error).__name__
try:
 child=subprocess.run([sys.executable,'-I','-B','-c','print(6*7)'],capture_output=True,text=True,timeout=10)
 result['child']=dict(exit_code=child.returncode,stdout=child.stdout,stderr_sha256=hashlib.sha256(child.stderr.encode()).hexdigest())
except OSError as error:result['child_error']=dict(type=type(error).__name__,errno=error.errno)
except Exception as error:result['child_error']=dict(type=type(error).__name__)
print('QH_PROJECT_OBSERVATION')
print(json.dumps(result,sort_keys=True))
