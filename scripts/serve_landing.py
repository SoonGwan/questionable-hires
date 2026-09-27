#!/usr/bin/env python3
"""Serve only a generated landing release, on loopback, behind Cloudflare Tunnel."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class LandingHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory, **kwargs):
        # Resolve the current-release symlink once per request.
        self.root = Path(directory).resolve()
        super().__init__(*args, directory=str(self.root), **kwargs)

    def send_response(self, code, message=None):
        self.response_status = code
        super().send_response(code, message)

    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Referrer-Policy', 'strict-origin-when-cross-origin')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'")
        immutable = getattr(self, 'immutable_artwork', False) and self.response_status in (200, 304)
        self.send_header('Cache-Control', 'public, max-age=31536000, immutable' if immutable else 'no-cache')
        super().end_headers()

    def send_head(self):
        self.immutable_artwork = False
        path = unquote(urlsplit(self.path).path)
        if path == '/_health':
            try:
                payload = (self.root / 'release.json').read_bytes()
                if json.loads(payload).get('app') != 'questionable-hires':
                    raise ValueError('Unknown app identity')
            except (OSError, ValueError):
                self.send_error(503)
                return None
            from io import BytesIO
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            return BytesIO(payload)
        if '..' in path.split('/') or '\\' in path or any(part.startswith('.') for part in path.split('/') if part):
            self.send_error(404)
            return None
        try:
            target = (self.root / path.lstrip('/')).resolve()
            target.relative_to(self.root)
        except (ValueError, OSError):
            self.send_error(404)
            return None
        if target.is_dir() and not (target / 'index.html').is_file():
            self.send_error(404)
            return None
        self.immutable_artwork = bool(target.is_file() and re.fullmatch(
            r'/assets/team-characters\.[0-9a-f]{64}\.(?:png|webp)', path))
        return super().send_head()

    def list_directory(self, path):
        self.send_error(404)
        return None

    def log_message(self, format, *args):
        # Do not retain visitor query strings in the static origin log.
        print(f'{self.log_date_time_string()} {self.command} {urlsplit(self.path).path}', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory', type=Path, required=True)
    parser.add_argument('--port', type=int, default=4180)
    args = parser.parse_args()
    if not (args.directory / 'index.html').is_file():
        parser.error('directory must contain a generated landing index.html')
    handler = functools.partial(LandingHandler, directory=args.directory)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    print(f'Questionable Hires listening at http://127.0.0.1:{args.port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
