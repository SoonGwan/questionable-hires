"""Run frozen native controls from retained bytes, without claiming Git provenance."""
from contextlib import contextmanager
import hashlib
from pathlib import Path
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / 'benchmarks/results/con-artist-repository-01/baseline/repository-collector-cache--baseline--1/project'
HASHES = {
    'skills/con-artist/scripts/context.py': 'ef2d38d549e7e33b894df4c4eb5156391c752a2e8d3d6bcab9ccc9a53aad3fcd',
    'tests/test_context_line_index.py': '4033cddc3c8029df60ba692e778f2c5e6d73168245db73575386f908b13ae299',
}


def retained_sources():
    result = {}
    for name, expected in HASHES.items():
        raw = (PROJECT / name).read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError('Retained repository fixture identity changed: ' + name)
        result[name] = raw.decode('utf-8')
    return result


@contextmanager
def native_controls(module):
    # Supply identical retained inputs to the unchanged author preflight. Its
    # expected local scratch parent belongs only to this disposable test root.
    sources = retained_sources()
    with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
        root = Path(scratch)
        (root / 'benchmarks/local-runs').mkdir(parents=True)
        with patch.object(module, 'source_files', side_effect=lambda: dict(sources)), patch.object(module, 'ROOT', root):
            yield
