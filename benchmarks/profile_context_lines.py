"""Local collector microbenchmark; never a model token/time benchmark."""
import argparse
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import tempfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
RELATIVE = 'skills/con-artist/scripts/context.py'
BEFORE = 'ff474e5'


def load(name, source):
    module = types.ModuleType(name)
    module.__file__ = str(ROOT / RELATIVE)
    exec(compile(source, module.__file__, 'exec'), module.__dict__)
    return module


def measure():
    old = subprocess.check_output(['git', 'show', BEFORE + ':' + RELATIVE], cwd=ROOT)
    new = (ROOT / RELATIVE).read_bytes()
    modules = {'before': load('context_before', old), 'after': load('context_after', new)}
    rows = []
    with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks/local-runs') as scratch:
        project = Path(scratch)
        for count in (50, 500):
            source = ''.join(f'@decorate({i})\ndef f{i}(value):\n    first = value + {i}\n    second = first * 2\n    return second\n\n' for i in range(count))
            (project / 'module.py').write_text(source)
            for selected in (1, 8):
                selectors = [f'module.py:{(i * (count // selected)) * 6 + 4}' for i in range(selected)]
                outputs = {name: module.collect(project, selectors) for name, module in modules.items()}
                assert outputs['before'] == outputs['after']
                samples = {name: [] for name in modules}
                for repeat in range(7):
                    order = ('before', 'after') if repeat % 2 == 0 else ('after', 'before')
                    for name in order:
                        start = time.perf_counter()
                        result = modules[name].collect(project, selectors)
                        samples[name].append(time.perf_counter() - start)
                        assert result == outputs['before']
                rows.append(dict(definitions=count, selectors=selectors,
                    input_sha256=hashlib.sha256(source.encode()).hexdigest(),
                    output_sha256=hashlib.sha256(json.dumps(outputs['before'], sort_keys=True).encode()).hexdigest(),
                    outputs_identical=True, samples_seconds=samples,
                    median_seconds={name: statistics.median(values) for name, values in samples.items()}))
    return dict(kind='Local function microbenchmark, not model performance', before_revision=BEFORE,
        source_sha256={'before': hashlib.sha256(old).hexdigest(), 'after': hashlib.sha256(new).hexdigest()},
        repetitions=7, warmup='One equality-check invocation per arm/workload before timing',
        order='Alternates before/after within each workload', rows=rows,
        limitations='Synthetic definition files, warm shared host/filesystem, one interpreter. Includes collect parsing/reading/output-bound serialization, not CLI startup or model calls. No statistical/general speedup claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = measure()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        old, new = row['median_seconds']['before'], row['median_seconds']['after']
        print(json.dumps(dict(definitions=row['definitions'], selectors=len(row['selectors']),
                              before=old, after=new, change_percent=(new / old - 1) * 100)))
