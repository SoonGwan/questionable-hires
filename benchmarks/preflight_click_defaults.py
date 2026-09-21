"""Native author controls for a Click default-resolution design proposal."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from preflight_click_context import REVISION, inventory

REPLACEMENTS = [
    ('if value is None and not ctx._default_map_has(self.name):', 'if value is None:'),
    ('if default_map_value is not None or ctx._default_map_has(self.name):',
     'if default_map_value is not None:'),
]
ORACLE = '''import json
from pathlib import Path
import click
from click._utils import UNSET
from click.testing import CliRunner
import pytest

@pytest.mark.parametrize('label,argv,env,mapping,expected,calls_expected', [
    ('cli', ['--name','cli'], 'env', {'name':None}, ['cli','COMMANDLINE'], 0),
    ('env', [], 'env', {'name':None}, ['env','ENVIRONMENT'], 0),
    ('none', [], None, {'name':None}, [None,'DEFAULT_MAP'], 0),
    ('empty', [], None, {'name':''}, ['','DEFAULT_MAP'], 0),
    ('zero', [], None, {'name':0}, ['0','DEFAULT_MAP'], 0),
    ('missing', [], None, {}, ['fallback','DEFAULT'], 0),
    ('unset', [], None, {'name':UNSET}, ['fallback','DEFAULT'], 0),
    ('callable-none', [], None, None, [None,'DEFAULT_MAP'], 1),
])
def test_actual_cli(label, argv, env, mapping, expected, calls_expected):
    assert Path(click.__file__).resolve() == Path(__file__).resolve().parents[1] / 'src/click/__init__.py'
    calls = []
    def factory():
        calls.append('called')
        return None
    if mapping is None:
        mapping = {'name':factory}
    @click.command()
    @click.option('--name', default='fallback', envvar='QH_REVIEW_NAME')
    @click.pass_context
    def cli(ctx, name):
        click.echo(json.dumps([name, ctx.get_parameter_source('name').name]))
    result = CliRunner().invoke(cli, argv, env={'QH_REVIEW_NAME':env}, default_map=mapping)
    assert result.exit_code == 0, (result.output, result.exception)
    actual = json.loads(result.output)
    print('OBSERVED', label, actual, 'factory_calls', len(calls))
    assert actual == expected
    assert len(calls) == calls_expected
'''


def observe(source):
    source = source.resolve()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if revision != REVISION or subprocess.check_output(['git', '--no-optional-locks', 'status', '--porcelain'], cwd=source):
        raise ValueError('Expected clean pinned Click source')
    before = inventory(source)
    rows = []
    with tempfile.TemporaryDirectory(prefix='click-defaults-', dir=Path(__file__).resolve().parent) as scratch:
        for variant in ('correct', 'proposal'):
            copied = Path(scratch) / variant
            shutil.copytree(source, copied, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache'))
            core = copied / 'src/click/core.py'
            body = core.read_text()
            for old, new in REPLACEMENTS:
                assert body.count(old) == 1
                if variant == 'proposal':
                    body = body.replace(old, new)
            if variant == 'proposal': core.write_text(body)
            (copied / 'tests/test_author_defaults.py').write_text(ORACLE)
            env = dict(os.environ, PYTHONPATH=str(copied / 'src'), PYTHONDONTWRITEBYTECODE='1', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
            suites = [
                ['tests/test_defaults.py::test_default_map_source', 'tests/test_defaults.py::test_lookup_default_callable_in_default_map'],
                ['tests/test_author_defaults.py'],
            ]
            for index, suite in enumerate(suites):
                command = [sys.executable, '-B', '-m', 'pytest', '-q', '-s', '-p', 'no:cacheprovider', *suite]
                result = subprocess.run(command, cwd=copied, env=env, capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                assert result.returncode == int(variant == 'proposal'), output
                expected = ('7 passed' if index == 0 else '8 passed') if variant == 'correct' else ('1 failed, 6 passed' if index == 0 else '2 failed, 6 passed')
                assert expected in output, output
                if variant == 'proposal': assert 'AssertionError' in output, output
                rows.append(dict(variant=variant, suite=suite, exit_code=result.returncode,
                                 output=output.replace(str(copied), '<COPY>')))
    assert inventory(source) == before
    return dict(upstream_revision=revision, outcomes=rows, originals_preserved=True,
                limitation='Author-selected proposal over real source, not a model result or organic upstream issue. Existing source is unchanged.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(observe(args.source), indent=2))
