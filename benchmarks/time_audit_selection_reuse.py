"""Fixed native helper timing screen; not a model benchmark."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
REVISIONS = {'before': '51a4f5a', 'after': 'b1875a0'}
CASES = ['adjacent-control', 'revisited-selection', 'alternating-eight']


def schedule():
    return [dict(case=case, repeat=repeat, arm=arm)
            for repeat in range(3) for index, case in enumerate(CASES)
            for arm in (['before', 'after'] if (repeat + index) % 2 == 0 else ['after', 'before'])]


def summarize(rows):
    expected = {(c['case'], c['repeat'], c['arm']) for c in schedule()}
    observed = [(c['case'], c['repeat'], c['arm']) for c in rows]
    if len(observed) != len(set(observed)) or set(observed) != expected:
        raise ValueError('All 18 scheduled native cells must be present exactly once')
    summary = {}
    for case in CASES:
        arms = {arm: [r['elapsed_seconds'] for r in rows if r['case'] == case and r['arm'] == arm]
                for arm in REVISIONS}
        if any(not isinstance(v, (int, float)) or not 0 < v < float('inf')
               for values in arms.values() for v in values):
            raise ValueError('Expected positive finite elapsed seconds')
        summary[case] = {arm: dict(mean=statistics.mean(values), minimum=min(values), maximum=max(values))
                         for arm, values in arms.items()}
        summary[case]['after_over_before_mean'] = statistics.mean(arms['after']) / statistics.mean(arms['before'])
    return summary


def run(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    resources = {arm: subprocess.check_output(['git', 'show', revision + ':skills/con-artist/scripts/audit.py'], cwd=ROOT)
                 for arm, revision in REVISIONS.items()}
    probe_bytes = subprocess.check_output(['git', 'show', 'b1875a0:benchmarks/probe_audit_selection_reuse.py'], cwd=ROOT)
    manifest = dict(kind='author native helper timing, not model evidence', schedule=schedule(),
                    revisions=REVISIONS, helper_sha256={a: hashlib.sha256(b).hexdigest() for a, b in resources.items()},
                    probe_sha256=hashlib.sha256(probe_bytes).hexdigest(),
                    timing='perf_counter around one frozen probe case: helper import, fixture setup, native checks, validation and cleanup; excludes Python process startup, resource materialization and JSON export',
                    limitations='Three authored cases, three repeats/arm, serial shared host/cache. No warmup, retries, exclusions or statistical superiority claim. Baseline observations are reused, not fresh evidence. No model tokens, billing or total user-task latency measured.')
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    rows = []
    with tempfile.TemporaryDirectory(prefix='audit-timing-resources-') as temporary:
        root = Path(temporary)
        probe_path = root / 'probe.py'
        probe_path.write_bytes(probe_bytes)
        spec = importlib.util.spec_from_file_location('timing_probe', probe_path)
        probe = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(probe)
        cases = dict(probe.SEQUENCES)
        for arm, content in resources.items():
            (root / (arm + '.py')).write_bytes(content)
        for index, cell in enumerate(manifest['schedule']):
            probe.SCRIPT = root / (cell['arm'] + '.py')
            probe.SEQUENCES = {cell['case']: cases[cell['case']]}
            start = time.perf_counter()
            observation = probe.probe()
            elapsed = time.perf_counter() - start
            if observation['helper_sha256'] != manifest['helper_sha256'][cell['arm']]:
                raise ValueError('Unexpected measured helper identity')
            row = dict(cell, elapsed_seconds=elapsed, observation=observation)
            (output / ('cell-%02d.json' % index)).write_text(json.dumps(row, indent=2) + '\n')
            rows.append(row)
    summary = summarize(rows)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.output), indent=2))
