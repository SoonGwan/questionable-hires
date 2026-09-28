"""Adapt the existing allocation profiler to exact-output context collection."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'allocation_engine', ROOT / 'benchmarks/profile_python_regions_budget.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
BEFORE = '65cd6556'


def measure():
    engine.RELATIVE = 'skills/con-artist/scripts/context.py'
    original_load = engine.load
    state = {}

    def load(name, source):
        module = original_load(name, source)

        def collect(_raw, selectors):
            result = module.collect(state['root'], selectors, pretty=state['pretty'])
            # Compare both the object and exact chosen CLI serialization.
            return {'result': result, 'serialized': module.encode(result, state['pretty']) + '\n'}

        module.select_regions = collect
        return module

    engine.load = load
    workloads = {
        'small': b'def first():\n    return 1\ndef second():\n    return 2\n',
        'sparse-large': ('def first():\n' + '    # ' + 'x' * 96 + '\n' +
                         ('    # ' + 'x' * 96 + '\n') * 1799 + '    return 1\n').encode(),
        'dense-fallback': ''.join(f'def f{i}():\n    return {i}\n' for i in range(220)).encode(),
        'format-crossover': ''.join(f'def f{i}():\n' + '    x = 1\n' * 9 for i in range(21)).encode(),
        'repository-tests': (ROOT / 'tests/test_audit_context.py').read_bytes(),
    }

    def cases():
        for identity, raw in workloads.items():
            with tempfile.TemporaryDirectory(prefix='.context-index-profile-',
                                             dir=ROOT / 'benchmarks/local-runs') as folder:
                root = Path(folder)
                (root / 'sample.py').write_bytes(raw)
                (root / 'AGENTS.md').write_text('Read source without executing imports.\n')
                state['root'] = root
                for pretty in (False, True):
                    state['pretty'] = pretty
                    yield identity + ('-pretty' if pretty else '-compact'), raw, ['sample.py']

    try:
        result = engine.measure(before=BEFORE, cases=cases())
    finally:
        engine.load = original_load
    result.update(kind='Native collect() allocation profile; not model performance',
                  wrapper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  engine_sha256=hashlib.sha256(Path(engine.__file__).read_bytes()).hexdigest(),
                  limitations='Four synthetic source shapes plus one repository-source control, compact and pretty. Shared warm host and one interpreter. Includes reads, AST parsing, representation choice and budget validation; wrapper also serializes chosen result. Excludes CLI startup. tracemalloc is Python allocation, not RSS. No model tokens/time claim.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = measure()
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    for row in result['rows']:
        print(json.dumps({key: row[key] for key in
                          ('case', 'median_seconds', 'median_peak_traced_bytes')}))
