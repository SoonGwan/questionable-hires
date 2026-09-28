import json,sys,threading,importlib.metadata
from httpbin import app
from pytest_httpbin.serve import Handler
from wsgiref.simple_server import make_server
class SchemeHandler(Handler):
 def get_environ(self):
  env=super().get_environ();env['HTTPS']='off';return env
server=make_server('127.0.0.1',0,app,handler_class=SchemeHandler);thread=threading.Thread(target=server.serve_forever);thread.start()
try:
 print(json.dumps(dict(url='http://127.0.0.1:%d/'%server.server_address[1],versions={n:importlib.metadata.version(n) for n in ('httpbin','Flask','Werkzeug','MarkupSafe')})),flush=True)
 sys.stdin.readline()
finally:
 server.shutdown();thread.join(3);server.server_close()
 print(json.dumps(dict(thread_stopped=not thread.is_alive(),socket_closed=server.socket.fileno()==-1)),flush=True)
 assert not thread.is_alive()
