"""Observe the supplied implementation; run with python3 -B experiments/probe_paths.py."""
import hashlib
import json
from pathlib import Path
import sys
from unittest.mock import patch

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from client import Client
import loader


def main():
    original_loader = loader.read_limit
    original_read_text = Path.read_text
    events = []
    active = None

    def record_loader(filename):
        call = {
            "input": filename,
            "cwd": str(Path.cwd()),
            "effective_path_if_read": str(Path(filename).resolve()),
            "cache_before": original_loader.cache_info()._asdict(),
        }
        active["loader_calls"].append(call)
        result = original_loader(filename)
        call["returned"] = result
        call["cache_after"] = original_loader.cache_info()._asdict()
        return result

    def record_read_text(path, *args, **kwargs):
        resolved = path.resolve()
        stat = resolved.stat()
        result = original_read_text(path, *args, **kwargs)
        active["physical_reads"].append({
            "path_argument": str(path),
            "resolved_path": str(resolved),
            "device": stat.st_dev,
            "inode": stat.st_ino,
            "text": result,
        })
        return result

    def request(label, client_id, client, root, filename, expected, observed):
        nonlocal active
        client.select_root(BASE / root)
        before = Path.cwd()
        active = {
            "label": label, "client": client_id,
            "requested_root": str(BASE / root),
            "selected_root": str(client.root),
            "requested_filename": filename, "expected": expected,
            "loader_calls": [], "physical_reads": [],
        }
        events.append(active)
        active["returned"] = client.load(filename)
        active["matches_requirement"] = active["returned"] == expected
        active["cwd_restored"] = Path.cwd() == before
        active["probe_check_passed"] = (
            active["returned"] == observed and active["cwd_restored"]
        )
        active = None

    original_loader.cache_clear()
    events.append({"action": "cache_clear", "reason": "deterministic initial baseline"})
    try:
        with patch.object(loader, "read_limit", record_loader), patch.object(Path, "read_text", record_read_text):
            shared = Client(BASE / "alpha")
            request("single-root control", "shared", shared, "alpha", "settings.txt", 111, 111)
            request("repeat single-root control", "shared", shared, "alpha", "settings.txt", 111, 111)
            request("other-filename control", "shared", shared, "alpha", "other.txt", 333, 333)
            request("switch to beta", "shared", shared, "beta", "settings.txt", 222, 111)
            request("switch back to alpha", "shared", shared, "alpha", "settings.txt", 111, 111)
            fresh = Client(BASE / "beta")
            request("fresh beta client", "fresh_beta", fresh, "beta", "settings.txt", 222, 111)
            request("fresh beta other filename", "fresh_beta", fresh, "beta", "other.txt", 444, 333)
            original_loader.cache_clear()
            events.append({"action": "cache_clear", "reason": "hold beta client/root/filename fixed; change only cache state"})
            request("beta after cache clear", "fresh_beta", fresh, "beta", "settings.txt", 222, 222)
            request("beta other-filename cold control", "fresh_beta", fresh, "beta", "other.txt", 444, 444)
    finally:
        original_loader.cache_clear()

    manifest = json.loads((BASE / "experiments/original_hashes.json").read_text())
    unchanged = all(hashlib.sha256((BASE / name).read_bytes()).hexdigest() == digest
                    for name, digest in manifest.items())
    passed = unchanged and all(e.get("probe_check_passed", True) for e in events)
    trace = BASE / "experiments/paths_trace.json"
    trace.write_text(json.dumps({
        "scope": "Sequential local supplied client and cached loader; wrappers delegate unchanged calls.",
        "read_observation": "Successful real Path.read_text calls, resolved filesystem identity and contents; empty list means no loader file read.",
        "original_files_unchanged": unchanged,
        "probe_checks_passed": passed,
        "events": events,
    }, indent=2) + "\n")
    print(f"Trace: {trace}")
    for event in events:
        if "returned" in event:
            print(f"{event['label']}: {Path(event['requested_root']).name}/{event['requested_filename']} -> {event['returned']} (expected {event['expected']}; reads={len(event['physical_reads'])})")
    print(f"Probe checks passed: {passed}; original files unchanged: {unchanged}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
