"""Run with python3 -B probe_paths.py; writes probe_trace.json beside this file.

Calls the supplied Client and cached loader unchanged. Instrumentation delegates
to the original functions; cache clears are explicit experimental boundaries.
No threads, network, third-party packages, or supplied-file writes are used.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
import client
import loader

SUPPLIED = (
    "client.py", "loader.py", "test_paths.py", "requirements.md",
    "alpha/settings.txt", "alpha/other.txt",
    "beta/settings.txt", "beta/other.txt",
)


def hashes():
    return {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
            for name in SUPPLIED}


def main():
    before = hashes()
    native = subprocess.run(
        ["python3", "-B", "-m", "unittest", "-v", "test_paths"],
        cwd=BASE, capture_output=True, text=True, check=False,
    )
    trace = {
        "scope": "Supplied synthetic application, sequential local process only",
        "native_tests": {
            "command": "python3 -B -m unittest -v test_paths",
            "returncode": native.returncode,
            "stdout": native.stdout, "stderr": native.stderr,
        },
        "events": [],
    }
    events = trace["events"]
    cached_loader = loader.read_limit
    original_read_text = Path.read_text
    original_open = io.open
    active = None

    def observed_open(file, *args, **kwargs):
        handle = original_open(file, *args, **kwargs)
        if active is not None:
            stat = os.fstat(handle.fileno())
            active["physical_opens"].append({
                "open_argument": os.fspath(file),
                "resolved_path": str(Path(file).resolve()),
                "device": stat.st_dev, "inode": stat.st_ino,
            })
        return handle

    def observed_read_text(path, *args, **kwargs):
        resolved = str(path.resolve())
        result = original_read_text(path, *args, **kwargs)
        if active is not None:
            active["physical_reads"].append({
                "path_argument": str(path), "resolved_path": resolved,
                "text_returned": result,
            })
        return result

    def observed_loader(filename):
        call = {
            "argument": filename, "argument_type": type(filename).__name__,
            "cwd": str(Path.cwd()),
            "resolved_candidate": str(Path(filename).resolve()),
            "cache_before": cached_loader.cache_info()._asdict(),
        }
        active["loader_calls"].append(call)
        result = cached_loader(filename)
        call.update(returned=result,
                    cache_after=cached_loader.cache_info()._asdict())
        return result

    def clear(reason):
        events.append({"action": "cache_clear", "reason": reason,
                       "cache_before": cached_loader.cache_info()._asdict()})
        cached_loader.cache_clear()

    def load(label, instance, expected, observed, filename=None):
        nonlocal active
        cwd = str(Path.cwd())
        active = {
            "action": "load", "label": label,
            "requested_root": str(instance.root),
            "requested_filename": filename or "settings.txt",
            "uses_default_filename": filename is None,
            "expected_by_contract": expected,
            "loader_calls": [], "physical_opens": [], "physical_reads": [],
            "cwd_before": cwd,
        }
        events.append(active)
        result = instance.load() if filename is None else instance.load(filename)
        active.update(returned=result, matches_contract=result == expected,
                      cwd_after=str(Path.cwd()))
        active["cwd_restored"] = active["cwd_after"] == cwd
        assert result == observed, (label, result, observed)
        assert active["cwd_restored"]
        active = None

    def select(label, instance, root):
        previous = str(instance.root)
        instance.select_root(BASE / root)
        events.append({"action": "select_root", "client": label,
                       "requested_root": str(BASE / root),
                       "previous_root": previous, "selected_root": str(instance.root)})

    with patch.object(loader, "read_limit", observed_loader), \
            patch.object(Path, "read_text", observed_read_text), \
            patch.object(io, "open", observed_open):
        for root, settings, other in (("alpha", 111, 333), ("beta", 222, 444)):
            clear("Isolated single-root and other-filename controls: " + root)
            instance = client.Client(BASE / root)
            load(root + " cold settings control", instance, settings, settings)
            load(root + " repeated settings control", instance, settings, settings)
            load(root + " other-filename control", instance, other, other, "other.txt")

        clear("Begin one-client alpha -> beta -> alpha sequence")
        shared = client.Client(BASE / "alpha")
        load("shared alpha settings", shared, 111, 111)
        load("shared alpha other", shared, 333, 333, "other.txt")
        select("shared", shared, "beta")
        load("shared beta settings", shared, 222, 111)
        load("shared beta other", shared, 444, 333, "other.txt")
        select("shared", shared, "alpha")
        load("shared alpha return settings", shared, 111, 111)
        load("shared alpha return other", shared, 333, 333, "other.txt")
        fresh = client.Client(BASE / "beta")
        load("fresh beta settings with warm cache", fresh, 222, 111)
        load("fresh beta other with warm cache", fresh, 444, 333, "other.txt")
        clear("Discriminating intervention: same fresh beta client and requests")
        load("same fresh beta settings after clear", fresh, 222, 222)
        load("same fresh beta other after clear", fresh, 444, 444, "other.txt")

    after = hashes()
    trace.update(supplied_sha256_before=before, supplied_sha256_after=after,
                 supplied_files_unchanged=before == after)
    assert before == after
    output = BASE / "probe_trace.json"
    output.write_text(json.dumps(trace, indent=2) + "\n")
    print(native.stderr, end="")
    print("Probe assertions passed; supplied file hashes unchanged.")
    print("Trace:", output)


if __name__ == "__main__":
    main()
