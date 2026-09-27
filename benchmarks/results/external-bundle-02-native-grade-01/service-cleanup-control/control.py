import json,threading,urllib.request
from httpbin import app
from pytest_httpbin.serve import Server
server=Server(application=app)
server.start()
try:
    with urllib.request.urlopen(server.url + '/get', timeout=2) as response:
        assert response.status == 200
        assert json.loads(response.read())['url'] == server.url + '/get'
finally:
    server.stop()
    threading.Thread.join(server, 2)
    assert not server.is_alive()
    server._server.server_close()
print('HTTP200_AND_NATIVE_THREAD_CLEANUP_PASS')
