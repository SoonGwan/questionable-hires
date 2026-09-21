"""Local allocation probe, not a model benchmark or subprocess-memory bound."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import sys
import time
import tracemalloc
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('history_memory', ROOT / 'skills/necromancer/scripts/trace.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def measure():
    source = '+++ b/a.py\n@@ -0,0 +1,40000 @@\n' + ''.join('+row %d\n' % i for i in range(40000))
    stream = helper.iter_git_lines
    samples = {'eager': [], 'chunked': []}
    outputs, peaks = {}, {}
    for index in range(10):
        for name in (('eager', 'chunked') if index % 2 == 0 else ('chunked', 'eager')):
            with patch.object(helper, 'iter_git_lines', helper.git_lines if name == 'eager' else stream):
                start = time.perf_counter()
                outputs[name] = helper.selected_patch_excerpt(source, 'a.py', [1, 20000, 40000])
                samples[name].append(time.perf_counter() - start)
    for name in samples:
        with patch.object(helper, 'iter_git_lines', helper.git_lines if name == 'eager' else stream):
            tracemalloc.start()
            try:
                helper.selected_patch_excerpt(source, 'a.py', [1, 20000, 40000])
                peaks[name] = tracemalloc.get_traced_memory()[1]
            finally:
                tracemalloc.stop()
    assert outputs['eager'] is not None and outputs['eager'] == outputs['chunked']
    return dict(python=sys.version.split()[0], input_characters=len(source), equal=True,
                samples_seconds=samples, median_seconds={k: statistics.median(v) for k, v in samples.items()},
                peak_traced_bytes=peaks,
                limitation='Input already allocated; Python excerpt-call allocations only, not RSS/Git/model tokens. Timing excludes tracemalloc, ten alternating pairs on shared host.')


def measure_hunks():
    """Selected-hunk allocations, distinct from the existing excerpt benchmark."""
    spec = importlib.util.spec_from_file_location('hunk_reference', ROOT / 'tests/test_history_hunk_stream.py')
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    result = dict(python=sys.version, helper_sha256=hashlib.sha256(
        (ROOT / 'skills/necromancer/scripts/trace.py').read_bytes()).hexdigest(), cases={})
    for label, (source, targets) in reference.fixtures().items():
        functions = {'eager': reference.eager, 'selected': helper.focused_patch}
        samples = {name: [] for name in functions}
        outputs, peaks = {}, {}
        for index in range(10):
            for name in (('eager', 'selected') if index % 2 == 0 else ('selected', 'eager')):
                start = time.perf_counter()
                outputs[name] = functions[name](source, 'a.py', targets)
                samples[name].append(time.perf_counter() - start)
        if outputs['eager'] != outputs['selected']:
            raise AssertionError('Selected evidence differs from the original implementation')
        for name, function in functions.items():
            tracemalloc.start()
            try:
                function(source, 'a.py', targets)
                peaks[name] = tracemalloc.get_traced_memory()[1]
            finally:
                tracemalloc.stop()
        result['cases'][label] = dict(input_characters=len(source), selected_lines=len(targets),
            equal=True, omitted_hunks=outputs['selected'][1], peak_traced_bytes=peaks,
            samples_seconds=samples, median_seconds={k:statistics.median(v) for k,v in samples.items()})
    result['limitation'] = ('Authored local helper inputs; ten alternating timing pairs, shared host. '
        'Inputs allocated before tracing; selected-function allocations, not RSS/Git/model costs. '
        'Eager reference is the pre-change implementation retained in tests; no model calls.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hunks', action='store_true', help='Measure hunk selection rather than numbered excerpts')
    parser.add_argument('--output', type=Path, help='New JSON evidence path; never overwritten')
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error('Output exists; retain earlier evidence')
    serialized = json.dumps(measure_hunks() if args.hunks else measure(), indent=2) + '\n'
    if args.output is not None:
        with args.output.open('x') as stream:
            stream.write(serialized)
    else:
        print(serialized, end='')
