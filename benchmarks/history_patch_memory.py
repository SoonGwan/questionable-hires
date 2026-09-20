"""Local allocation probe, not a model benchmark or subprocess-memory bound."""
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


if __name__ == '__main__':
    print(json.dumps(measure(), indent=2))
