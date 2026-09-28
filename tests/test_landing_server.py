"""Exercise the actual loopback origin handler before public deployment."""
import functools
import hashlib
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

    def request(self, path, method='GET', headers=None):
        connection = HTTPConnection('127.0.0.1', self.server.server_port, timeout=5)
        connection.request(method, path, headers=headers or {})
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

    def test_directory_indexes_cannot_serve_outside_the_release(self):
        directory = self.site / 'linked-index'
        directory.mkdir()
        (directory / 'index.html').symlink_to(self.base / 'outside.txt')
        (self.site / 'index.html').unlink()
        (self.site / 'index.html').symlink_to(self.base / 'outside.txt')
        for path in ('/', '/linked-index/', '/linked-index'):
            for method in ('GET', 'HEAD'):
                with self.subTest(path=path, method=method):
                    status, headers, body = self.request(path, method=method)
                    self.assertNotIn(b'must not be served', body)
                    self.assertEqual(status, 404)
                    self.assertEqual(headers['Cache-Control'], 'no-cache')

    def test_health_cannot_identify_a_manifest_outside_the_release(self):
        outside = self.base / 'outside-release.json'
        outside.write_text(json.dumps(dict(app='questionable-hires', revision='outside-release')))
        (self.site / 'release.json').unlink()
        (self.site / 'release.json').symlink_to(outside)
        for method in ('GET', 'HEAD'):
            with self.subTest(method=method):
                status, headers, body = self.request('/_health', method=method)
                self.assertNotIn(b'outside-release', body)
                self.assertEqual(status, 503)
                self.assertEqual(headers['Cache-Control'], 'no-cache')

    def test_contained_index_and_manifest_links_remain_available(self):
        directory = self.site / 'contained'
        directory.mkdir()
        (directory / 'index.html').symlink_to(self.site / 'index.html')
        manifest = self.site / 'manifest.json'
        (self.site / 'release.json').rename(manifest)
        (self.site / 'release.json').symlink_to(manifest)
        self.assertEqual(self.request('/contained')[0], 301)
        for method in ('GET', 'HEAD'):
            with self.subTest(method=method):
                status, headers, body = self.request('/contained/', method=method)
                self.assertEqual(status, 200)
                self.assertEqual(body, b'<h1>Questionable Hires</h1>' if method == 'GET' else b'')
                self.assertEqual(headers['Cache-Control'], 'no-cache')
                status, _, body = self.request('/_health', method=method)
                self.assertEqual(status, 200)
                if method == 'GET':
                    self.assertEqual(json.loads(body)['revision'], 'test-resource')
                else:
                    self.assertEqual(body, b'')

    def test_only_existing_fingerprinted_artwork_is_immutable(self):
        artwork = b'unchanged image bytes'
        name = 'team-characters.' + hashlib.sha256(artwork).hexdigest() + '.png'
        (self.site / 'assets' / name).write_bytes(artwork)
        status, headers, body = self.request('/assets/' + name)
        self.assertEqual((status, body), (200, artwork))
        self.assertEqual(headers['Cache-Control'], 'public, max-age=31536000, immutable')
        status, conditional, body = self.request('/assets/' + name, headers={
            'If-Modified-Since': headers['Last-Modified']})
        self.assertEqual((status, body), (304, b''))
        self.assertEqual(conditional['Cache-Control'], headers['Cache-Control'])
        status, head, body = self.request('/assets/' + name, method='HEAD')
        self.assertEqual((status, body), (200, b''))
        self.assertEqual(head['Content-Length'], str(len(artwork)))
        (self.site / 'assets/team-characters.png').write_bytes(artwork)
        self.assertEqual(self.request('/assets/team-characters.png')[1]['Cache-Control'], 'no-cache')

    def test_near_length_fingerprints_are_revalidated_for_both_formats(self):
        artwork = b'not a full SHA-256 filename'
        for extension in ('png', 'webp'):
            for length in (63, 65):
                with self.subTest(extension=extension, length=length):
                    name = 'team-characters.' + 'a' * length + '.' + extension
                    (self.site / 'assets' / name).write_bytes(artwork)
                    path = '/assets/' + name
                    status, headers, body = self.request(path)
                    self.assertEqual((status, body), (200, artwork))
                    self.assertEqual(headers['Cache-Control'], 'no-cache')
                    status, conditional, body = self.request(path, headers={
                        'If-Modified-Since': headers['Last-Modified']})
                    self.assertEqual((status, body), (304, b''))
                    self.assertEqual(conditional['Cache-Control'], 'no-cache')
                    status, head, body = self.request(path, method='HEAD')
                    self.assertEqual((status, body), (200, b''))
                    self.assertEqual(head['Content-Length'], str(len(artwork)))
                    self.assertEqual(head['Cache-Control'], 'no-cache')

    def test_missing_or_escaped_fingerprint_never_caches_an_error(self):
        name = 'team-characters.' + 'a' * 64 + '.png'
        for path in ('/assets/' + name, '/assets/%2e%2e/.private', '/_health'):
            status, headers, _ = self.request(path)
            self.assertEqual(headers['Cache-Control'], 'no-cache')
            self.assertEqual(status, 200 if path == '/_health' else 404)

    def test_webp_has_native_media_type_and_immutable_conditional_response(self):
        artwork = b'lossless webp bytes'
        name = 'team-characters.' + hashlib.sha256(artwork).hexdigest() + '.webp'
        status, headers, body = self.request('/assets/' + name)
        self.assertEqual(status, 404)
        self.assertEqual(headers['Cache-Control'], 'no-cache')
        (self.site / 'assets' / name).write_bytes(artwork)
        status, headers, body = self.request('/assets/' + name)
        self.assertEqual((status, body), (200, artwork))
        self.assertEqual({key.lower(): value for key, value in headers.items()}['content-type'], 'image/webp')
        self.assertEqual(headers['Cache-Control'], 'public, max-age=31536000, immutable')
        status, conditional, body = self.request('/assets/' + name, headers={
            'If-Modified-Since': headers['Last-Modified']})
        self.assertEqual((status, body), (304, b''))
        self.assertEqual(conditional['Cache-Control'], headers['Cache-Control'])

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
