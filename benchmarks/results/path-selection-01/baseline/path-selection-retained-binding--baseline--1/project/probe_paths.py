"""Run with python3 -B probe_paths.py; writes probe_trace.json beside this file.

Observation wrappers delegate to the supplied client, loader and real file I/O.
Assertions below check this reproduction, not the desired corrected behavior.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
from unittest.mock import patch

import client
import loader

BASE = Path(__file__).resolve().parent
ORIGINALS = (
    "client.py", "loader.py", "test_paths.py", "requirements.md",
    "alpha/settings.txt", "alpha/other.txt", "beta/settings.txt", "beta/other.txt",
)


def hashes():
    return {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
            for name in ORIGINALS}


def main():
    before = hashes()
    command = ["python3", "-B", "-m", "unittest", "-v", "test_paths"]
    native = subprocess.run(command, cwd=BASE, capture_output=True, text=True)
    trace = {
        "scope": "Supplied local application, sequential calls; no production inference",
        "instrumentation": "Delegating loader.read_limit and io.open wrappers; "
                           "file_read records the actual handle.read result. "
                           "Empty read lists mean no read at this observed boundary. "
                           "OS disk/page-cache activity is not measured.",
        "native_tests": {"command": command, "cwd": str(BASE),
                         "returncode": native.returncode,
                         "stdout": native.stdout, "stderr": native.stderr},
        "calls": [],
    }
    real_loader = loader.read_limit
    real_open = io.open

    def observe(instance, identity, root, filename="settings.txt", *, default=False,
                action="construct"):
        row = {
            "client": identity, "action_before_load": action,
            "requested_root": str(BASE / root), "requested_filename": filename,
            "call_style": "load()" if default else "load(filename)",
            "client_root": str(instance.root),
            "client_read_root": str(instance._read_root),
            "expected_path": str(BASE / root / filename),
            "expected_value": {("alpha", "settings.txt"): 111,
                               ("alpha", "other.txt"): 333,
                               ("beta", "settings.txt"): 222,
                               ("beta", "other.txt"): 444}[(root, filename)],
            "loader_inputs": [], "physical_files_opened": [], "reads": [],
            "events": [],
        }

        class ObservedFile:
            def __init__(self, handle, physical):
                self.handle = handle
                self.physical = physical

            def __enter__(self):
                self.handle.__enter__()
                return self

            def __exit__(self, *args):
                return self.handle.__exit__(*args)

            def __getattr__(self, name):
                return getattr(self.handle, name)

            def read(self, *args, **kwargs):
                value = self.handle.read(*args, **kwargs)
                event = {"event": "file_read", "physical_path": self.physical,
                         "text": value}
                row["reads"].append(event)
                row["events"].append(event)
                return value

        def observed_open(path, *args, **kwargs):
            handle = real_open(path, *args, **kwargs)
            physical = str(Path(path).resolve())
            stat = os.fstat(handle.fileno())
            event = {"event": "file_open", "input": os.fspath(path),
                     "physical_path": physical, "device": stat.st_dev,
                     "inode": stat.st_ino}
            row["physical_files_opened"].append(event)
            row["events"].append(event)
            return ObservedFile(handle, physical)

        def observed_loader(path):
            row["loader_inputs"].append(os.fspath(path))
            row["events"].append({"event": "loader_call", "input": os.fspath(path)})
            value = real_loader(path)
            row["events"].append({"event": "loader_return", "value": value})
            return value

        with patch.object(loader, "read_limit", observed_loader), \
                patch.object(io, "open", observed_open):
            value = instance.load() if default else instance.load(filename)
        row["returned_value"] = value
        row["matches_requirement"] = value == row["expected_value"]
        row["events"].append({"event": "client_return", "value": value})
        trace["calls"].append(row)

    observe(client.Client(BASE / "alpha"), "single_root_control", "alpha", default=True)
    observe(client.Client(BASE / "alpha"), "other_filename_control", "alpha", "other.txt")
    switching = client.Client(BASE / "alpha")
    for index, root in enumerate(("alpha", "beta", "alpha")):
        action = "construct"
        if index:
            switching.select_root(BASE / root)
            action = "select_root"
        observe(switching, "switching", root, default=True, action=action)
        observe(switching, "switching", root, "other.txt", action="same selected root")
    fresh = client.Client(BASE / "beta")
    observe(fresh, "fresh_beta", "beta", default=True)
    observe(fresh, "fresh_beta", "beta", "other.txt", action="same selected root")

    after = hashes()
    trace["original_files"] = {"sha256_before": before, "sha256_after": after,
                               "unchanged": before == after}
    target = BASE / "probe_trace.json"
    target.write_text(json.dumps(trace, indent=2) + "\n")
    assert before == after, "A supplied file changed"
    assert [row["returned_value"] for row in trace["calls"]] == [
        111, 333, 111, 333, 111, 333, 111, 333, 222, 444,
    ], "Reproduction changed; inspect trace"
    assert all(len(row["reads"]) == 1 for row in trace["calls"])
    assert native.returncode == 1 and "Ran 3 tests" in native.stderr
    assert "FAILED (failures=1)" in native.stderr
    print(f"Trace: {target.name}; native tests: 2 pass, 1 expected reproduction failure")
    for row in trace["calls"]:
        actual = Path(row["loader_inputs"][0]).relative_to(BASE)
        print(f"{row['client']}: {Path(row['requested_root']).name}/"
              f"{row['requested_filename']} -> loader/read {actual} -> "
              f"{row['returned_value']} (expected {row['expected_value']})")


if __name__ == "__main__":
    main()
