#!/usr/bin/env python3
"""Independent mutation oracle; never give its expected results to evaluated agents."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

REVISION = '26d48e0634e6ee9cdc0533996db289ce4b430177'
FAULTS = {
    'wsgi-cleanup': ('httpx/_transports/wsgi.py', '            self._close()', '            pass', 'tests/test_wsgi.py'),
    'asgi-head': ('httpx/_transports/asgi.py', 'if body and request.method != "HEAD":', 'if body:', 'tests/test_asgi.py'),
    'asgi-exceptions': ('httpx/_transports/asgi.py', 'if self.raise_app_exceptions:', 'if False:', 'tests/test_asgi.py'),
}

# These independent checks establish that each mutation changes reachable behavior.
# They are deliberately excluded from every evaluated model's project.
WITNESSES = {
    'wsgi-cleanup': '''import httpx
class Body:
    closed = False
    def __iter__(self):
        yield b"payload"
    def close(self):
        self.closed = True
body = Body()
def app(environ, start_response):
    start_response("200 OK", [])
    return body
with httpx.Client(transport=httpx.WSGITransport(app=app)) as client:
    response = client.get("http://local.test/")
    assert response.content == b"payload"
    assert body.closed, "response iterable close was not called"
print("PASS: actual client response closes application iterable")
''',
    'asgi-head': '''import asyncio
import httpx
async def app(scope, receive, send):
    await send({"type": "http.response.start", "status": 200, "headers": []})
    await send({"type": "http.response.body", "body": b"payload"})
async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        get = await client.get("http://local.test/")
        head = await client.head("http://local.test/")
        assert get.content == b"payload", "GET control must retain body"
        assert head.content == b"", "HEAD exposed application body"
    print("PASS: GET retains body; HEAD suppresses body")
asyncio.run(main())
''',
    'asgi-exceptions': '''import asyncio
import httpx
async def app(scope, receive, send):
    raise RuntimeError("application failure")
async def main():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app)) as client:
        try:
            await client.get("http://local.test/")
        except RuntimeError as error:
            assert str(error) == "application failure"
        else:
            raise AssertionError("default transport swallowed application exception")
    print("PASS: application exception reaches caller")
asyncio.run(main())
''',
}


def witness(python, project, name):
    # Verify the interpreter imports the copy, not an installed package.
    prefix = 'from pathlib import Path; import httpx; assert Path(httpx.__file__).resolve().is_relative_to(Path.cwd().resolve())\n'
    result = subprocess.run([str(python), '-B', '-c', prefix + WITNESSES[name]], cwd=project,
                            text=True, capture_output=True, timeout=30)
    return dict(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)


def run(python, project, test):
    result = subprocess.run([str(python), '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', test], cwd=project,
                            text=True, capture_output=True, timeout=60)
    return dict(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--python', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION or subprocess.check_output(['git', 'status', '--porcelain'], cwd=source, text=True).strip():
        raise ValueError('Expected clean pinned upstream checkout')
    if args.output.exists():
        raise FileExistsError(args.output)
    records = {}
    with tempfile.TemporaryDirectory(prefix='qh-httpx-oracle-') as directory:
        for name, (filename, before, after, test) in FAULTS.items():
            project = Path(directory) / name
            shutil.copytree(source, project, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
            baseline = run(args.python, project, test)
            correct_witness = witness(args.python, project, name)
            if baseline['exit_code'] != 0:
                raise RuntimeError(f'{name}: baseline is not green: {baseline}')
            target = project / filename
            original = target.read_text()
            if original.count(before) != 1:
                raise ValueError(f'{name}: mutation must match exactly once')
            target.write_text(original.replace(before, after))
            mutant = run(args.python, project, test)
            faulty_witness = witness(args.python, project, name)
            records[name] = dict(baseline=baseline, mutant=mutant, correct_witness=correct_witness,
                                 faulty_witness=faulty_witness, file=filename, before=before, after=after)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as handle:
        json.dump(dict(revision=revision, records=records, limitation='Local controlled faults, not naturally occurring upstream bugs; witnesses exercise in-process transports, not deployed networks.'), handle, indent=2)
    for name, record in records.items():
        print(name, 'baseline', record['baseline']['exit_code'], 'mutant', record['mutant']['exit_code'])
        if record['correct_witness']['exit_code'] != 0 or record['faulty_witness']['exit_code'] != 1:
            raise SystemExit(f'{name}: witness failed to distinguish correct and faulty behavior; inspect retained record')


if __name__ == '__main__':
    main()
