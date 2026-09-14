#!/usr/bin/env python3
"""Function-only hunk lookup comparison, not an agent performance benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/necromancer/scripts/trace.py'


def compare(revision):
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', revision + '^{commit}'], cwd=ROOT, text=True).strip()
    prior = subprocess.check_output(['git', 'show', revision + ':' + SCRIPT], cwd=ROOT)
    current = (ROOT / SCRIPT).read_bytes()
    functions = {}
    for name, source in [('baseline', prior), ('candidate', current)]:
        namespace = {'__name__': 'trusted_comparison'}
        exec(compile(source, SCRIPT, 'exec'), namespace)
        functions[name] = namespace['focused_patch']
    rows = []
    for count in (1, 1000, 10000):
        text = 'commit fixture\n--- a/a.py\n+++ b/a.py\n' + ''.join(
            f'@@ -{10*i+1} +{10*i+1} @@\n-old_{i}\n+new_{i}\n' for i in range(count))
        targets = list(range(max(1, count * 10 - 99), count * 10 + 1))
        timings = {name: [] for name in functions}
        expected = functions['baseline'](text, 'a.py', targets)
        for repeat in range(5):
            order = ('baseline', 'candidate') if repeat % 2 == 0 else ('candidate', 'baseline')
            for name in order:
                started = time.perf_counter()
                actual = functions[name](text, 'a.py', targets)
                elapsed = time.perf_counter() - started
                assert actual == expected
                timings[name].append(elapsed)
        rows.append(dict(hunks=count, selected_lines=len(targets), input_bytes=len(text.encode()),
                         output_sha256=hashlib.sha256(expected[0].encode()).hexdigest(),
                         omitted_hunks=expected[1], evidence_identical=True, seconds=timings,
                         medians={name: statistics.median(values) for name, values in timings.items()}))
    return dict(baseline_revision=revision, candidate_sha256=hashlib.sha256(current).hexdigest(),
                scenarios=rows, limitation='Authored patch strings, five function calls per version/scenario. '
                'Not native Git end-to-end timing, memory measurement or model token/time savings.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-revision', required=True, help='Trusted local revision whose Python code is executed')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite measurements')
    report = compare(args.baseline_revision)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps(report, indent=2))
