import hashlib,http.server,json,os,pathlib,selectors,subprocess,sys,threading,time,urllib.parse
out=pathlib.Path('/tmp/qh-cookie-observations');out.mkdir();prefix=out/'service-prefix';prefix.mkdir();wheels=json.loads(pathlib.Path('/qh/wheels.json').read_text())
for w in wheels:assert hashlib.sha256((pathlib.Path('/qh/wheels')/w['filename']).read_bytes()).hexdigest()==w['sha256']
p=subprocess.run([sys.executable,'-m','pip','install','--no-index','--no-deps','--no-compile','--disable-pip-version-check','--target',str(prefix),*[str(pathlib.Path('/qh/wheels')/w['filename']) for w in wheels]],capture_output=True,timeout=45);(out/'install.stdout').write_bytes(p.stdout);(out/'install.stderr').write_bytes(p.stderr);assert p.returncode==0
sys.path.insert(0,'/testbed');import requests
assert requests.__file__=='/testbed/requests/__init__.py' and hashlib.sha256(pathlib.Path(requests.__file__).read_bytes()).hexdigest()=='364d408838c8073cab46f4846cefaabb03c5b8d18b530c6d8d563f4d6a3920bf'
assert str(prefix) not in sys.path
class CookieHandler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  self.send_response(200)
  if self.path=='/set':self.send_header('Set-Cookie','qh_boundary=present; Path=/')
  if self.path=='/expire':self.send_header('Set-Cookie','qh_boundary=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT')
  self.end_headers();self.wfile.write(json.dumps(dict(cookie=self.headers.get('Cookie'))).encode())
 def log_message(self,*args):pass
server=http.server.HTTPServer(('127.0.0.1',0),CookieHandler);thread=threading.Thread(target=server.serve_forever);thread.start();service=None;rows=[]
try:
 err=(out/'service.stderr').open('wb');service=subprocess.Popen([sys.executable,'-B','/qh/service.py'],env=dict(os.environ,PYTHONPATH=str(prefix)),cwd=out,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err,text=True)
 ready_selector=selectors.DefaultSelector();ready_selector.register(service.stdout,selectors.EVENT_READ);assert ready_selector.select(10),'Service readiness timeout';line=service.stdout.readline();ready_selector.close();ready=json.loads(line);(out/'service-ready.json').write_text(json.dumps(ready,indent=2)+'\n')
 for kind,url in [('stdlib','http://127.0.0.1:%d/'%server.server_address[1]),('httpbin',ready['url'])]:
  with requests.Session() as session:
   first=session.get(url+('set' if kind=='stdlib' else 'cookies/set'),params=None if kind=='stdlib' else {'qh_boundary':'present'},timeout=3);assert first.status_code==200 and session.cookies.get('qh_boundary')=='present'
   normal=session.get(url+('keep' if kind=='stdlib' else 'cookies'),timeout=3);assert normal.status_code==200 and session.cookies.get('qh_boundary')=='present';echo=normal.json();assert ('qh_boundary=present' in echo.get('cookie','') if kind=='stdlib' else echo.get('cookies',{}).get('qh_boundary')=='present')
   expired=session.get(url+('expire' if kind=='stdlib' else 'response-headers'),params=None if kind=='stdlib' else {'Set-Cookie':'qh_boundary=deleted; expires=Thu, 01-Jan-1970 00:00:01 GMT'},timeout=3);assert expired.status_code==200
   rows.append(dict(service=kind,normal_control=True,status=expired.status_code,response_set_cookie=expired.headers.get('Set-Cookie'),raw_set_cookie=[value for key,value in expired.raw._original_response.msg.items() if key.lower()=='set-cookie'],remaining_cookie=session.cookies.get('qh_boundary'),cookie_removed='qh_boundary' not in session.cookies))
finally:
 server.shutdown();thread.join(3);server.server_close();local_cleanup=dict(thread_stopped=not thread.is_alive(),socket_closed=server.socket.fileno()==-1);assert all(local_cleanup.values())
 if service is not None:
  tail,_=service.communicate(input='stop\n',timeout=8);err.close();(out/'service-terminal.stdout').write_text(tail);assert service.returncode==0;service_cleanup=json.loads(tail.strip());assert all(service_cleanup.values())
result=dict(checkpoint='requests2674-cookie-boundary01',requests_version=requests.__version__,requests_path=requests.__file__,python=sys.version,client_service_prefix_absent=True,install_exit=p.returncode,observations=rows,stdlib_cleanup=local_cleanup,httpbin_cleanup=service_cleanup,model_calls=0,selected_issue_tests=0)
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
