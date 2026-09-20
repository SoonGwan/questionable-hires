"""Optional bounded preservation guard for caller-owned native comparisons.

Reuses the adjacent comparison helper's inventory; does not invoke its runner.
Trusted local workflows only. Not a sandbox or a test-success verdict.
"""
from contextlib import contextmanager
import hashlib
import importlib.util
import json
import os
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    '_receipt_preservation_inventory', Path(__file__).with_name('compare.py'))
_comparison = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_comparison)
tree_inventory = _comparison.tree_inventory


@contextmanager
def preserved_tree(root):
    """Inventory once before/after; caller cleans scratch inside the block.

    Authorize reading the entire root first. Changes raise without restoration.
    Caller exceptions propagate even if originals remain unchanged. Result starts
    unknown; inspect after normal exit. No native runner, subprocess supervision,
    provenance, scratch cleanup or test-outcome interpretation is supplied here.
    """
    root = Path(root).resolve(strict=True)
    if os.name != 'posix' or not root.is_dir():
        raise ValueError('Requires POSIX and a directory root')
    previous, byte_count = tree_inventory(root)
    report = {'unchanged': None}
    try:
        yield report
    finally:
        report.clear()
        report['unchanged'] = None
        current, _ = tree_inventory(root)
        differences = sorted(name for name in previous.keys() | current.keys()
                             if previous.get(name) != current.get(name))
        if differences:
            raise RuntimeError('Project tree changed; not restored (' + str(len(differences))
                               + ' paths): ' + ', '.join(differences[:20]))
        encoded = json.dumps(previous, sort_keys=True, separators=(',', ':')).encode()
        report.update(unchanged=True, entries=len(previous), file_bytes=byte_count,
                      inventory_sha256=hashlib.sha256(encoded).hexdigest(),
                      scope='source root including Git metadata; symlink targets not read')
