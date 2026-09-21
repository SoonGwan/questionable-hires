"""Author-only current retry-decision controls and ancestor evidence; no HTTP/model calls."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = '2458bfcd3dacdf6c196e98d077fc6bb02a5fc1df'
INTRO = 'b6d45c4e702f66e819373c79122944204ebe7e72'
EXTRACT = 'f37a48942be19c019fa9834f9796f354dd1ef2c1'
TARGET = 'src/urllib3/util/retry.py'
METHOD = '        if not self._is_method_retryable(method):\n            return False\n\n'
FORCE = '        if self.status_forcelist and status_code in self.status_forcelist:\n            return True\n\n'
TOTAL = '            self.total\n            and self.respect_retry_after_header'
PROBES = '''import importlib
from pathlib import Path
import unittest
from urllib3.util import Retry

module = importlib.import_module('urllib3.util.retry')
assert Path(module.__file__).resolve() == Path('src/urllib3/util/retry.py').resolve()
assert Retry is module.Retry

class Compatibility(unittest.TestCase):
    def test_method_restriction(self):
        self.assertIs(Retry(total=3, status_forcelist=[500], allowed_methods=['GET']).is_retry('POST', 500), False)

    def test_zero_budget_header(self):
        self.assertIs(Retry(total=0, allowed_methods=['GET']).is_retry('GET', 429, True), False)

    def test_allowed_forced_status(self):
        self.assertIs(Retry(total=3, status_forcelist=[500], allowed_methods=['GET']).is_retry('GET', 500), True)

    def test_positive_budget_header(self):
        self.assertIs(Retry(total=3, allowed_methods=['GET']).is_retry('GET', 429, True), True)

    def test_zero_budget_forced_status(self):
        self.assertIs(Retry(total=0, status_forcelist=[500], allowed_methods=['GET']).is_retry('GET', 500), True)
'''
METHODS = ('method_restriction', 'zero_budget_header', 'allowed_forced_status',
           'positive_budget_header', 'zero_budget_forced_status')


def git(checkout, *args):
    return subprocess.check_output(['git', '-C', str(checkout), *args], timeout=20)


def load_source(checkout):
    if git(checkout, 'rev-parse', 'HEAD').decode().strip() != REVISION:
        raise ValueError('Wrong upstream revision')
    if git(checkout, 'status', '--porcelain=v1') or git(checkout, 'rev-parse', '--is-shallow-repository').strip() != b'false':
        raise ValueError('Requires clean full history')
    files = {}
    for entry in git(checkout, 'ls-tree', '-r', 'HEAD', '--', 'src/urllib3', 'test/test_retry.py', 'LICENSE.txt').decode().splitlines():
        info, name = entry.split('\t', 1)
        mode, kind, oid = info.split()
        path = checkout / name
        if kind != 'blob' or mode != '100644' or path.is_symlink() or not path.is_file():
            raise ValueError('Unexpected upstream entry: ' + name)
        body = path.read_bytes()
        digest = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if digest != oid or path.stat().st_mode & 0o777 != 0o644:
            raise ValueError('Changed upstream file: ' + name)
        files[name] = body
    if TARGET not in files or 'LICENSE.txt' not in files or 'test/test_retry.py' not in files:
        raise ValueError('Missing required source')
    return files


def preflight(checkout):
    files = load_source(checkout)
    source = files[TARGET].decode()
    assert source.count(METHOD + FORCE) == source.count(TOTAL) == 1
    variants = [('current', source, [0, 0, 0, 0, 0]),
        ('forced-status-before-method', source.replace(METHOD + FORCE, FORCE + METHOD, 1), [1, 0, 0, 0, 0]),
        ('omit-total-from-header', source.replace(TOTAL, '            self.respect_retry_after_header', 1), [0, 1, 0, 0, 0])]
    rows = []
    with tempfile.TemporaryDirectory(prefix='urllib3-history-', dir=ROOT / 'benchmarks/local-runs') as folder:
        project = Path(folder)
        for name, body in files.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        (project / 'test_compatibility.py').write_text(PROBES)
        env = dict(os.environ, PYTHONPATH=str(project / 'src'), PYTHONDONTWRITEBYTECODE='1')
        for variant, body, expected in variants:
            (project / TARGET).write_text(body)
            observations = []
            for method, code in zip(METHODS, expected):
                result = subprocess.run([sys.executable, '-B', '-m', 'unittest',
                    'test_compatibility.Compatibility.test_' + method, '-v'], cwd=project, env=env,
                    capture_output=True, text=True, timeout=15)
                output = result.stdout + result.stderr
                assert result.returncode == code and 'Ran 1 test' in output and 'ERROR' not in output, output
                if code:
                    assert 'AssertionError: True is not False' in output, output
                observations.append(dict(method=method, exit_code=result.returncode, output=output))
            rows.append(dict(variant=variant, observations=observations))
    assert not project.exists()
    history = {}
    for commit in (INTRO, EXTRACT):
        git(checkout, 'merge-base', '--is-ancestor', commit, 'HEAD')
        parent = git(checkout, 'show', commit + '^:urllib3/util/retry.py').decode()
        child = git(checkout, 'show', commit + ':urllib3/util/retry.py').decode()
        if commit == INTRO:
            assert 'def is_forced_retry(' in parent and 'self.total and self.respect_retry_after_header' not in parent
            assert 'def is_retry(' in child and 'self.total and self.respect_retry_after_header' in child
        else:
            assert 'def _is_method_retryable(' not in parent and 'def _is_method_retryable(' in child
            assert 'if self.method_whitelist and method.upper() not in self.method_whitelist:' in parent
            assert 'if not self._is_method_retryable(method):' in child
        history[commit] = dict(parent=git(checkout, 'rev-parse', commit + '^').decode().strip(),
            patch=git(checkout, 'show', '--format=%H%n%P%n%s', commit, '--',
                      'urllib3/util/retry.py', 'test/test_retry.py').decode(),
            source_sha256={k: hashlib.sha256(v.encode()).hexdigest() for k, v in [('parent', parent), ('child', child)]})
    assert load_source(checkout) == files
    return dict(revision=REVISION, ancestors=int(git(checkout, 'rev-list', '--count', 'HEAD')),
        python_version=sys.version, license=files['LICENSE.txt'].decode(),
        selected_source_sha256={n: hashlib.sha256(b).hexdigest() for n, b in files.items()},
        controls=rows, history=history,
        limitation='15 author unittest processes, current source/independent modifications only. '
            'Static ancestor evidence; no historical execution, HTTP request, model session, or efficiency claim. '
            'is_retry is a predicate, not proof of an actual network retry; the connection-pool caller also invokes increment.')


if __name__ == '__main__':
    from export import redact_paths
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = preflight(args.checkout.resolve())
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(result, indent=2)) + '\n')
    print('15 native controls and ancestor checks passed; no HTTP/model calls.')
