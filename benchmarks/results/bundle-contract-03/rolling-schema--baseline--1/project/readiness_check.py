"""Local, dependency-free schema/read compatibility and rollback probe."""

import ast
import hashlib
import json
from pathlib import Path
import sqlite3


ROOT = Path(__file__).resolve().parent
RELEASE_FILES = (
    "001_initial.sql", "002_up.sql", "002_down.sql",
    "old_reader.py", "new_reader.py", "release.md",
)


def hashes():
    return {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in RELEASE_FILES
    }


def reader_query(name):
    tree = ast.parse((ROOT / name).read_text())
    assignments = [
        node for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "QUERY" for t in node.targets)
    ]
    assert len(assignments) == 1
    query = ast.literal_eval(assignments[0].value)
    assert isinstance(query, str)
    return query


def main():
    before = hashes()
    queries = {name: reader_query(name) for name in ("old_reader.py", "new_reader.py")}
    db = sqlite3.connect(":memory:")
    snapshots = []

    def snapshot(state, working_reader, expected_rows):
        result = {
            "state": state,
            "schema": db.execute("PRAGMA table_info(users)").fetchall(),
            "stored_rows": db.execute("SELECT * FROM users ORDER BY id").fetchall(),
            "readers": {},
        }
        assert result["stored_rows"] == expected_rows
        for name, query in queries.items():
            try:
                rows = db.execute(query).fetchall()
            except sqlite3.OperationalError as error:
                result["readers"][name] = {"error": str(error)}
                assert name != working_reader
                missing = "name" if name == "old_reader.py" else "display_name"
                assert str(error) == "no such column: " + missing
            else:
                result["readers"][name] = {"rows": rows}
                assert name == working_reader
                assert sorted(rows) == expected_rows
        snapshots.append(result)

    db.executescript((ROOT / "001_initial.sql").read_text())
    db.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "Alice"), (2, "Bob")])
    db.commit()
    snapshot("initial", "old_reader.py", [(1, "Alice"), (2, "Bob")])

    db.executescript((ROOT / "002_up.sql").read_text())
    snapshot("up_before_writes", "new_reader.py", [(1, "Alice"), (2, "Bob")])

    # Synthetic SQL probes, not evidence about an application writer.
    probe_sql = [
        "INSERT INTO users (id, display_name) VALUES (3, 'Carol')",
        "UPDATE users SET display_name = 'Alicia' WHERE id = 1",
        "UPDATE users SET display_name = 'Caroline' WHERE id = 3",
    ]
    for statement in probe_sql:
        db.execute(statement)
    db.commit()
    expected = [(1, "Alicia"), (2, "Bob"), (3, "Caroline")]
    snapshot("up_after_writes_before_rollback", "new_reader.py", expected)

    db.executescript((ROOT / "002_down.sql").read_text())
    snapshot("down_after_writes", "old_reader.py", expected)
    db.close()
    assert hashes() == before, "Release files changed during verification"
    print(json.dumps({
        "sqlite_version": sqlite3.sqlite_version,
        "database": ":memory:",
        "queries": queries,
        "synthetic_new_schema_writes": probe_sql,
        "states": snapshots,
        "release_sha256": before,
        "release_files_unchanged": True,
        "assertions": "passed",
    }, indent=2))


if __name__ == "__main__":
    main()
