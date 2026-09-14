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


def literal_reader(reference, root, remaining, cache=None):
    """Read a declaration-only module without importing or executing it."""
    if (not isinstance(reference, dict) or set(reference) != {'python_file', 'constant'}
            or not all(isinstance(value, str) and value for value in reference.values())):
        raise ValueError('reader reference requires python_file and constant strings')
    relative = Path(reference['python_file'])
    if relative.is_absolute() or not relative.parts or '..' in relative.parts:
        raise ValueError('reader file must be project-relative')
    key = relative.as_posix()
    if cache is not None and key in cache:
        constants, length, digest = cache[key]
        if length > remaining:
            raise ValueError('SQL exceeds 2 MB')
    else:
        constants, length, digest = reader_constants(relative, root, remaining)
        if cache is not None:
            cache[key] = constants, length, digest
    selected = constants.get(reference['constant'])
    if selected is None or not isinstance(selected[0], str):
        raise ValueError('selected reader constant must be a literal SQL string')
    query, line = selected
    return query, length, {'python_file': key,
                           'constant': reference['constant'], 'line': line,
                           'sha256': digest, 'query': query,
                           'kind': 'static literal, not runtime binding evidence'}


def reader_constants(relative, root, remaining):
    """One bounded declaration snapshot; no imports or SQL execution."""
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
    return constants, len(source), hashlib.sha256(source).hexdigest()


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
    resolved, sources, reader_cache = {}, {}, {}
    for label, value in checks.items():
        if isinstance(value, str):
            resolved[label] = value
        else:
            query, source_bytes, provenance = literal_reader(value, root, 2_000_000 - total, reader_cache)
            total += source_bytes + len(query.encode('utf-8'))
            if total > 2_000_000:
                raise ValueError('SQL exceeds 2 MB')
            resolved[label], sources[label] = query, provenance
    checks = resolved
    reader_cache.clear()  # Keep selected queries/provenance, not unused constants.
    prepared = []
    for phase in phases:
        if (not isinstance(phase, dict) or "name" not in phase
                or set(phase) - {"name", "files", "sql", "checks"}):
            raise ValueError("each phase requires name; only files, sql and checks are optional")
        if not isinstance(phase["name"], str) or not phase["name"]:
            raise ValueError("phase name must be nonempty text")
        selected = phase.get('checks', list(checks))
        if (not isinstance(selected, list) or not selected
                or any(not isinstance(label, str) or label not in checks for label in selected)
                or len(set(selected)) != len(selected)):
            raise ValueError('phase checks must be a nonempty list of unique declared check names')
        files, sql = phase.get("files", []), phase.get("sql", "")
        if not isinstance(files, list) or not isinstance(sql, str):
            raise ValueError("files must be a list; sql must be text")
        total += len(sql.encode("utf-8"))
        if total > 2_000_000:
            raise ValueError("SQL exceeds 2 MB")
        chunks = []
        for filename in files:
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
        chunks.append(sql)
        prepared.append((phase["name"], chunks, selected))

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
        for name, chunks, selected in prepared:
            row = {"name": name, "checks": {}}
            if selected != list(checks):
                row['selected_checks'] = list(selected)
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
            for label in selected:
                query = checks[label]
                # SQLite's progress callback need not run for a short statement.
                # Do not start another check after the shared budget is exhausted.
                if time.monotonic() >= deadline:
                    break
                cursor = None
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
                finally:
                    # A bounded fetch may leave this statement active. Release
                    # its read lock before a following phase changes the schema.
                    if cursor is not None:
                        cursor.close()
            readonly = False
            if time.monotonic() >= deadline:
                output["complete"] = False
                output["error"] = "time budget exhausted"
                break
    finally:
        db.close()
    return output


def assert_rows(result, phase_index, check, *, columns, rows):
    """Assert one selected native observation; never execute SQL or infer readiness.

    Explicit raises remain active under python -O. Ordered values use Python
    equality, retaining native BLOB bytes and duplicate column labels.
    """
    if (type(phase_index) is not int or phase_index < 0
            or phase_index >= len(result['phases'])):
        raise ValueError('phase_index must identify an observed phase (zero based)')
    if (not isinstance(columns, (list, tuple))
            or any(not isinstance(column, str) for column in columns)
            or not isinstance(rows, (list, tuple))
            or any(not isinstance(row, (list, tuple)) or len(row) != len(columns) for row in rows)):
        raise ValueError('provide ordered columns and equally wide list/tuple rows')
    if result.get('complete') is not True:
        raise AssertionError('matrix incomplete; inspect recorded errors and unrun phases')
    phase = result['phases'][phase_index]
    context = f"phase {phase_index} ({phase['name']!r}), check {check!r}"
    if check not in phase['checks']:
        raise AssertionError(context + ': check unrun')
    observed = phase['checks'][check]
    if observed.get('ok') is not True:
        raise AssertionError(context + ': reader failed: ' + observed.get('error', 'unknown error'))
    if observed.get('truncated') is not False:
        raise AssertionError(context + ': rows truncated or completeness unknown')
    expected_columns, expected_rows = list(columns), [tuple(row) for row in rows]
    if observed['columns'] != expected_columns:
        raise AssertionError(f"{context}: columns expected {expected_columns!r}, observed {observed['columns']!r}")
    actual_rows = [tuple(row) for row in observed['rows']]
    if actual_rows != expected_rows:
        raise AssertionError(f'{context}: rows expected {expected_rows!r}, observed {actual_rows!r}')


def format_result(result):
    """Serialize collected observations exactly as the CLI, including BLOBs.

    Does not run SQL, change result, or establish compatibility.
    """
    def encode(value):
        if isinstance(value, bytes):
            return {"blob_hex": value.hex()}
        raise TypeError("Unsupported result value: " + type(value).__name__)
    return json.dumps(result, ensure_ascii=True, default=encode, separators=(',', ':'))


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
