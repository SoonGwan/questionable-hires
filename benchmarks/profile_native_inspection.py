"""Author-only native display accounting; not a model or latency benchmark."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPORTER = ROOT / 'benchmarks/prototypes/native_node_reporter_v2.mjs'
CASES = {'tiny-pass': (1, 0), 'many-pass': (24, 0),
         'repeated-failure': (24, 24), 'late-failure': (206, 1)}


def source_for(count, failures):
    return '''import test from 'node:test';
import assert from 'node:assert/strict';
import {appendFileSync} from 'node:fs';
for (let i=0; i<COUNT; i++) test(`case-${i}`, () => {
  appendFileSync('calls.txt', 'x');
  assert.equal(i >= COUNT-FAILURES ? 2 : 1, 1, `result-${i}`);
});
'''.replace('COUNT', str(count)).replace('FAILURES', str(failures))


def measure(output):
    node = shutil.which('node')
    if not node:
        raise ValueError('Node 24 required')
    version = subprocess.check_output([node, '--version'], text=True).strip()
    if not version.startswith('v24.'):
        raise ValueError('This author probe is scoped to Node 24')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {'kind': 'author native display accounting; not model evidence',
              'node_version': version,
              'reporter_sha256': hashlib.sha256(REPORTER.read_bytes()).hexdigest(),
              'cases': {}}
    for name, (count, failures) in CASES.items():
        folder = output / name
        folder.mkdir()
        source = source_for(count, failures)
        (folder / 'case.test.mjs').write_text(source)
        argv = [node, '--test', '--test-reporter=tap', '--test-reporter-destination=raw.tap',
                '--test-reporter=spec', '--test-reporter-destination=raw.spec',
                '--test-reporter=' + str(REPORTER), '--test-reporter-destination=stdout',
                'case.test.mjs']
        (folder / 'argv.json').write_text(json.dumps(argv, indent=2) + '\n')
        result = subprocess.run(argv, cwd=folder, capture_output=True, timeout=10,
                                env=dict(os.environ, NO_COLOR='1'))
        (folder / 'first-look.jsonl').write_bytes(result.stdout)
        (folder / 'stderr.txt').write_bytes(result.stderr)
        (folder / 'exit.txt').write_text(str(result.returncode) + '\n')
        end = json.loads(result.stdout.splitlines()[-1])
        assert result.returncode == (1 if failures else 0), result.stderr
        assert (folder / 'calls.txt').read_text() == 'x' * count
        assert end['summaries'] == 1
        assert end['native']['counts']['tests'] == count
        assert end['native']['counts']['failed'] == failures
        assert end['exceptional_results_omitted'] == 0
        lengths = {}
        identities = {}
        for filename in ['raw.tap', 'raw.spec', 'first-look.jsonl', 'stderr.txt']:
            content = (folder / filename).read_bytes()
            lengths[filename] = len(content)
            identities[filename] = hashlib.sha256(content).hexdigest()
        report['cases'][name] = dict(source_sha256=hashlib.sha256(source.encode()).hexdigest(),
            executions=count, failures=failures, native_exit=result.returncode,
            stderr_present=bool(result.stderr),
            bytes=lengths, sha256=identities,
            full_tap_inspection_bytes=lengths['first-look.jsonl'] + lengths['raw.tap'],
            full_spec_inspection_bytes=lengths['first-look.jsonl'] + lengths['raw.spec'])
    report['limitations'] = ('Four authored fixtures, one native execution each, three presentations. '
        'Full-inspection sums count display bytes, not model tokens, interactions, latency or billing. '
        'Selective reading is not measured. Spec is an existing native format, not a skill invention. '
        'Source/capture overhead excluded equally; output paths affect byte sizes. '
        'This fixed-fixture probe is not a general capture wrapper.')
    (output / 'observation.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(measure(args.output), indent=2))
