#!/usr/bin/env python3
"""Compare separate and batched complete collector invocations, not model cost."""
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
    parser.add_argument('--baseline-revision', required=True, help='Trusted local source revision')
    parser.add_argument('--output', type=Path, required=True, help='New local measurement JSON')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; do not overwrite a measurement')
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', args.baseline_revision + '^{commit}'],
                                       cwd=ROOT, text=True).strip()
    prior = subprocess.check_output(['git', 'show', revision + ':' + SCRIPT], cwd=ROOT)
    current = (ROOT / SCRIPT).read_bytes()
    ranges = [(25000, 25009), (50000, 50009), (75000, 75009)]
    timings, sizes = {k: [] for k in ('separate', 'batch')}, {}
    with tempfile.TemporaryDirectory(prefix='qh-history-ranges-', dir=ROOT) as directory:
        scratch = Path(directory)
        project = scratch / 'project'
        project.mkdir()
        def git(*command):
            return subprocess.check_output(['git', *command], cwd=project, text=True).strip()
        git('init', '-q', '--template=')
        git('config', 'user.name', 'Range Benchmark')
        git('config', 'user.email', 'fixture@example.invalid')
        git('config', 'commit.gpgsign', 'false')
        git('config', 'core.hooksPath', str(scratch / 'no-hooks'))
        rows = [f'old_{i:06d}\n' for i in range(1, 100001)]
        path = project / 'data.txt'
        path.write_text(''.join(rows))
        git('add', '.'); git('commit', '-qm', 'Initial records')
        for start, end in ranges:
            for number in range(start, end + 1):
                rows[number - 1] = f'new_{number:06d}\n'
        path.write_text(''.join(rows))
        git('add', '.'); git('commit', '-qm', 'Update three distant regions')
        source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        scripts = {}
        for name, content in [('separate', prior), ('batch', current)]:
            scripts[name] = scratch / (name + '.py')
            scripts[name].write_bytes(content)
        reference = None
        for repeat in range(3):
            for mode in (('separate', 'batch') if repeat % 2 == 0 else ('batch', 'separate')):
                groups = [[r] for r in ranges] if mode == 'separate' else [ranges]
                observations, output_bytes = [], 0
                started = time.perf_counter()
                for selections in groups:
                    flags = [item for start, end in selections for item in ('--lines', f'{start}:{end}')]
                    run = subprocess.run([sys.executable, '-B', str(scripts[mode]), '--repo', str(project),
                                          '--path', 'data.txt', *flags], capture_output=True, check=True, timeout=60)
                    observations.append(json.loads(run.stdout))
                    output_bytes += len(run.stdout)
                timings[mode].append(time.perf_counter() - started)
                sizes[mode] = output_bytes
                projected = {key: [r for observation in observations for r in observation[key]]
                             for key in ('current_lines', 'blame')}
                if reference is None:
                    reference = projected
                assert projected == reference
                assert [r['line'] for r in projected['current_lines']] == [i for a, b in ranges for i in range(a, b + 1)]
                assert all(o['history'] == 'available' and o['omitted_commits'] == 0 for o in observations)
                patches = [c for o in observations for c in o['commits']]
                assert all(c['exit_code'] == 0 and not c['truncated'] for c in patches)
                evidence = '\n'.join(c['evidence'] for c in patches)
                for start, end in ranges:
                    for i in range(start, end + 1):
                        assert f'-old_{i:06d}' in evidence and f'+new_{i:06d}' in evidence
                assert 'old_040000' not in evidence
        assert git('status', '--porcelain') == ''
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source_hash
    result = dict(baseline_revision=revision, candidate_sha256=hashlib.sha256(current).hexdigest(),
                  python=sys.version, ranges=ranges, input_bytes=1100000, input_sha256=source_hash,
                  seconds=timings, medians={k: statistics.median(v) for k, v in timings.items()},
                  stdout_bytes=sizes, selected_current_and_blame_equal=True,
                  selected_old_and_new_patch_lines_retained=True, original_source_unchanged=True,
                  limitation='One authored local Git history; three paired rounds of complete CLI collection. '
                             'Separate outputs repeat commit metadata; batch shares it. Not model token/time or general performance.')
    with args.output.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
