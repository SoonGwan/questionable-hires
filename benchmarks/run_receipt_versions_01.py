"""Six exclusive Receipt development cells; retain every attempt, never retry."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import receipt_versions_cases as fixture

ROOT = Path(__file__).resolve().parents[1]
CURRENT = 'e075bdb'
PREVIOUS = 'efc1439'


def identities():
    paths = ['benchmarks/run_receipt_versions_01.py',
             'benchmarks/run_packaging_specifier_01.py', 'benchmarks/run.py',
             'benchmarks/receipt_versions_cases.py',
             'benchmarks/RECEIPT-VERSIONS-01-PREPARATION.md',
             'tests/test_receipt_versions_cases.py', 'tests/test_receipt_versions_runner.py',
             'tests/test_packaging_specifier_runner.py']
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths}


def validate_preflight():
    selected = ROOT/'skills/receipt/scripts/compare.py'
    pinned = subprocess.check_output(['git', '-C', str(ROOT), 'show',
        CURRENT + ':skills/receipt/scripts/compare.py'], timeout=20)
    if selected.read_bytes() != pinned:
        raise ValueError('Author preflight helper differs from pinned current resource')
    result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover',
        '-s', 'tests', '-p', 'test_receipt_versions_cases.py', '-v'], cwd=ROOT,
        capture_output=True, text=True, timeout=60)
    if result.returncode or 'Ran 2 tests' not in result.stderr:
        raise ValueError('Native fixture preflight failed: ' + result.stderr)
    return dict(python=sys.version, exit_code=result.returncode,
        output=result.stdout + result.stderr, current_revision=CURRENT,
        predecessor_revision=PREVIOUS,
        helper_sha256=hashlib.sha256((ROOT/'skills/receipt/scripts/compare.py').read_bytes()).hexdigest())


def configured_driver():
    spec = importlib.util.spec_from_file_location('_receipt_versions_scheduler',
        ROOT/'benchmarks/run_packaging_specifier_01.py')
    scheduler = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scheduler)
    scheduler.fixture = fixture
    scheduler.RESOURCE = CURRENT
    scheduler.CONDITIONS = ('baseline', 'predecessor', 'current')
    scheduler.SCHEDULE = [(0, 'baseline'), (0, 'predecessor'), (0, 'current'),
                          (1, 'current'), (1, 'predecessor'), (1, 'baseline')]
    scheduler.identities = identities
    scheduler.validate_preflight = validate_preflight
    original_environment = scheduler.environment
    def environment():
        return dict(original_environment(), codex_version=subprocess.check_output(
            ['codex', '--version'], text=True, timeout=20).strip())
    scheduler.environment = environment

    def snapshot(directory):
        if directory.name != 'current':
            raise ValueError('Expected current condition directory')
        for condition, revision in [('current', CURRENT), ('predecessor', PREVIOUS)]:
            destination = directory.parent/condition
            for line in scheduler.git('ls-tree', '-r', revision, '--', 'skills/receipt').decode().splitlines():
                info, name = line.split('\t', 1)
                mode, kind, oid = info.split()
                if kind != 'blob' or mode not in ('100644', '100755'):
                    raise ValueError('Unsupported pinned resource')
                target = destination/name
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open('xb') as stream:
                    stream.write(scheduler.git('cat-file', 'blob', oid))
                target.chmod(int(mode[-3:], 8))
            if not (destination/'skills/receipt/SKILL.md').is_file():
                raise ValueError('Pinned Receipt entrypoint missing')
    scheduler.snapshot = snapshot
    return scheduler


driver = configured_driver()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        driver.execute(output, json.loads((output/'run.json').read_text()))
    else:
        driver.prepare(output)
        print('Prepared six cells; no model calls.')
