#!/usr/bin/env python3
"""Compare complete local collector processes on one disposable real Git history."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/necromancer/scripts/trace.py'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline-revision', required=True, help='Trusted local revision to execute')
    parser.add_argument('--layout', choices=('rewrite', 'scattered'), default='rewrite')
    args = parser.parse_args()
    revision = subprocess.check_output(
        ['git', 'rev-parse', '--verify', args.baseline_revision + '^{commit}'],
        cwd=ROOT, text=True).strip()
    prior = subprocess.check_output(['git', 'show', revision + ':' + SCRIPT], cwd=ROOT)
    current = (ROOT / SCRIPT).read_bytes()
    with tempfile.TemporaryDirectory(prefix='qh-collector-bench-') as directory:
        scratch = Path(directory)
        repo = scratch / 'project'
        repo.mkdir()
        def git(*command):
            return subprocess.check_output(['git', *command], cwd=repo, text=True).strip()
        git('init', '-q', '--template=')
        git('config', 'user.name', 'Collector Fixture')
        git('config', 'user.email', 'fixture@example.invalid')
        git('config', 'commit.gpgsign', 'false')
        git('config', 'core.hooksPath', str(scratch / 'no-hooks'))
        for version in ('old', 'new'):
            (repo / 'data.txt').write_text(''.join(
                f'{version if args.layout == "rewrite" or i % 20 == 0 else "old"}_{i:06d}\n'
                for i in range(100000)))
            git('add', 'data.txt')
            git('commit', '-qm', version)
        before = git('status', '--porcelain')
        source_hash = hashlib.sha256((repo / 'data.txt').read_bytes()).hexdigest()
        scripts = {}
        for name, content in (('baseline', prior), ('candidate', current)):
            scripts[name] = scratch / (name + '.py')
            scripts[name].write_bytes(content)
        timings = {name: [] for name in scripts}
        canonical = None
        for repeat in range(3):
            order = ('baseline', 'candidate') if repeat % 2 == 0 else ('candidate', 'baseline')
            for name in order:
                started = time.perf_counter()
                result = subprocess.run(
                    [sys.executable, '-B', str(scripts[name]), '--repo', str(repo),
                     '--path', 'data.txt', '--lines', '50000:50099'],
                    capture_output=True, text=True, timeout=60, check=True)
                elapsed = time.perf_counter() - started
                evidence = json.loads(result.stdout)
                if canonical is None:
                    canonical = evidence
                if evidence != canonical:
                    raise RuntimeError('Collector evidence differs')
                if args.layout == 'rewrite' and not evidence['commits'][0].get('selected_patch_excerpt'):
                    raise RuntimeError('Fixture did not exercise large-hunk excerpt')
                if args.layout == 'scattered' and not any(c['omitted_hunks'] > 1000 for c in evidence['commits']):
                    raise RuntimeError('Fixture did not exercise many-hunk selection')
                timings[name].append(elapsed)
        if (before or git('status', '--porcelain') or
                hashlib.sha256((repo / 'data.txt').read_bytes()).hexdigest() != source_hash):
            raise RuntimeError('Fixture changed during collection')
        print(json.dumps(dict(baseline_revision=revision, layout=args.layout, python=sys.version,
                              candidate_sha256=hashlib.sha256(current).hexdigest(),
                              input_sha256=source_hash, evidence_identical=True,
                              current_file_bytes=(repo / 'data.txt').stat().st_size,
                              seconds=timings,
                              medians={k: statistics.median(v) for k, v in timings.items()},
                              limitation='One local Git fixture, three calls per version; '
                                          'not agent/session performance or total-memory measurement.'), indent=2))


if __name__ == '__main__':
    main()
