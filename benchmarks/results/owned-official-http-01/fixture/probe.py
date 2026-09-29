import hashlib,importlib,json,os,sys,threading
from http.server import BaseHTTPRequestHandler,HTTPServer
os.chdir('/testbed');sys.path[0]=''
import requests
result=dict(checkpoint='owned-official-http-01',models=0,selected_test_calls=0,project_path=requests.__file__,project_file_sha256=hashlib.sha256(open(requests.__file__,'rb').read()).hexdigest(),dependencies={})
for name in ('httpbin','pytest_httpbin','flask','werkzeug','mock'):
 try:
  module=importlib.import_module(name);result['dependencies'][name]=dict(imported=True,path=getattr(module,'__file__',None),version=getattr(module,'__version__',None))
 except Exception as error:result['dependencies'][name]=dict(imported=False,error_type=type(error).__name__)
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  body=b'QH_OFFICIAL_HTTP_OK';self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def log_message(self,*args):pass
server=HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever);thread.start()
try:
 response=requests.get('http://127.0.0.1:%d/health'%server.server_address[1],timeout=3)
 result['http']=dict(status=response.status_code,body=response.text)
except Exception as error:result['http']=dict(error_type=type(error).__name__)
finally:
 server.shutdown();thread.join(3);server.server_close();result['cleanup']=dict(thread_stopped=not thread.is_alive(),socket_closed=server.socket.fileno()==-1)
print('QH_HTTP_OBSERVATION');print(json.dumps(result,sort_keys=True))
