"""Author-only line-selection microbenchmark, not whole-task model evidence."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import statistics
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/necromancer/scripts/trace.py'


def measure():
    spec = importlib.util.spec_from_file_location('current_lines_helper', SCRIPT)
    helper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helper)
    cases = [('many-short', 'short row\n' * 190000, [1, 95000, 190000]),
             ('early-only', 'short row\n' * 190000, [1]),
             ('long-row', 'x' * 1900000, [1]),
             ('small', 'short row\n' * 30, [1, 15, 30])]
    records = []
    for name, source, numbers in cases:
        def eager():
            lines = helper.git_lines(source)
            return [dict(line=n, text=lines[n - 1]) for n in numbers]
        def selected():
            return helper.selected_current_lines(source, numbers)
        if eager() != selected():
            raise AssertionError('Selected text differs: ' + name)
        functions = [('eager', eager), ('selected', selected)]
        seconds = {label: [] for label, _ in functions}
        peaks = {}
        for repeat in range(9):
            for label, function in functions[::1 if repeat % 2 == 0 else -1]:
                start = time.perf_counter()
                function()
                seconds[label].append(time.perf_counter() - start)
        for label, function in functions:
            tracemalloc.start()
            try:
                function()
                peaks[label] = tracemalloc.get_traced_memory()[1]
            finally:
                tracemalloc.stop()
        records.append(dict(case=name, source_characters=len(source), selected=numbers,
                            identical=True, seconds=seconds,
                            median_seconds={k: statistics.median(v) for k, v in seconds.items()},
                            peak_bytes=peaks))
    return dict(python=platform.python_version(), platform=platform.platform(),
                helper_sha256=hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), cases=records,
                limitation='Author-created microbenchmark; source is already decoded. '
                'No file I/O, Git, model call, or whole-task performance measured.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Refusing to overwrite evidence')
    result = measure()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['cases']:
        print(row['case'], row['median_seconds'], row['peak_bytes'])
