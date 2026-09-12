#!/usr/bin/env python3
"""Local function microbenchmark; executes a trusted committed helper revision."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
import types

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/necromancer/scripts/trace.py'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-revision', required=True,
                        help='Trusted local Git revision to execute, not untrusted submitted code')
    args = parser.parse_args()
    revision = subprocess.check_output(
        ['git', 'rev-parse', '--verify', args.baseline_revision + '^{commit}'], cwd=ROOT,
        text=True).strip()
    baseline = types.ModuleType('history_baseline')
    exec(subprocess.check_output(['git', 'show', revision + ':' + SCRIPT], cwd=ROOT),
         baseline.__dict__)
    spec = importlib.util.spec_from_file_location('history_candidate', ROOT / SCRIPT)
    candidate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    source = ('diff --git a/a.py b/a.py\n--- a/a.py\n+++ b/a.py\n'
              '@@ -1,100000 +1,100000 @@\n' +
              ''.join(f' context_{i:06d}\n' for i in range(100000)))
    cases = [('one', [50000]), ('20-near', list(range(50000, 50020))),
             ('20-far', list(range(1000, 100000, 5000))),
             ('100-near', list(range(50000, 50100))),
             ('100-far', list(range(500, 100000, 1000)))]
    functions = {'baseline': baseline.selected_patch_excerpt,
                 'candidate': candidate.selected_patch_excerpt}
    for name, targets in cases:
        expected = functions['baseline'](source, 'a.py', targets)
        if expected is None or functions['candidate'](source, 'a.py', targets) != expected:
            raise RuntimeError('Candidate evidence differs: ' + name)
        timings = {key: [] for key in functions}
        for repeat in range(7):
            order = ('baseline', 'candidate') if repeat % 2 == 0 else ('candidate', 'baseline')
            for key in order:
                started = time.perf_counter()
                actual = functions[key](source, 'a.py', targets)
                elapsed = time.perf_counter() - started
                if actual != expected:
                    raise RuntimeError('Unstable evidence: ' + name)
                timings[key].append(elapsed)
        print(json.dumps(dict(case=name, baseline_revision=revision,
                              candidate_sha256=hashlib.sha256((ROOT / SCRIPT).read_bytes()).hexdigest(),
                              python=sys.version, evidence_identical=True,
                              excerpt_characters=len(expected), seconds=timings,
                              medians={k: statistics.median(v) for k, v in timings.items()},
                              limitation='Function-only local timing; not model tokens, RSS or session cost.')),
              flush=True)


if __name__ == '__main__':
    main()
