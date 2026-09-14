#!/usr/bin/env python3
"""Nested configuration release reviews with actual versioned Python consumers."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
OLD = '''def options(config):
    return {'timeout_ms': int(config.get('timeout_ms', 1000)),
            'attempts': int(config.get('attempts', 3))}
'''
NEW = '''def options(config):
    seconds = config.get('timeout_seconds')
    milliseconds = int(float(seconds) * 1000) if seconds is not None else int(config.get('timeout_ms', 1000))
    return {'timeout_ms': milliseconds, 'attempts': int(config.get('attempts', 3))}
'''
TASK = '''Review the release described by ops/releases/current.json for local consumer
configuration compatibility, including mixed versions and rollback. Locate and follow
applicable project instructions. Exercise the actual versioned Python options functions
on each active consumer/config pairing; compare returned values against the documented
service contract, not merely successful calls. Identify the earliest incompatible
step, if any, and distinguish final recovery from safety of the entire sequence.
Report actual commands, observed values, minimal mitigation and unavailable production
evidence. Preserve all supplied files; review only, no fixes or deployment. No services,
network or dependency installation. Any scratch must be project-local and removed.
'''


def cases():
    output = []
    for label, dual_rollback in [('a', True), ('b', False)]:
        phases = [
            {'name': 'original', 'config': 'ops/config/legacy.json', 'active': ['old']},
            {'name': 'mixed rollout', 'config': 'ops/config/bridge.json', 'active': ['old', 'new']},
            {'name': 'old retired and config pruned', 'config': 'ops/config/current.json', 'active': ['new']},
            {'name': 'rollback overlap', 'config': 'ops/config/bridge.json' if dual_rollback else 'ops/config/current.json', 'active': ['new', 'old']},
            {'name': 'rollback complete', 'config': 'ops/config/legacy.json', 'active': ['old']}]
        plan = {'consumers': {'old': 'services/worker/versions/old.py',
                              'new': 'services/worker/versions/new.py'}, 'phases': phases}
        files = {
            'AGENTS.md': 'Review only; preserve every supplied file. Read applicable nested instructions before exercising a component. Use Python standard library, no external services. Keep any scratch under this project and remove it.\n',
            'ops/AGENTS.md': 'Release paths in manifests are relative to repository root. Preserve the listed order; a later recovery does not erase an earlier incompatibility.\n',
            'services/worker/AGENTS.md': 'The service contract is timeout_ms=7500 and attempts=4 at every active pairing, including mixed-version rollback. Check exact options values and that caller-owned config mappings remain unchanged. The supplied version modules have no import-time side effects and may be loaded with runpy.run_path. Actual production reloading, network timing and process orchestration are not supplied.\n',
            'ops/releases/current.json': json.dumps(plan, indent=2) + '\n',
            'ops/config/legacy.json': '{"timeout_ms":7500,"attempts":4}\n',
            'ops/config/bridge.json': '{"timeout_ms":7500,"timeout_seconds":7.5,"attempts":4}\n',
            'ops/config/current.json': '{"timeout_seconds":7.5,"attempts":4}\n',
            'services/worker/versions/old.py': OLD,
            'services/worker/versions/new.py': NEW,
            '.notes/owner.txt': 'Unrelated owner notes: preserve.\n'}
        output.append(dict(id='config-release-' + label, skill='friday', task=TASK, files=files,
                           criteria=['Read applicable root and nested project instructions.',
                                     'Execute actual options functions for active pairings with unchanged config inputs.',
                                     'Assess exact service values, earliest incompatibility and final recovery without reordering.',
                                     'Preserve files and scope; distinguish local results from missing production evidence.']))
    return output


ORACLE = '''import copy
import json
from pathlib import Path
import runpy
import unittest

class ReleaseTests(unittest.TestCase):
    def test_active_options_and_unchanged_inputs(self):
        plan = json.loads(Path('ops/releases/current.json').read_text())
        consumers = {name: runpy.run_path(path)['options'] for name, path in plan['consumers'].items()}
        for phase in plan['phases']:
            config = json.loads(Path(phase['config']).read_text())
            original = copy.deepcopy(config)
            for name in phase['active']:
                with self.subTest(phase=phase['name'], consumer=name):
                    actual = consumers[name](config)
                    print(phase['name'], name, actual)
                    self.assertEqual(config, original)
                    self.assertEqual(actual, {'timeout_ms': 7500, 'attempts': 4})
'''


def preflight():
    rows = []
    for case in cases():
        with tempfile.TemporaryDirectory(prefix='config-preflight-', dir=ROOT) as temporary:
            root = Path(temporary)
            for name, text in dict(case['files'], **{'test_release.py': ORACLE}).items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
            before = {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            result = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'discover', '-v'],
                                    cwd=root, capture_output=True, text=True, timeout=15)
            text = result.stdout + result.stderr
            broken = case['id'].endswith('-b')
            assert result.returncode == int(broken) and 'Ran 1 test' in text, text
            assert 'ERROR:' not in text, text
            if broken:
                assert "phase='rollback overlap', consumer='old'" in text and 'AssertionError:' in text
                assert "'timeout_ms': 1000" in text and "'timeout_ms': 7500" in text
            assert "rollback complete old {'timeout_ms': 7500, 'attempts': 4}" in text
            assert before == {p.relative_to(root): p.read_bytes() for p in root.rglob('*') if p.is_file()}
            rows.append(dict(case=case['id'], exit_code=result.returncode,
                             output=text.replace(str(root), '<PREFLIGHT>')))
    return rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preflight-output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.preflight_output.exists():
        parser.error('Refusing to overwrite frozen evidence')
    observed = preflight()
    for path, data in [(args.output, cases()), (args.preflight_output, observed)]:
        with path.open('x') as stream:
            json.dump(data, stream, indent=2)
            stream.write('\n')
