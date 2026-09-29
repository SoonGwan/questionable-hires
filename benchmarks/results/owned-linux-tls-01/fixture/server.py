import socket,ssl,hashlib,importlib.metadata,json,sys,threading
from pathlib import Path
from httpbin import app
import httpbin,flask,werkzeug,markupsafe,markupsafe._speedups
from pytest_httpbin.serve import Handler
from wsgiref.simple_server import make_server,WSGIServer
context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/_qh_probe_01/layers/certs/cert.pem','/_qh_probe_01/layers/certs/key.pem')
class DualServer(WSGIServer):
 def finish_request(self,request,address):
  request.settimeout(3)
  if request.recv(1,socket.MSG_PEEK)==b'\x16':request=context.wrap_socket(request,server_side=True)
  self.RequestHandlerClass(request,address,self)
class SchemeHandler(Handler):
 def get_environ(self):
  env=super().get_environ();env['HTTPS']='on' if isinstance(self.request,ssl.SSLSocket) else 'off';return env
server=make_server('127.0.0.1',0,app,server_class=DualServer,handler_class=SchemeHandler);thread=threading.Thread(target=server.serve_forever);thread.start()
try:
 print(json.dumps(dict(url='http://127.0.0.1:%d/'%server.server_address[1],paths={m.__name__:m.__file__ for m in (httpbin,flask,werkzeug,markupsafe)},versions={n:importlib.metadata.version(n) for n in ('httpbin','Flask','Werkzeug','MarkupSafe')},native_extension_path=markupsafe._speedups.__file__,native_extension_sha256=hashlib.sha256(Path(markupsafe._speedups.__file__).read_bytes()).hexdigest())),flush=True)
 sys.stdin.readline()
finally:
 server.shutdown();thread.join(3);server.server_close()
 print(json.dumps(dict(thread_stopped=not thread.is_alive(),socket_closed=server.socket.fileno()==-1)),flush=True)
 assert not thread.is_alive()
