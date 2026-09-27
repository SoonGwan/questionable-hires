import subprocess,socket,time,os,signal,sys
s=socket.socket();s.bind(('127.0.0.1',0));port=s.getsockname()[1];s.close();p=subprocess.Popen(['python3','-B','-m','http.server',str(port),'--bind','127.0.0.1','--directory',sys.argv[1]],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
try:
 deadline=time.monotonic()+10
 while True:
  try:
   with socket.create_connection(('127.0.0.1',port),timeout=.1):break
  except OSError:
   if time.monotonic()>deadline:raise TimeoutError('Preview readiness')
   time.sleep(.05)
 c=subprocess.run(['node','/tmp/qh-landing-evidence-01/check.cjs',f'http://127.0.0.1:{port}',sys.argv[2]],env=dict(os.environ,NODE_PATH='/tmp/qh-landing-qa/node_modules'),timeout=50);code=c.returncode
finally:
 p.terminate()
 try:p.wait(timeout=3)
 except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=3)
sys.exit(code)
