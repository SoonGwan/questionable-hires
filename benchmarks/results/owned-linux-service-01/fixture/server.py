import hashlib,importlib.metadata,json,sys,threading
from pathlib import Path
from httpbin import app
import httpbin,flask,werkzeug,markupsafe,markupsafe._speedups
from pytest_httpbin.serve import Handler
from wsgiref.simple_server import make_server
server=make_server('127.0.0.1',0,app,handler_class=Handler);thread=threading.Thread(target=server.serve_forever);thread.start()
try:
 print(json.dumps(dict(url='http://127.0.0.1:%d/'%server.server_address[1],paths={m.__name__:m.__file__ for m in (httpbin,flask,werkzeug,markupsafe)},versions={n:importlib.metadata.version(n) for n in ('httpbin','Flask','Werkzeug','MarkupSafe')},native_extension_path=markupsafe._speedups.__file__,native_extension_sha256=hashlib.sha256(Path(markupsafe._speedups.__file__).read_bytes()).hexdigest())),flush=True)
 sys.stdin.readline()
finally:
 server.shutdown();thread.join(3);server.server_close()
 print(json.dumps(dict(thread_stopped=not thread.is_alive(),socket_closed=server.socket.fileno()==-1)),flush=True)
 assert not thread.is_alive()
