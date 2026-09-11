#!/usr/bin/env python3
"""Execute a local SQLite compatibility matrix; never open a database file."""
import argparse
import json
from pathlib import Path
import sqlite3
import sys
import time


def matrix(spec, root, timeout=5):
    """Each phase changes one in-memory DB; checks cannot change its state."""
    if not isinstance(spec, dict) or set(spec) != {"phases", "checks"}:
        raise ValueError("spec requires only phases and checks")
    phases, checks = spec["phases"], spec["checks"]
    if not isinstance(phases, list) or not 1 <= len(phases) <= 20:
        raise ValueError("provide 1..20 phases")
    if not isinstance(checks, dict) or not 1 <= len(checks) <= 20:
        raise ValueError("provide 1..20 named read queries")
    if not 0 < timeout <= 30:
        raise ValueError("timeout must be in (0, 30]")
    root = Path(root).resolve(strict=True)
    prepared = []
    for phase in phases:
        if not isinstance(phase, dict) or set(phase) != {"name", "files", "sql"}:
            raise ValueError("each phase requires name, files and sql")
        if not isinstance(phase["name"], str) or not phase["name"]:
            raise ValueError("phase name must be nonempty text")
        if not isinstance(phase["files"], list) or not isinstance(phase["sql"], str):
            raise ValueError("files must be a list; sql must be text")
        chunks = []
        for filename in phase["files"]:
            relative = Path(filename)
            if relative.is_absolute() or not relative.parts or ".." in relative.parts:
                raise ValueError("SQL files must be relative to source")
            path = root / relative
            if any(part.is_symlink() for part in [path, *path.parents] if part != root and root in part.parents):
                raise ValueError("symlink SQL paths are not supported")
            if not path.is_file() or path.stat().st_size > 1_000_000:
                raise ValueError("SQL file missing or exceeds 1 MB")
            chunks.append(path.read_text(encoding="utf-8"))
        chunks.append(phase["sql"])
        prepared.append((phase["name"], chunks))
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in checks.items()):
        raise ValueError("checks map names to SQL strings")
    if sum(len(s) for _, chunks in prepared for s in chunks) + sum(map(len, checks.values())) > 2_000_000:
        raise ValueError("SQL exceeds 2 MB")

    readonly = False
    allowed_reads = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ, sqlite3.SQLITE_FUNCTION,
                     sqlite3.SQLITE_RECURSIVE}

    def authorize(action, arg1, arg2, database, trigger):
        if action in {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH, sqlite3.SQLITE_PRAGMA}:
            return sqlite3.SQLITE_DENY
        if action == sqlite3.SQLITE_FUNCTION and (arg2 or "").lower() == "load_extension":
            return sqlite3.SQLITE_DENY
        if readonly and action not in allowed_reads:
            return sqlite3.SQLITE_DENY
        return sqlite3.SQLITE_OK

    # Disable statement caching so a statement authorized in a migration cannot
    # reuse that authorization when later submitted as a read-only check.
    db = sqlite3.connect(":memory:", cached_statements=0)
    db.set_authorizer(authorize)
    deadline = time.monotonic() + timeout
    db.set_progress_handler(lambda: int(time.monotonic() >= deadline), 1000)
    output = {"engine": "sqlite-memory", "complete": True, "phases": []}
    try:
        for name, chunks in prepared:
            row = {"name": name, "checks": {}}
            output["phases"].append(row)
            try:
                for sql in chunks:
                    db.executescript(sql)
            except sqlite3.Error as error:
                row["migration_error"] = str(error)
                output["complete"] = False
                break  # Never label a partially applied migration as the next state.
            readonly = True
            for label, query in checks.items():
                try:
                    cursor = db.execute(query)
                    rows = cursor.fetchmany(21)
                    row["checks"][label] = {"ok": True, "rows": rows[:20],
                                             "truncated": len(rows) > 20}
                except sqlite3.Error as error:
                    row["checks"][label] = {"ok": False, "error": str(error)}
            readonly = False
            if time.monotonic() >= deadline:
                output["complete"] = False
                output["error"] = "time budget exhausted"
                break
    finally:
        db.close()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", required=True, help="JSON recipe path, or - for stdin")
    parser.add_argument("--source", default=".", help="root for relative SQL files")
    parser.add_argument("--timeout", type=float, default=5, help="SQL time budget, at most 30 seconds")
    args = parser.parse_args()
    try:
        if args.spec == "-":
            raw = sys.stdin.read(2_000_001)
        else:
            with open(args.spec, encoding="utf-8") as stream:
                raw = stream.read(2_000_001)
        if len(raw) > 2_000_000:
            raise ValueError("recipe exceeds 2 MB")
        result = matrix(json.loads(raw), args.source, args.timeout)
        print(json.dumps(result, ensure_ascii=True, default=lambda v: {"blob_hex": v.hex()}))
        return 0 if result["complete"] else 1
    except (ValueError, OSError, TypeError) as error:
        print(json.dumps({"complete": False, "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
