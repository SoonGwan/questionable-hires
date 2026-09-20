"""Author-only offline upload replay observations, not a model task or HTTP wire test."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'


def observe(source):
    source = source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION:
        raise ValueError('Expected pinned HTTPX revision')
    if subprocess.check_output(['git', '--no-optional-locks', 'status', '--porcelain'], cwd=source, text=True):
        raise ValueError('Expected clean pinned checkout')
    originals = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in source.rglob('*') if p.is_file() and '.git' not in p.parts}
    sys.path.insert(0, str(source))
    import httpx
    if Path(httpx.__file__).resolve() != source / 'httpx/__init__.py':
        raise ValueError('HTTPX binding is not the selected checkout')

    class OnePass(io.RawIOBase):
        def __init__(self):
            super().__init__()
            self.remaining = b'upload-payload-123'

        def read(self, size=-1):
            if size < 0: size = len(self.remaining)
            chunk, self.remaining = self.remaining[:size], self.remaining[size:]
            return chunk

    check = unittest.TestCase()
    check.maxDiff = None
    outcomes = []
    for mode in ('mock-one-pass', 'stream-one-pass', 'stream-seekable', 'stream-buffered'):
        records = []

        def respond(request, body, before):
            records.append(dict(path=request.url.path, method=request.method,
                stream_before=before, stream_after=type(request.stream).__name__,
                body_hex=body.hex(), body_length=len(body),
                content_length=request.headers.get('content-length'),
                transfer_encoding=request.headers.get('transfer-encoding')))
            return (httpx.Response(307, headers={'location': '/end'})
                    if request.url.path == '/start' else httpx.Response(200))

        class StreamingRecorder(httpx.BaseTransport):
            def handle_request(self, request):
                before = type(request.stream).__name__
                return respond(request, b''.join(request.stream), before)

        def mock_handler(request):
            return respond(request, request.content, type(request.stream).__name__)

        transport = httpx.MockTransport(mock_handler) if mode == 'mock-one-pass' else StreamingRecorder()
        upload = io.BytesIO(b'upload-payload-123') if mode == 'stream-seekable' else OnePass()
        try:
            with httpx.Client(transport=transport) as client:
                request = client.build_request('POST', 'https://example.invalid/start',
                    files={'file': ('upload.bin', upload, 'application/octet-stream')},
                    headers={'Content-Type': 'multipart/form-data; boundary=BOUNDARY'})
                if mode == 'stream-buffered': request.read()
                response = client.send(request, follow_redirects=True)
                check.assertEqual(response.status_code, 200)
                check.assertEqual([r['method'] for r in records], ['POST', 'POST'])
                check.assertEqual([r['path'] for r in records], ['/start', '/end'])
                check.assertEqual([r.status_code for r in response.history], [307])
        finally:
            upload.close()
        bodies = [bytes.fromhex(r['body_hex']) for r in records]
        check.assertIn(b'upload-payload-123', bodies[0])
        equal = bodies[0] == bodies[1]
        check.assertEqual(equal, mode != 'stream-one-pass')
        if mode == 'stream-one-pass':
            check.assertNotIn(b'upload-payload-123', bodies[1])
        for record in records:
            if record['content_length'] is not None:
                check.assertEqual(int(record['content_length']), record['body_length'])
        outcomes.append(dict(mode=mode, records=records, bodies_equal=equal))
    try:
        check.assertEqual(outcomes[1]['records'][0]['body_hex'], outcomes[1]['records'][1]['body_hex'])
    except AssertionError as error:
        negative = str(error)
    else:
        raise AssertionError('False replay-safety claim was not rejected')
    after = {str(p.relative_to(source)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in source.rglob('*') if p.is_file() and '.git' not in p.parts}
    check.assertEqual(originals, after)
    return dict(upstream_revision=revision, imported_module='httpx/__init__.py',
                source_sha256=originals['httpx/__init__.py'], outcomes=outcomes,
                deliberate_assertion_failure=negative, original_files_preserved=True,
                limitation='Author-selected pinned checkout. Real Client, multipart and redirect implementation; custom in-memory transport records stream consumption, not network/wire behavior. No model result or production fix.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(observe(args.source), indent=2))
