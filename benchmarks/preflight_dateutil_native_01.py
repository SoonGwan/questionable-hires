"""Author-only real-source audit controls; no model calls or performance score."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = '1ae807774053c071acc9e7d3d27778fba0a7773e'
BLOBS = {
    'AUTHORS.md': '793a2fd59586c099e4db9475b79d92c8427363fa',
    'LICENSE': '1e65815cf0b3132689485874a93034ede7206bf4',
    'src/dateutil/__init__.py': 'a2c19c06fe14476a9bfa4f1f60de7a997a41191c',
    'src/dateutil/_common.py': '4eb2659bd2986125fcfb4afea5bae9efc2dcd1a0',
    'src/dateutil/relativedelta.py': 'cd323a549e0f182541ebcde2d2ea1adfbbd9701e',
    'tests/__init__.py': 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
    'tests/_common.py': 'b8d20473743bfbdc0968578e2b79b201b79512fb',
    'tests/test_relativedelta.py': '5204c293b7c0a318a75f6ff6395bdc1f9a517ae0',
}
TARGET = 'src/dateutil/relativedelta.py'
PREFIX = 'tests.test_relativedelta.RelativeDeltaTest.'
SELECTORS = [PREFIX + 'testNextMonth', PREFIX + 'testNextFriday']
FAULTS = [
    ('february-cap', 'day = min(calendar.monthrange(year, month)[1],',
     'day = min(28,', 'testLastDayOfFebruaryLeapYear', [0, 0]),
    ('strict-next-weekday', '(7 - ret.weekday() + weekday) % 7',
     '((7 - ret.weekday() + weekday) % 7 or 7)', 'testNextWednesdayIsToday', [0, 0]),
    ('omit-relative-month', 'month += self.months',
     'month += 0', 'testNextMonth', [1, 0]),
]


def load_source(checkout):
    if subprocess.check_output(['git', '-C', str(checkout), 'rev-parse', 'HEAD'], text=True).strip() != REVISION:
        raise ValueError('Wrong upstream revision')
    files = {}
    for name, expected in BLOBS.items():
        path = checkout / name
        if path.is_symlink() or not path.is_file():
            raise ValueError('Not a regular upstream file: ' + name)
        body = path.read_bytes()
        blob = hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        if blob != expected:
            raise ValueError('Changed upstream file: ' + name)
        files[name] = body
    return files


def inventory(root):
    return {str(p.relative_to(root)): (hashlib.sha256(p.read_bytes()).hexdigest(),
            p.stat().st_mode & 0o777) for p in root.rglob('*') if p.is_file()}


def preflight(checkout):
    files = load_source(checkout)
    rows = []
    with tempfile.TemporaryDirectory(prefix='dateutil-preflight-', dir=ROOT / 'benchmarks/local-runs') as folder:
        project = Path(folder)
        for name, body in files.items():
            path = project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        original = inventory(project)
        env = dict(os.environ, PYTHONPATH=str(project / 'src'), PYTHONDONTWRITEBYTECODE='1')
        source = files[TARGET].decode()

        def execute(selector, expected):
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', selector, '-v'],
                cwd=project, env=env, text=True, capture_output=True, timeout=20)
            output = result.stdout + result.stderr
            if (result.returncode != expected or 'Ran ' not in output or 'ERROR' in output
                    or (expected == 1 and 'AssertionError:' not in output)):
                raise AssertionError(output)
            return dict(selector=selector, exit_code=result.returncode, output=output)

        variants = [('correct', None, None, None, [0, 0]), *FAULTS,
                    ('equivalent', 'month += self.months', 'month = month + self.months', None, [0, 0])]
        for name, old, new, witness, expected in variants:
            if old is not None and source.count(old) != 1:
                raise AssertionError('Ambiguous patch: ' + name)
            (project / TARGET).write_text(source if old is None else source.replace(old, new, 1))
            selected = [execute(selector, code) for selector, code in zip(SELECTORS, expected)]
            witnesses = [execute(PREFIX + fault[3], int(fault[0] == name)) for fault in FAULTS]
            rows.append(dict(variant=name, selected=selected, witnesses=witnesses))
        (project / TARGET).write_bytes(files[TARGET])
        assert inventory(project) == original
        # Same unchanged upstream test bodies through the optional production helper.
        recipe = dict(files=list(files), imports=['dateutil.relativedelta', 'tests.test_relativedelta'],
            import_roots=['src'], runner='unittest', invocation='module', tests=[SELECTORS[0], '-v'],
            precheck="import importlib\nr = importlib.import_module('dateutil.relativedelta')\n"
                     "t = importlib.import_module('tests.test_relativedelta')\n"
                     "assert t.relativedelta is r.relativedelta\nprint('copied binding verified', flush=True)\n",
            mutations=[dict(target=TARGET, old=old, new=new, tests=[selector, '-v'])
                       for _, old, new, _, _ in FAULTS for selector in SELECTORS])
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'skills/con-artist/scripts/audit.py'),
            '--source', str(project), '--spec', '-'], input=json.dumps(recipe),
            text=True, capture_output=True, timeout=60)
        if result.returncode != 0:
            raise AssertionError(result.stderr + result.stdout)
        report = json.loads(result.stdout)
        assert report['status'] == 'observed'
        for index, audit in enumerate(report['audits']):
            correct = audit['checks']['correct_tests']
            if index < 2:
                assert correct['exit_code'] == 0
            else:
                assert correct['observation_ref'] == '#/audits/{}/checks/correct_tests'.format(index % 2)
            check = audit['checks']['mutant_tests']
            expected = FAULTS[index // 2][4][index % 2]
            assert check['exit_code'] == check['native_exit_code'] == expected
            assert check['suite_observation'] == dict(tests=1, skipped=0, successful=not expected)
            assert 'copied binding verified' in check['output']
            assert 'ERROR' not in check['output']
            if expected:
                assert 'AssertionError:' in check['output']
            assert audit['integrity']['owned_scratch_removed']
        assert inventory(project) == original
        assert set(p.name for p in project.iterdir()) == {'LICENSE', 'AUTHORS.md', 'src', 'tests'}
    assert not project.exists()
    return dict(upstream_revision=REVISION, upstream_blob_ids=BLOBS, python=sys.version,
        dependencies={n: importlib.metadata.version(n) for n in ('pytest', 'six', 'iniconfig', 'packaging', 'pluggy')},
        direct_controls=rows, helper_report=report, scratch_removed=True,
        limitation='Selected unchanged upstream files/tests, author-chosen mutations and selections. '
                   '25 direct controls plus 8 helper executions. Not a whole-project suite, model measurement or holdout.')


if __name__ == '__main__':
    from export import redact_paths
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkout', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    observations = preflight(args.checkout.resolve())
    with args.output.open('x') as stream:
        stream.write(redact_paths(json.dumps(observations, indent=2)) + '\n')
    print('Native upstream controls and helper parity passed; no model calls.')
