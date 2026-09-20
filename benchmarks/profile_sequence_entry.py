"""Local async scheduling profile; not model or end-to-end performance evidence."""
import argparse
import asyncio
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
import types

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/mother-in-law/scripts/sequence_probe.py'


class Guarded:
    def __init__(self):
        self.result, self.generation = None, 0

    async def run(self, query, fetch):
        self.generation += 1
        generation = self.generation
        result = await fetch(query)
        if generation == self.generation:
            self.result = result


class Unguarded:
    def __init__(self):
        self.result = None

    async def run(self, query, fetch):
        self.result = await fetch(query)


async def measure():
    revisions = {'pre_fix': '8804ee4', 'task_race': '87513cb'}
    sources = {name: subprocess.check_output(['git', 'show', revision+':'+SCRIPT], cwd=ROOT)
               for name, revision in revisions.items()}
    sources['future_signal'] = (ROOT/SCRIPT).read_bytes()
    modules = {}
    for name, source in sources.items():
        module = types.ModuleType(name)
        exec(compile(source, SCRIPT, 'exec'), module.__dict__)
        modules[name] = module
    rows = []
    repeats, batch = 12, 300
    for factory, expected in ((Guarded, [True, True]), (Unguarded, [True, False])):
        reference = await modules['pre_fix'].probe(factory, 'run', 'result', 'old', 'new', None)
        assert [case['passed'] for case in reference] == expected
        samples = {name: [] for name in modules}
        names = list(modules)
        for repeat in range(repeats):
            # Rotate all three implementations through each position.
            order = names[repeat % 3:] + names[:repeat % 3]
            for name in order:
                started = time.perf_counter()
                for _ in range(batch):
                    result = await modules[name].probe(factory, 'run', 'result', 'old', 'new', None)
                    assert result == reference
                samples[name].append((time.perf_counter()-started)/batch)
        rows.append(dict(case=factory.__name__, expected_passes=expected,
                         outputs_identical=True, samples_seconds_per_probe=samples,
                         median_seconds_per_probe={k: statistics.median(v) for k,v in samples.items()}))
    return dict(kind=__doc__, python=sys.version, revisions=revisions,
                source_sha256={k: hashlib.sha256(v).hexdigest() for k,v in sources.items()},
                repetitions=repeats, probes_per_batch=batch, rows=rows,
                limitations='Synthetic in-process components, shared warm host, no CLI/import cost, '
                'no model calls or token savings. Early termination covered separately by regression tests.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = asyncio.run(measure())
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(row['case'], row['median_seconds_per_probe'])
