import http.server, pathlib, sys, threading, unittest
import requests
root=pathlib.Path.cwd().resolve()
assert pathlib.Path(requests.__file__).resolve().is_relative_to(root)
payload=b"\x00\xffnative-response"
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
    def log_message(self, *args): pass
class Transport(unittest.TestCase):
    def test_actual_source_reads_exact_binary_response(self):
        server=http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread=threading.Thread(target=server.serve_forever, kwargs={'poll_interval':0.01}, daemon=True)
        thread.start()
        try:
            response=requests.get('http://127.0.0.1:%d/'%server.server_address[1], timeout=2)
            try:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content, payload if sys.argv[1]=='pass' else b'wrong payload')
            finally: response.raw.release_conn()
        finally:
            server.shutdown();server.server_close();thread.join(timeout=2)
            self.assertFalse(thread.is_alive())
unittest.main(argv=['native-http-control'], verbosity=2)
