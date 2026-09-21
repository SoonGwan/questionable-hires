"""Author controls for a real Click test gap; no model result or upstream fix."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

REVISION = '6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1'
ANCHOR = '        exit_result = self._exit_stack.__exit__(exc_type, exc_value, tb)'
MUTATION = '''        pending_count = len(self._exit_stack._exit_callbacks)
        exit_result = self._exit_stack.__exit__(exc_type, exc_value, tb)
        if pending_count > 1 and exc_value is not None and not exit_result:
            exit_result = True'''
ORACLE = '''import click
import pytest
from pathlib import Path

@pytest.mark.parametrize('count,suppress', [(2,False),(1,False),(2,True)])
def test_real_nested_exit(count, suppress):
    assert Path(click.__file__).resolve() == Path(__file__).resolve().parents[1] / 'src/click/__init__.py'
    calls = []
    error = RuntimeError('body-failure-sentinel')
    class Resource:
        def __init__(self, name): self.name = name
        def __enter__(self): return self
        def __exit__(self, typ, value, tb):
            calls.append((self.name, value is error, value is None))
            return suppress
    caught = None
    ctx = click.Context(click.Command('test'))
    try:
        with ctx.scope():
            for index in range(count): ctx.with_resource(Resource(index))
            raise error
    except RuntimeError as exc:
        caught = exc
    finally:
        ctx.close()
    print('OBSERVED', count, suppress, calls, 'propagated', caught is error)
    assert (caught is error) == (not suppress)
    expected = [(i, not suppress or i == count-1, suppress and i != count-1)
                for i in reversed(range(count))]
    assert calls == expected
'''


def inventory(root):
    return {str(p.relative_to(root)): (p.stat().st_mode & 0o777, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in root.rglob('*') if p.is_file()}


def observe(source):
    source = source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION or subprocess.check_output(['git', '--no-optional-locks', 'status', '--porcelain'], cwd=source):
        raise ValueError('Expected clean pinned Click checkout')
    original = inventory(source)
    outcomes = []
    with tempfile.TemporaryDirectory(prefix='click-context-', dir=Path(__file__).resolve().parent) as scratch:
        for variant in ('correct', 'faulty'):
            copied = Path(scratch) / variant
            shutil.copytree(source, copied, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
            implementation = copied / 'src/click/core.py'
            text = implementation.read_text()
            assert text.count(ANCHOR) == 1
            if variant == 'faulty': implementation.write_text(text.replace(ANCHOR, MUTATION))
            (copied / 'tests/test_author_context.py').write_text(ORACLE)
            env = dict(os.environ, PYTHONPATH=str(copied / 'src'), PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
            for suite in ('tests/test_context.py', 'tests/test_author_context.py'):
                command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', suite]
                result = subprocess.run(command, cwd=copied, env=env, capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                expected = int(variant == 'faulty' and suite.endswith('test_author_context.py'))
                assert result.returncode == expected, output
                assert ('1 failed, 2 passed' if expected else '30 passed' if suite.endswith('/test_context.py') else '3 passed') in output, output
                outcomes.append(dict(variant=variant, suite=suite, exit_code=result.returncode,
                                     output=output.replace(str(copied), '<COPY>')))
    assert inventory(source) == original
    return dict(upstream_revision=revision, outcomes=outcomes, originals_preserved=True,
                limitation='Author-selected upstream test gap and synthetic mutation; not an organic production bug, model score or performance result.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(observe(args.source), indent=2))
