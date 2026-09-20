"""Give unchanged native preflights their own scratch root in archive tests."""
from contextlib import contextmanager
from pathlib import Path
import tempfile
from unittest.mock import patch


@contextmanager
def isolated_preflight_root(module, parent):
    with tempfile.TemporaryDirectory(dir=parent) as scratch:
        root = Path(scratch)
        (root / 'benchmarks/local-runs').mkdir(parents=True)
        with patch.object(module, 'ROOT', root):
            yield root
