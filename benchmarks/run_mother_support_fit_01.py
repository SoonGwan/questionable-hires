"""Four frozen original-task cells; reuse the existing guarded serial scheduler."""
import argparse
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import importlib.util
spec = importlib.util.spec_from_file_location('_mother_support_fit_apps', Path(__file__).with_name('run_all_eight_apps_01.py'))
driver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(driver)
import editor_snapshot_cases
import mother_repeat_cases
import subprocess
import sys
import tempfile
from run_all_eight_current_06 import retain_rules
from mother_support_fit_candidate import entry

ROOT = Path(__file__).resolve().parents[1]
driver.MODELS = {c: 'gpt-6-astra' for c in ('previous', 'candidate')}
driver.FLAGS = {c: [] for c in driver.MODELS}
driver.base.CONDITIONS = tuple(driver.MODELS)
driver.base.RESOURCES = {c: '383820c8' for c in driver.MODELS}
driver.base.SCHEDULE = [(0, 'previous'), (0, 'candidate'), (1, 'candidate'), (1, 'previous')]
original_cases = driver.base.cases
original_snapshot = driver.base.snapshot
original_identities = driver.base.identities
original_frozen = driver.base.frozen
original_cell = driver.base.run.run_cell


def cases():
    selected = [editor_snapshot_cases.cases()[1], mother_repeat_cases.cases()[0]]
    if [c['id'] for c in selected] != ['editor-snapshot-absent', 'repeat-query-qa']:
        raise ValueError('Expected both unchanged Mother tasks')
    return selected


def snapshot(directory, revision):
    original_snapshot(directory, revision)
    if directory.name == 'candidate':
        path = directory / 'skills/mother-in-law/SKILL.md'
        path.write_text(entry(path.read_text()))


def identities():
    result = original_identities()
    for name in ('benchmarks/run_mother_support_fit_01.py',
                 'benchmarks/mother_support_fit_candidate.py',
                 'benchmarks/MOTHER-SUPPORT-FIT-01-PROTOCOL.md',
                 'benchmarks/run_all_eight_current_06.py',
                 'benchmarks/editor_snapshot_cases.py', 'benchmarks/mother_repeat_cases.py',
                 'tests/test_mother_repeat_fixture.py', 'tests/test_mother_support_fit_01.py'):
        result['execution_sources'][name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    return result


def frozen(output):
    return {**original_frozen(output), 'execpolicy_rules': 'retained'}


def run_cell(*args, **kwargs):
    return original_cell(*args, **kwargs, launcher=retain_rules,
                         launcher_execution='host-workspace-write-rules-retained')


driver.base.cases = cases
driver.base.snapshot = snapshot
driver.base.identities = identities
driver.base.frozen = frozen
def preflight():
    editor = editor_snapshot_cases.preflight()
    witness = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
        '-s', 'tests', '-p', 'test_mother_repeat_fixture.py', '-v'], cwd=ROOT,
        text=True, capture_output=True, timeout=30)
    if witness.returncode or 'Ran 3 tests' not in witness.stderr:
        raise RuntimeError('Repeated-query witness preflight failed: ' + witness.stderr)
    with tempfile.TemporaryDirectory(prefix='mother-fit-native-', dir=ROOT / 'benchmarks') as temporary:
        root = Path(temporary)
        for name, body in mother_repeat_cases.FILES.items():
            (root / name).write_text(body)
        code = "import pathlib, search, unittest; assert pathlib.Path(search.__file__).resolve().parent == pathlib.Path.cwd().resolve(); unittest.main(module='test_search', verbosity=2)"
        native = subprocess.run([sys.executable, '-B', '-c', code], cwd=root,
            text=True, capture_output=True, timeout=20)
        if native.returncode or 'Ran 1 test' not in native.stderr:
            raise RuntimeError('Fresh project import/initial native test failed: ' + native.stderr)
    return dict(editor=editor, repeated_query_witness=dict(exit_code=witness.returncode,
        stdout=witness.stdout, stderr=witness.stderr), repeated_query_native=dict(
        exit_code=native.returncode, stdout=native.stdout, stderr=native.stderr),
        limitation='Author preflight only, not model or efficiency evidence.')


driver.base.controls = SimpleNamespace(check=preflight)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        with patch.object(driver.base.run, 'run_cell', new=run_cell):
            driver.execute(output, json.loads((output / 'run.json').read_text()))
    else:
        driver.base.prepare(output)
        print('Prepared four changed-resource Mother cells; no model calls.')
