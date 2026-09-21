"""Single native run: compare TAP and experimental view bytes, not model tokens."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPORTER = ROOT / 'benchmarks/prototypes/native_node_reporter.mjs'
SOURCE = '''import test from 'node:test';
import assert from 'node:assert/strict';
import {appendFileSync} from 'node:fs';
for (let i = 0; i < 24; i++) test(`wrong result ${i}`, () => {
  appendFileSync('calls.txt', 'x'); assert.equal(2, 1, 'wrong result');
});
'''


def measure(output, passing=False):
    node = shutil.which('node')
    if not node:
        raise ValueError('This experimental profile requires Node 24')
    version = subprocess.check_output([node, '--version'], text=True).strip()
    if version.split('.')[0] != 'v24':
        raise ValueError('This experimental profile is scoped to Node 24')
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = SOURCE.replace('assert.equal(2, 1', 'assert.equal(1, 1') if passing else SOURCE
    (output / 'case.test.mjs').write_text(source)
    command = [node, '--test', '--test-reporter=tap', '--test-reporter-destination=raw.tap',
        '--test-reporter=' + str(REPORTER), '--test-reporter-destination=stdout', 'case.test.mjs']
    (output / 'argv.json').write_text(json.dumps(command, indent=2) + '\n')
    result = subprocess.run(command, cwd=output, capture_output=True, timeout=10)
    (output / 'compact.jsonl').write_bytes(result.stdout)
    (output / 'stderr.txt').write_bytes(result.stderr)
    (output / 'exit.txt').write_text(str(result.returncode) + '\n')
    tap = (output / 'raw.tap').read_bytes()
    records = [json.loads(line) for line in result.stdout.splitlines()]
    end = records[-1]
    assert result.returncode == (0 if passing else 1) and not result.stderr
    assert (output / 'calls.txt').read_text() == 'x' * 24
    assert end['single_global_summary_seen'] and end['native']['counts']['failed'] == (0 if passing else 24)
    assert end['native']['native_success'] == passing and end['omitted_result_events'] == 0
    assert len([r for r in records if r['type'] == ('test:pass' if passing else 'test:fail')]) == 24
    observation = dict(kind='author native output-volume observation, not model evidence',
        node_version=version,
        reporter_sha256=hashlib.sha256(REPORTER.read_bytes()).hexdigest(),
        source_sha256=hashlib.sha256(source.encode()).hexdigest(),
        native_exit=result.returncode, executions=24, failures=0 if passing else 24,
        raw_tap_bytes=len(tap), compact_bytes=len(result.stdout),
        raw_tap_sha256=hashlib.sha256(tap).hexdigest(),
        compact_sha256=hashlib.sha256(result.stdout).hexdigest(),
        limitation='One authored 24-test fixture (failure or passing control); same native run and different presentations. Raw output remains necessary. No tokenizer, billing, latency or whole-task improvement measurement.')
    (output / 'observation.json').write_text(json.dumps(observation, indent=2) + '\n')
    return observation


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--passing', action='store_true', help='Normal passing control with the same test count')
    args = parser.parse_args()
    print(json.dumps(measure(args.output, args.passing), indent=2))
