#!/usr/bin/env python3
"""Author-only copied-test entry-wait comparison; never rewrites model evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'benchmarks/results/hostage-copy-check-model-01/javascript-preview-latest--skill--1/project'
ASSET = ROOT / 'skills/hostage-negotiator/assets/controlled_call.mjs'


def probe(output):
    original_test = (PROJECT / 'preview.regression.test.mjs').read_text()
    adapted = original_test
    for callback, task in {
        'r.fetch': 'r.task', 'r.decode': 'r.task', 'failed.fetch': 'failed.task',
        'old.fetch': 'old.task', 'old.decode': 'old.task',
        'newest.fetch': 'newest.task', 'newest.decode': 'newest.task',
        'next.fetch': 'next.task', 'br.fetch': 'br.task', 'fetch': 'task', 'decode': 'task',
    }.items():
        before = callback + '.started()'
        adapted, count = re.subn(r'(?<![\w.])' + re.escape(before),
                                callback + '.startedBefore(' + task + ')', adapted)
        assert count, before
    assert '.started()' not in adapted and adapted != original_test
    final = (PROJECT / 'preview.mjs').read_text()
    marker = '      const value = await decode'
    assert final.count(marker) == 1
    broken = final.replace(marker,
        '      if (this.#request !== request) return undefined;\n' + marker)
    original_files = {str(p.relative_to(PROJECT)): p.read_bytes()
                      for p in PROJECT.rglob('*') if p.is_file()}
    results = []
    for mode, tests, asset in (
        ('original_wait', original_test, original_files['test-support/controlled_call.mjs']),
        ('task_aware_wait', adapted, ASSET.read_bytes()),
    ):
        for variant, source in (('final', final), ('skip_stale_decode', broken)):
            with tempfile.TemporaryDirectory(prefix='entry-probe-', dir=output.parent) as folder:
                scratch = Path(folder) / 'project'
                shutil.copytree(PROJECT, scratch)
                (scratch / 'preview.regression.test.mjs').write_text(tests)
                (scratch / 'test-support/controlled_call.mjs').write_bytes(asset)
                (scratch / 'preview.mjs').write_text(source)
                start = time.monotonic()
                run = subprocess.run(['node', '--test', '--test-reporter=tap'], cwd=scratch,
                                     text=True, capture_output=True, timeout=30)
                elapsed = time.monotonic() - start
                transcript = run.stdout + run.stderr
                counts = {k: int(v) for k, v in re.findall(
                    r'^# (tests|pass|fail|cancelled|skipped) (\d+)$', transcript, re.M)}
                expected = {'tests': 43, 'pass': 43 if variant == 'final' else 35,
                            'fail': 0 if variant == 'final' else 8, 'cancelled': 0, 'skipped': 0}
                results.append(dict(mode=mode, variant=variant, elapsed_seconds=elapsed,
                    exit_code=run.returncode, counts=counts,
                    matched=counts == expected and run.returncode == int(variant != 'final'),
                    output=transcript.replace(str(scratch), '<REPLAY>')))
    assert all((PROJECT / path).read_bytes() == data for path, data in original_files.items())
    report = dict(kind='author-adapted retained tests; not model adoption or model-cost evidence',
        source_revision='11122f3', current_asset_sha256=hashlib.sha256(ASSET.read_bytes()).hexdigest(),
        original_tests_sha256=hashlib.sha256(original_test.encode()).hexdigest(),
        adapted_tests_sha256=hashlib.sha256(adapted.encode()).hexdigest(),
        adaptation='Only started() calls changed to startedBefore(relevant_task); asset replaced.',
        adapted_test_source=adapted, retained_source_unchanged=True, checks=results)
    with output.open('x') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')
    print(json.dumps([{k: row[k] for k in ('mode', 'variant', 'elapsed_seconds', 'counts', 'matched')}
                      for row in results], indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite prior evidence')
    probe(args.output.resolve())
