"""Native author controls before any model sees the new JSON comparison task."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from httpx_receipt_json_case import HEAD, BEFORE, AFTER, TESTS

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refuse existing output')
    source = args.source.resolve()
    def git(*args):
        return subprocess.check_output(['git', *args], cwd=source, text=True).strip()
    assert git('rev-parse', 'HEAD') == HEAD and not git('status', '--porcelain')
    assert git('rev-parse', AFTER + '^') == BEFORE
    names = git('ls-files').splitlines()
    def inventory():
        return {n: dict(sha256=hashlib.sha256((source/n).read_bytes()).hexdigest(),
                        mode=(source/n).stat().st_mode & 0o777) for n in names}
    before = inventory()
    module_spec = importlib.util.spec_from_file_location('receipt', ROOT/'skills/receipt/scripts/compare.py')
    helper = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(helper)
    fixed = [n for n in names if n.startswith('httpx/') and n != 'httpx/_content.py']
    fixed += ['pyproject.toml', 'tests/__init__.py', 'tests/conftest.py',
              'tests/concurrency.py', 'tests/test_content.py']
    recipe = dict(fixed=fixed, vary=['httpx/_content.py'], before=BEFORE, after=AFTER,
                  imports=['httpx', 'httpx._content'], runner='pytest',
                  tests=['-vv', '-p', 'no:cacheprovider', *TESTS])
    with tempfile.TemporaryDirectory(prefix='json-commit-preflight-', dir=ROOT/'benchmarks/local-runs') as temporary:
        project = Path(temporary)/'project'
        shutil.copytree(source, project)
        result = helper.compare(project, recipe, python=str(args.python.absolute()))
        assert result['status'] == 'observed', result
        original, fixed_result = result['checks']['before'], result['checks']['after']
        assert original['exit_code'] == 1 and fixed_result['exit_code'] == 0, result
        assert '4 failed, 1 passed' in original['output'], original
        assert '5 passed' in fixed_result['output'], fixed_result
        assert 'DID NOT RAISE' in original['output'], original
        assert "'19'" in original['output'] and "'18'" in original['output'], original
        assert 'Verified copied import: httpx._content' in original['output']
        assert 'Verified copied import: httpx._content' in fixed_result['output']
        assert not original['output_truncated'] and not fixed_result['output_truncated']
        assert result['originals']['unchanged'] and result['comparison_copies_removed']
        encoded = (json.dumps(result, indent=2).replace(str(project), '<AUTHOR_COPY>')
                   .replace(str(args.python.absolute()), '<PREINSTALLED_PYTHON>'))
    assert inventory() == before and not git('status', '--porcelain')
    report = dict(source_revision=HEAD, source_inventory=before, tests=list(TESTS),
                  recipe=recipe, observation=json.loads(encoded),
                  source_unchanged=True, author_copy_removed=not Path(temporary).exists(),
                  limitation='Native author preflight only; real upstream source/commit, current support held fixed. Not a model result or full historical environment recreation.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in ('source_revision','tests','source_unchanged','author_copy_removed')}))


if __name__ == '__main__':
    main()
