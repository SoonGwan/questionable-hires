"""Exercise the actual loopback origin handler before public deployment."""
import functools
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('serve_landing', ROOT / 'scripts/serve_landing.py')
origin = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(origin)


class LandingOriginTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.site = self.base / 'site'
        self.site.mkdir()
        (self.site / 'index.html').write_text('<h1>Questionable Hires</h1>')
        (self.site / 'release.json').write_text(json.dumps(dict(app='questionable-hires', revision='test-resource')))
        (self.base / 'outside.txt').write_text('must not be served')
        (self.site / 'linked-secret.txt').symlink_to(self.base / 'outside.txt')
        (self.site / '.private').write_text('hidden')
        (self.site / 'assets').mkdir()
        self.current = self.base / 'current'
        self.current.symlink_to(self.site, target_is_directory=True)
        handler = functools.partial(origin.LandingHandler, directory=self.current)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temporary.cleanup()

    def request(self, path, method='GET'):
        connection = HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        connection.request(method, path)
        response = connection.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        connection.close()
        return result

    def test_health_identifies_the_served_release_and_head_has_no_body(self):
        status, headers, body = self.request('/_health')
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)['revision'], 'test-resource')
        self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
        status, headers, body = self.request('/_health', method='HEAD')
        self.assertEqual(status, 200)
        self.assertEqual(body, b'')
        self.assertGreater(int(headers['Content-Length']), 0)

    def test_files_have_headers_and_no_listing_or_repository_escape(self):
        status, headers, body = self.request('/')
        self.assertEqual(status, 200)
        self.assertIn(b'Questionable Hires', body)
        self.assertEqual(headers['X-Content-Type-Options'], 'nosniff')
        self.assertIn("script-src 'self'", headers['Content-Security-Policy'])
        self.assertEqual(headers['Cache-Control'], 'no-cache')
        for path in ('/assets/', '/.private', '/linked-secret.txt', '/%2e%2e/outside.txt', '/missing'):
            with self.subTest(path=path):
                status, _, body = self.request(path)
                self.assertEqual(status, 404)
                self.assertNotIn(b'must not be served', body)

    def test_unknown_app_identity_is_not_a_healthy_landing(self):
        (self.site / 'release.json').write_text('{"app":"another-app"}')
        self.assertEqual(self.request('/_health')[0], 503)

    def test_release_switch_serves_new_files_without_exposing_parent(self):
        replacement = self.base / 'new-site'
        replacement.mkdir()
        (replacement / 'index.html').write_text('<h1>New release</h1>')
        alternate = self.base / 'new-current'
        alternate.symlink_to(replacement, target_is_directory=True)
        alternate.replace(self.current)
        self.assertIn(b'New release', self.request('/')[2])
        self.assertEqual(self.request('/%2e%2e/outside.txt')[0], 404)


if __name__ == '__main__':
    unittest.main()
