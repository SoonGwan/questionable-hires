import json,pathlib,socket,ssl,sys,threading
from httpbin import app
from pytest_httpbin.serve import Handler,Server,ServerHandler
from wsgiref.simple_server import WSGIServer,make_server
import requests
source=pathlib.Path(sys.argv[1]).resolve();certs=pathlib.Path(sys.argv[2])
assert pathlib.Path(requests.__file__).resolve().is_relative_to(source)
context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(str(certs/'cert.pem'),str(certs/'key.pem'))
class DualServer(WSGIServer):
    def finish_request(self,request,address):
        request.settimeout(3)
        if request.recv(1,socket.MSG_PEEK)==b'\x16':
            request=context.wrap_socket(request,server_side=True)
        self.RequestHandlerClass(request,address,self)
rows=[]
for mode,server_class in [('http-only',WSGIServer),('dual-protocol',DualServer)]:
    server=make_server('127.0.0.1',0,app,server_class=server_class,handler_class=Handler)
    thread=threading.Thread(target=server.serve_forever);thread.start()
    port=server.server_address[1]
    try:
        outcomes={}
        for scheme in ['http','https']:
            try:
                response=requests.get('%s://127.0.0.1:%s/get'%(scheme,port),verify=str(certs/'cacert.pem'),timeout=4)
                outcomes[scheme]={'status':response.status_code};response.close()
            except requests.exceptions.SSLError as error:
                outcomes[scheme]={'ssl_error':True,'wrong_version_number':'WRONG_VERSION_NUMBER' in str(error)}
        if mode=='dual-protocol':
            try:
                requests.get('https://127.0.0.1:%s/get'%port,timeout=4)
                outcomes['untrusted_ca_rejected']=False
            except requests.exceptions.SSLError:
                outcomes['untrusted_ca_rejected']=True
        rows.append({'mode':mode,'outcomes':outcomes})
    finally:
        server.shutdown();thread.join(3);server.server_close();assert not thread.is_alive()
print(json.dumps(rows))
assert rows[0]['outcomes']['http']['status']==200
assert rows[0]['outcomes']['https']['wrong_version_number']
assert rows[1]['outcomes']['http']['status']==200
assert rows[1]['outcomes']['https']['status']==200
assert rows[1]['outcomes']['untrusted_ca_rejected']
