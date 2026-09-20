"""Compare exact excerpt output, local latency and traced allocation peaks."""
import argparse
import gc
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
import tracemalloc
import types

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = 'skills/necromancer/scripts/python_regions.py'
BEFORE = 'd087a96'


def load(name, source):
    module = types.ModuleType(name)
    exec(compile(source, name, 'exec'), module.__dict__)
    return module


def workloads():
    yield 'small-complete', b'def first():\n    return 1\ndef second():\n    return 2\n', ['first', 'second']
    yield 'large-single', ('def f():\n    return "' + 'x' * 1_800_000 + '"\n').encode(), ['f']
    nested = ''.join('    ' * i + f'def f{i}():\n' for i in range(10))
    nested += '    ' * 10 + 'return "' + 'x' * 1_800_000 + '"\n'
    yield 'large-overlap', nested.encode(), [f'f{i}' for i in range(10)]


def measure():
    sources = {'before': subprocess.check_output(['git', 'show', BEFORE + ':' + RELATIVE], cwd=ROOT),
               'after': (ROOT / RELATIVE).read_bytes()}
    modules = {name: load(name, source) for name, source in sources.items()}
    rows = []
    for identity, raw, names in workloads():
        outputs = {name: module.select_regions(raw, names) for name, module in modules.items()}
        assert outputs['before'] == outputs['after']
        timings = {name: [] for name in modules}
        peaks = {name: [] for name in modules}
        for repeat in range(7):
            for name in (('before', 'after') if repeat % 2 == 0 else ('after', 'before')):
                started = time.perf_counter()
                result = modules[name].select_regions(raw, names)
                timings[name].append(time.perf_counter() - started)
                assert result == outputs['before']
        # Allocation instrumentation is separate from latency measurements.
        for repeat in range(3):
            for name in (('before', 'after') if repeat % 2 == 0 else ('after', 'before')):
                gc.collect()
                tracemalloc.start()
                try:
                    result = modules[name].select_regions(raw, names)
                    peaks[name].append(tracemalloc.get_traced_memory()[1])
                finally:
                    tracemalloc.stop()
                assert result == outputs['before']
        rows.append(dict(case=identity, input_bytes=len(raw), input_sha256=hashlib.sha256(raw).hexdigest(),
            names=names, outputs_identical=True,
            output_sha256=hashlib.sha256(json.dumps(outputs['before'], sort_keys=True).encode()).hexdigest(),
            samples_seconds=timings, samples_peak_traced_bytes=peaks,
            median_seconds={k: statistics.median(v) for k, v in timings.items()},
            median_peak_traced_bytes={k: statistics.median(v) for k, v in peaks.items()}))
    return dict(kind='Local select_regions microbenchmark, not model performance', python=sys.version,
        before_revision=BEFORE, source_sha256={k: hashlib.sha256(v).hexdigest() for k, v in sources.items()},
        rows=rows, warmup='One equality-check invocation per arm/workload',
        timing_repetitions=7, allocation_repetitions=3, order='Alternating before/after',
        limitations='Synthetic inputs, shared warm host, one interpreter. Function includes decode/parse/hash/excerpt, not CLI startup or Git. tracemalloc is Python-traced peak allocation, not RSS/total memory. No model token/time or general speedup claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = measure()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(json.dumps({key: row[key] for key in ('case', 'median_seconds', 'median_peak_traced_bytes')}))
