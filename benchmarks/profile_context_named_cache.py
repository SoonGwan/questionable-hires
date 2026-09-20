"""Profile named collection on repository source, not model performance."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import time
import types

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/con-artist/scripts/context.py'
BEFORE = 'e20396f'


def measure():
    sources = {'before': subprocess.check_output(['git', 'show', BEFORE+':'+SCRIPT], cwd=ROOT),
               'after': (ROOT/SCRIPT).read_bytes()}
    modules = {}
    for name, source in sources.items():
        module = types.ModuleType(name)
        exec(compile(source, SCRIPT, 'exec'), module.__dict__)
        modules[name] = module
    rows = []
    for path in (SCRIPT, 'tests/test_audit_context.py', 'tests/test_httpx_audit.py'):
        raw = (ROOT/path).read_bytes()
        definitions = modules['before'].definition_spans(ast.parse(raw))
        names = [name for _, _, name, node in definitions
                 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))][:8]
        for count in (1, len(names)):
            selectors = [path+':'+name for name in names[:count]]
            expected = modules['before'].collect(ROOT, selectors)
            assert modules['after'].collect(ROOT, selectors) == expected
            samples = {name: [] for name in modules}
            for repeat in range(15):
                for name in (('before', 'after') if repeat % 2 == 0 else ('after', 'before')):
                    started = time.perf_counter()
                    result = modules[name].collect(ROOT, selectors)
                    samples[name].append(time.perf_counter()-started)
                    assert result == expected
            rows.append(dict(path=path, input_sha256=hashlib.sha256(raw).hexdigest(),
                selectors=selectors, outputs_identical=True,
                output_sha256=hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest(),
                samples_seconds=samples,
                median_seconds={k: statistics.median(v) for k,v in samples.items()}))
    return dict(kind='Local collect() profile on repository files; not model evidence',
        before_revision=BEFORE, python=sys.version, repetitions=15,
        source_sha256={k: hashlib.sha256(v).hexdigest() for k,v in sources.items()}, rows=rows,
        limitations='Shared warm host, one interpreter; includes collection, file reads, parsing and JSON budget validation, not CLI startup. First eight function definitions in source order, plus single-selector controls. No token or whole-task savings claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = measure()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(row['path'], len(row['selectors']), row['median_seconds'])
