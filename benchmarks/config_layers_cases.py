"""Authored configuration audit inputs and native author preflight, not model evidence."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = '''def resolve(defaults, environment, overrides):
    result = dict(defaults)
    for layer in (environment, overrides):
        for key, value in layer.items():
            if value is not None:
                result[key] = value
    return result
'''
TESTS = '''import unittest
from settings import resolve

class SettingsTests(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(resolve({'retries': 3}, {}, {}), {'retries': 3})
    def test_environment(self):
        self.assertEqual(resolve({'retries': 3}, {'retries': 4}, {}), {'retries': 4})
    def test_override(self):
        self.assertEqual(resolve({'retries': 3}, {}, {'retries': 5}), {'retries': 5})
    def test_absent_override(self):
        self.assertEqual(resolve({'retries': 3}, {}, {'retries': None}), {'retries': 3})
'''
STRONG = TESTS + '''
    def test_layer_interactions_and_preservation(self):
        defaults = {'enabled': True, 'retries': 3, 'region': 'eu', 'label': 'default'}
        environment = {'enabled': False, 'retries': 0, 'region': 'us', 'label': ''}
        overrides = {'region': 'ap', 'retries': None}
        before = [dict(layer) for layer in (defaults, environment, overrides)]
        self.assertEqual(resolve(defaults, environment, overrides),
                         {'enabled': False, 'retries': 0, 'region': 'ap', 'label': ''})
        self.assertEqual([defaults, environment, overrides], before)
'''
FILES = {'settings.py': SOURCE, 'test_settings.py': TESTS}
MUTATIONS = [
    dict(target='settings.py', old='(environment, overrides)', new='(overrides, environment)'),
    dict(target='settings.py', old='if value is not None:', new='if value:'),
    dict(target='settings.py', old='result = dict(defaults)', new='result = defaults'),
    dict(target='settings.py', old='if value is not None:', new='if True:'),
]
PRECHECK = ('import settings, test_settings\n'
            'assert test_settings.resolve is settings.resolve\n')
TASK = '''Audit the supplied configuration resolver's existing native tests against
the requested independent replacements below. Contract: defaults are overridden
by environment, then explicit overrides. None means absent. False, zero and empty
strings remain explicit values. None of the three input mappings may change.
There is no parsing, type coercion or unknown-key rejection requirement.

Run the original unchanged test_settings suite on correct code and each isolated
fault in project-local disposable copies, using the supplied Python's unittest
runner. Verify copy-local settings/test_settings paths and their resolve binding
inside every actual native test process. An import-only preliminary check is not
same-process proof. Report native counts, exits and actual assertion values or
survival; import/setup/empty-suite failures are not detection.

For each survivor, add a focused native regression assertion in a disposable
copy, preserving every existing assertion, and verify the same assertion passes
correct code and fails that fault. No added assertion is required for a fault
already detected by the original suite. Reuse a successful correct observation
only while its inputs, runtime and relevant state remain identical; label reuse
instead of counting it as another execution. Choose your own implementation;
no particular helper or grouping is required.

Keep source/test bytes and modes, Git HEAD/index and supplied skill resources
unchanged. Remove owned scratch, including failure paths, leaving no permanent
harness/report. Work only within this project; no network, installation,
external-project search, delegation, Git mutation or publication. Report unknowns
honestly. These are authored development inputs, not production incident data.
'''
CRITERIA = [
    'Copy-local module/test binding verified in every actual native test process.',
    'Unchanged original suite passes correct code and runs every isolated requested fault.',
    'Detection/survival uses native counts, exits and actual assertions, not support errors.',
    'Every survivor has a native stronger assertion passing correct code and rejecting it unchanged.',
    'Original bytes/modes/Git/resources preserved, owned scratch removed, project-only scope kept.',
]


def cases(python):
    if not Path(python).is_absolute():
        raise ValueError('Supply an absolute preinstalled interpreter path')
    return [dict(id='config-layers-' + label, skill='con-artist', files=dict(FILES),
                 task=TASK + '\nIndependent replacements:\n' + json.dumps(MUTATIONS[:count], indent=2)
                      + '\nPreinstalled Python: ' + str(python), criteria=list(CRITERIA))
            for label, count in [('single', 1), ('multiple', 4)]]


def preflight():
    script = ROOT / 'skills/con-artist/scripts/audit.py'
    spec = importlib.util.spec_from_file_location('config_audit', script)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    for mutation in MUTATIONS:
        if SOURCE.count(mutation['old']) != 1:
            raise ValueError('Ambiguous declared mutation')
    report = dict(kind='author native preflight, not model evidence', python=sys.version,
                  helper_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                  fixture_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), cases={})
    with tempfile.TemporaryDirectory(prefix='config-layers-', dir=ROOT / 'benchmarks') as directory:
        root = Path(directory)
        for name, content in FILES.items():
            (root / name).write_text(content)
            (root / name).chmod(0o644)
        original = {p.name: (p.read_bytes(), p.stat().st_mode) for p in root.iterdir()}
        fresh = subprocess.run([sys.executable, '-I', '-B', '-c',
            'import sys;sys.path.insert(0,".");import settings;'
            'assert settings.resolve({"v":1},{},{}) == {"v":1};print("fresh public import passed")'],
            cwd=root, capture_output=True, text=True, timeout=10)
        if fresh.returncode != 0:
            raise RuntimeError(fresh.stderr)
        report['fresh_import'] = dict(exit_code=fresh.returncode, output=fresh.stdout)
        for label, count in [('single', 1), ('multiple', 4)]:
            recipe = dict(files=list(FILES), imports=['settings', 'test_settings'],
                          tests=['-v', 'test_settings'], precheck=PRECHECK,
                          mutations=[dict(fault, probe_replacements={'test_settings.py': STRONG},
                                          probe_tests=['-v', 'test_settings'], probe_when='survives')
                                     for fault in MUTATIONS[:count]])
            observed = helper.audit_batch(root, recipe, timeout=10)
            if observed['status'] != 'observed' or len(observed['audits']) != count:
                raise AssertionError('Incomplete author controls')
            for index, audit in enumerate(observed['audits']):
                checks = audit['checks']
                expected = 1 if index == 3 else 0
                if checks['mutant_tests']['exit_code'] != expected:
                    raise AssertionError('Unexpected original test behavior')
                if expected == 0:
                    if checks['correct_probe']['exit_code'] != 0 or checks['mutant_probe']['exit_code'] != 1:
                        raise AssertionError('Stronger native control did not pass/fail as required')
                    if 'AssertionError:' not in checks['mutant_probe']['output']:
                        raise AssertionError('Missing actual assertion evidence')
                for check in checks.values():
                    if check['timed_out'] or check.get('output_truncated'):
                        raise AssertionError('Incomplete output')
                if not audit['integrity']['owned_scratch_removed']:
                    raise AssertionError('Scratch retained')
            report['cases'][label] = json.loads(json.dumps(observed).replace(str(root), '<PROJECT>'))
        if original != {p.name: (p.read_bytes(), p.stat().st_mode) for p in root.iterdir()}:
            raise AssertionError('Originals changed or scratch remained')
        report['originals_unchanged'] = True
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight-output', type=Path, required=True)
    args = parser.parse_args()
    if args.preflight_output.exists():
        parser.error('Refusing to overwrite preflight evidence')
    result = preflight()
    with args.preflight_output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print('Native controls recorded; no model sessions launched.')
