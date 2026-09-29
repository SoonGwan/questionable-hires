"""Run with python3 -B probe_paths.py; write evidence to trace_paths.json.

Recording wrappers delegate to the supplied loader and real Path.open/read.
No fixture, client, or loader implementation is replaced or modified on disk.
"""
import hashlib
import json
import os
from pathlib import Path
from unittest.mock import patch

from client import Client
import loader


BASE = Path(__file__).resolve().parent
TRACE = BASE / "trace_paths.json"
SUPPLIED = ["client.py", "loader.py", "test_paths.py", "requirements.md",
            "alpha/settings.txt", "alpha/other.txt",
            "beta/settings.txt", "beta/other.txt"]


def hashes():
    return {name: hashlib.sha256((BASE / name).read_bytes()).hexdigest()
            for name in SUPPLIED}


def main():
    before = hashes()
    events = []
    active = None
    original_loader = loader.read_limit
    original_open = Path.open

    class RecordingFile:
        def __init__(self, stream, event):
            self.stream, self.event = stream, event

        def __enter__(self):
            self.stream.__enter__()
            return self

        def __exit__(self, *args):
            return self.stream.__exit__(*args)

        def __getattr__(self, name):
            return getattr(self.stream, name)

        def read(self, *args, **kwargs):
            value = self.stream.read(*args, **kwargs)
            self.event["reads"].append({"operation": "read", "text": value})
            return value

    def recording_open(path, *args, **kwargs):
        stream = original_open(path, *args, **kwargs)
        if active is None:
            return stream
        stat = os.fstat(stream.fileno())
        event = {"path": str(path), "resolved_path": str(path.resolve()),
                 "device": stat.st_dev, "inode": stat.st_ino, "reads": []}
        active["file_opens"].append(event)
        return RecordingFile(stream, event)

    def recording_loader(filename):
        event = {"input": str(filename)}
        active["loader_calls"].append(event)
        value = original_loader(filename)
        event["returned_value"] = value
        return value

    def observe(client, client_id, root, filename, expected, observed, action,
                default_filename=False):
        nonlocal active
        event = {"sequence": len(events) + 1, "client_id": client_id,
                 "action": action, "requested_root": str(BASE / root),
                 "requested_filename": filename,
                 "filename_argument_omitted": default_filename,
                 "client_root": str(client.root),
                 "client_read_root": str(client._read_root),
                 "expected_value": expected, "loader_calls": [], "file_opens": []}
        events.append(event)
        active = event
        try:
            value = client.load() if default_filename else client.load(filename)
            event["returned_value"] = value
            event["matches_requirement"] = value == expected
        except Exception as exc:
            event["exception"] = repr(exc)
            raise
        finally:
            active = None
            event["read_observed"] = any(f["reads"] for f in event["file_opens"])
        assert value == observed, event
        assert len(event["loader_calls"]) == len(event["file_opens"]) == 1, event
        opened = event["file_opens"][0]
        assert opened["resolved_path"] == event["loader_calls"][0]["input"], event
        assert int(opened["reads"][0]["text"]) == value, event

    failure = None
    try:
        with patch.object(loader, "read_limit", recording_loader), \
                patch.object(Path, "open", recording_open):
            control = Client(BASE / "alpha")
            observe(control, "single_alpha", "alpha", "settings.txt", 111, 111,
                    "construct(alpha)", True)
            observe(control, "single_alpha", "alpha", "other.txt", 333, 333,
                    "same root")
            shared = Client(BASE / "alpha")
            for index, root in enumerate(("alpha", "beta", "alpha")):
                action = "construct(alpha)"
                if index:
                    shared.select_root(BASE / root)
                    action = "select_root(" + root + ")"
                observe(shared, "shared", root, "settings.txt",
                        111 if root == "alpha" else 222, 111, action, True)
                observe(shared, "shared", root, "other.txt",
                        333 if root == "alpha" else 444, 333, "same root")
            fresh = Client(BASE / "beta")
            observe(fresh, "fresh_beta", "beta", "settings.txt", 222, 222,
                    "construct(beta)", True)
            observe(fresh, "fresh_beta", "beta", "other.txt", 444, 444, "same root")
        assert [e["sequence"] for e in events if not e["matches_requirement"]] == [5, 6]
    except Exception as exc:
        failure = repr(exc)
    after = hashes()
    unchanged = before == after
    report = {
        "command": "python3 -B probe_paths.py",
        "scope": "Sequential supplied local implementation; no production observation",
        "instrumentation": "Delegating loader.read_limit and Path.open wrappers; real stream.read and fstat",
        "read_evidence_limit": "Filesystem stream reads, not proof of physical disk I/O versus OS caching",
        "source_files": {"client": str(BASE / "client.py"), "loader": str(BASE / "loader.py")},
        "supplied_hashes_before": before, "supplied_hashes_after": after,
        "supplied_files_unchanged": unchanged, "probe_failure": failure,
        "events": events,
    }
    TRACE.write_text(json.dumps(report, indent=2) + "\n")
    print("Trace:", TRACE)
    for event in events:
        print("{sequence}: {client_id} {requested_filename} root={client_root} "
              "expected={expected_value} returned={returned_value} read={read_observed}".format(**event))
    print("Probe failure:", failure, "Supplied files unchanged:", unchanged)
    if failure or not unchanged:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
