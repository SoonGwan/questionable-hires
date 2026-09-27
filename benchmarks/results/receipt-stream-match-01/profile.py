"""Historical author profile; no model, native test runner or whole-task timing."""
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import sys
import tempfile
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from receipt_stream_match_candidate import transform


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def profile():
    original = ROOT / 'skills/receipt/scripts/compare.py'
    identities = json.loads(Path(__file__).with_name('source-hashes.json').read_text())
    assert hashlib.sha256(original.read_bytes()).hexdigest() == identities['baseline_sha256']
    before = module(original, 'receipt_before')
    rows = []
    with tempfile.TemporaryDirectory(prefix='qh-stream-profile-') as directory:
        root = Path(directory)
        source = root / 'compare.py'
        source.write_text(transform(original.read_text()))
        assert hashlib.sha256(source.read_bytes()).hexdigest() == identities['candidate_sha256']
        after = module(source, 'receipt_after')
        checkers = {'before': lambda path, expected: before.read_limited(path, len(expected)) == expected,
                    'candidate': after.content_matches}
        path = root / 'selected.bin'
        for size in (65536, 8388608):
            expected = b'x' * size
            for mutation, value, wanted in [('same', expected, True),
                                            ('last_byte', expected[:-1] + b'y', False),
                                            ('growth', expected + b'y', False)]:
                path.write_bytes(value)
                data = {name: {'seconds': [], 'peak_allocated_bytes': []} for name in checkers}
                for check in checkers.values():
                    assert check(path, expected) is wanted
                # Separate untraced timing from Python-allocation observations.
                for repeat in range(20):
                    order = list(checkers) if repeat % 2 == 0 else list(reversed(checkers))
                    for name in order:
                        started = time.perf_counter()
                        assert checkers[name](path, expected) is wanted
                        data[name]['seconds'].append(time.perf_counter() - started)
                for name, check in checkers.items():
                    for _ in range(3):
                        tracemalloc.start()
                        try:
                            assert check(path, expected) is wanted
                            data[name]['peak_allocated_bytes'].append(tracemalloc.get_traced_memory()[1])
                        finally:
                            tracemalloc.stop()
                    data[name]['median_seconds'] = statistics.median(data[name]['seconds'])
                assert path.read_bytes() == value
                rows.append({'selected_bytes': size, 'mutation': mutation, 'matches': wanted, 'versions': data})
    return {'source': identities, 'rows': rows,
            'scope': 'Selected final byte comparison only; original expected bytes allocated before tracing. Warm shared-host samples, not process RSS, whole-compare cost or model tokens.'}


if __name__ == '__main__':
    print(json.dumps(profile(), indent=2))
