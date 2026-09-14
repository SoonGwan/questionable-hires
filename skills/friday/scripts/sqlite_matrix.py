#!/usr/bin/env python3
"""Execute a local SQLite compatibility matrix; never open a database file."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import time


def literal_reader(reference, root, remaining):
    """Read a declaration-only module without importing or executing it."""
    if (not isinstance(reference, dict) or set(reference) != {'python_file', 'constant'}
            or not all(isinstance(value, str) and value for value in reference.values())):
        raise ValueError('reader reference requires python_file and constant strings')
    relative = Path(reference['python_file'])
    if relative.is_absolute() or not relative.parts or '..' in relative.parts:
        raise ValueError('reader file must be project-relative')
    path = root / relative
    if any(part.is_symlink() for part in [path, *path.parents]
           if part != root and root in part.parents):
        raise ValueError('symlink reader paths are not supported')
    if not path.is_file() or path.stat().st_size > 1_000_000:
        raise ValueError('reader file missing or exceeds 1 MB')
    if path.stat().st_size > remaining:
        raise ValueError('SQL exceeds 2 MB')
    with path.open('rb') as stream:
        source = stream.read(min(1_000_000, remaining) + 1)
    if len(source) > 1_000_000:
        raise ValueError('reader file exceeds 1 MB')
    if len(source) > remaining:
        raise ValueError('SQL exceeds 2 MB')
    try:
        tree = ast.parse(source, filename=relative.as_posix())
    except (SyntaxError, ValueError, RecursionError) as error:
        raise ValueError('cannot parse reader module: ' + str(error)) from error
    constants = {}
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            continue  # A module docstring has no query-binding side effect.
        if (not isinstance(node, ast.Assign) or len(node.targets) != 1
                or not isinstance(node.targets[0], ast.Name)
                or not isinstance(node.value, ast.Constant)):
            raise ValueError('reader module must contain only unique scalar literal assignments and docstrings')
        name = node.targets[0].id
        if name in constants:
            raise ValueError('reader module reassigns a constant: ' + name)
        constants[name] = (node.value.value, node.lineno)
    selected = constants.get(reference['constant'])
    if selected is None or not isinstance(selected[0], str):
        raise ValueError('selected reader constant must be a literal SQL string')
    query, line = selected
    return query, len(source), {'python_file': relative.as_posix(),
                               'constant': reference['constant'], 'line': line,
                               'sha256': hashlib.sha256(source).hexdigest(),
                               'query': query, 'kind': 'static literal, not runtime binding evidence'}


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
    if any(not isinstance(k, str) or not isinstance(v, (str, dict)) for k, v in checks.items()):
        raise ValueError("checks map names to SQL strings or literal reader references")
    total = sum(len(s.encode("utf-8")) for s in checks.values() if isinstance(s, str))
    if total > 2_000_000:
        raise ValueError("SQL exceeds 2 MB")
    root = Path(root).resolve(strict=True)
    resolved, sources = {}, {}
    for label, value in checks.items():
        if isinstance(value, str):
            resolved[label] = value
        else:
            query, source_bytes, provenance = literal_reader(value, root, 2_000_000 - total)
            total += source_bytes + len(query.encode('utf-8'))
            if total > 2_000_000:
                raise ValueError('SQL exceeds 2 MB')
            resolved[label], sources[label] = query, provenance
    checks = resolved
    prepared = []
    for phase in phases:
        if not isinstance(phase, dict) or set(phase) != {"name", "files", "sql"}:
            raise ValueError("each phase requires name, files and sql")
        if not isinstance(phase["name"], str) or not phase["name"]:
            raise ValueError("phase name must be nonempty text")
        if not isinstance(phase["files"], list) or not isinstance(phase["sql"], str):
            raise ValueError("files must be a list; sql must be text")
        total += len(phase["sql"].encode("utf-8"))
        if total > 2_000_000:
            raise ValueError("SQL exceeds 2 MB")
        chunks = []
        for filename in phase["files"]:
            relative = Path(filename)
            if relative.is_absolute() or not relative.parts or ".." in relative.parts:
                raise ValueError("SQL files must be relative to source")
            path = root / relative
            if any(part.is_symlink() for part in [path, *path.parents] if part != root and root in part.parents):
                raise ValueError("symlink SQL paths are not supported")
            if not path.is_file():
                raise ValueError("SQL file missing or exceeds 1 MB")
            length = path.stat().st_size
            if length > 1_000_000:
                raise ValueError("SQL file missing or exceeds 1 MB")
            if total + length > 2_000_000:
                raise ValueError("SQL exceeds 2 MB")
            # Preserve original bytes (including CRLF) and bound a read even if
            # the file grows after stat. Repeated selections count each time.
            with path.open("rb") as stream:
                data = stream.read(min(1_000_000, 2_000_000 - total) + 1)
            if len(data) > 1_000_000:
                raise ValueError("SQL file missing or exceeds 1 MB")
            total += len(data)
            if total > 2_000_000:
                raise ValueError("SQL exceeds 2 MB")
            chunks.append(data.decode("utf-8"))
        chunks.append(phase["sql"])
        prepared.append((phase["name"], chunks))

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
    db.execute("PRAGMA temp_store=MEMORY")
    db.set_authorizer(authorize)
    deadline = time.monotonic() + timeout
    db.set_progress_handler(lambda: int(time.monotonic() >= deadline), 1000)
    output = {"engine": "sqlite-memory", "complete": True, "phases": []}
    if sources:
        output['reader_sources'] = sources
    try:
        for name, chunks in prepared:
            row = {"name": name, "checks": {}}
            output["phases"].append(row)
            try:
                for sql in chunks:
                    if time.monotonic() >= deadline:
                        output["complete"] = False
                        output["error"] = "time budget exhausted"
                        break
                    db.executescript(sql)
            except sqlite3.Error as error:
                row["migration_error"] = str(error)
                output["complete"] = False
                break  # Never label a partially applied migration as the next state.
            if not output["complete"]:
                break
            readonly = True
            for label, query in checks.items():
                # SQLite's progress callback need not run for a short statement.
                # Do not start another check after the shared budget is exhausted.
                if time.monotonic() >= deadline:
                    break
                try:
                    cursor = db.execute(query)
                    if cursor.description is None:
                        row['checks'][label] = {'ok': False, 'error':
                            'Reader produced no result set; empty/comment-only SQL is not a check'}
                        continue
                    rows = cursor.fetchmany(21)
                    row["checks"][label] = {"ok": True, "rows": rows[:20],
                                             "columns": [column[0] for column in cursor.description],
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


def format_result(result):
    """Serialize collected observations exactly as the CLI, including BLOBs.

    Does not run SQL, change result, or establish compatibility.
    """
    def encode(value):
        if isinstance(value, bytes):
            return {"blob_hex": value.hex()}
        raise TypeError("Unsupported result value: " + type(value).__name__)
    return json.dumps(result, ensure_ascii=True, default=encode)


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
        if len(raw.encode("utf-8")) > 2_000_000:
            raise ValueError("recipe exceeds 2 MB")
        result = matrix(json.loads(raw), args.source, args.timeout)
        print(format_result(result))
        return 0 if result["complete"] else 1
    except (ValueError, OSError, TypeError) as error:
        print(json.dumps({"complete": False, "error": str(error)}))
        return 2


if __name__ == "__main__":
    sys.exit(main())
