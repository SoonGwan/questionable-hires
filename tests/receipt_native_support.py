"""Run native controls with hash-verified shipped bytes, not invented Git evidence."""
from contextlib import contextmanager
import hashlib
from pathlib import Path
import shutil
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = 'skills/receipt/scripts/compare.py'
HELPER_SHA256 = 'a94b827a6fd346a93adbfb6ea4b3606d66b26f7e5201a035da7fc853978c2fe7'


@contextmanager
def native_controls(runner):
    raw = (ROOT / HELPER).read_bytes()
    if hashlib.sha256(raw).hexdigest() != HELPER_SHA256:
        raise ValueError('Receipt native control helper identity changed')
    revision = runner.REVISIONS['current'] if hasattr(runner, 'REVISIONS') else runner.RESOURCE

    def retained_git(*args):
        if args != ('show', revision + ':' + HELPER):
            raise AssertionError('Unexpected Git request in native control: ' + repr(args))
        # Content availability only. A separate history check proves provenance.
        return raw

    with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
        root = Path(scratch)
        (root / 'benchmarks/local-runs').mkdir(parents=True)
        for name in (HELPER, 'tests/test_receipt_startup_case.py',
                     'benchmarks/receipt-ledger-cases.json'):
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, destination)
        with patch.object(runner, 'ROOT', root), patch.object(runner, 'git', side_effect=retained_git):
            yield root
