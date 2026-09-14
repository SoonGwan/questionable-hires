"""Local SQLite verification; release files are read only and DB stays in memory."""
import ast
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
FILES = ["001_initial.sql", "002_up.sql", "002_down.sql", "old_reader.py", "new_reader.py", "release.md"]


def fingerprints():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def query_from(name):
    tree = ast.parse((ROOT / name).read_text())
    return next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "QUERY" for t in node.targets))


before = fingerprints()
queries = {name: query_from(name) for name in ("old_reader.py", "new_reader.py")}
db = sqlite3.connect(":memory:")
results = {"engine": "SQLite", "version": sqlite3.sqlite_version,
           "database": ":memory:", "queries": queries, "states": [],
           "data_scope": "Synthetic SQL fixtures only; no application writer was supplied."}


def snapshot(state):
    entry = {"state": state, "columns": db.execute("PRAGMA table_info(users)").fetchall(),
             "rows": db.execute("SELECT * FROM users ORDER BY id").fetchall(), "readers": {}}
    for name, query in queries.items():
        try:
            entry["readers"][name] = {"status": "ok", "rows": db.execute(query).fetchall()}
        except sqlite3.Error as exc:
            entry["readers"][name] = {"status": "error", "error": str(exc)}
    results["states"].append(entry)


db.executescript((ROOT / "001_initial.sql").read_text())
db.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "Alice"), (2, "Bob")])
db.commit()
snapshot("initial")
db.executescript((ROOT / "002_up.sql").read_text())
snapshot("up_before_new_schema_writes")
db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Alice updated", 1))
db.execute("INSERT INTO users (id, display_name) VALUES (?, ?)", (3, "New user 새 사용자"))
db.commit()
results["fixture_writes"] = [
    {"sql": "UPDATE users SET display_name = ? WHERE id = ?", "parameters": ["Alice updated", 1]},
    {"sql": "INSERT INTO users (id, display_name) VALUES (?, ?)", "parameters": [3, "New user 새 사용자"]},
]
snapshot("up_after_new_schema_writes_before_rollback")
db.executescript((ROOT / "002_down.sql").read_text())
snapshot("down_after_new_schema_writes")

expected_statuses = [("ok", "error"), ("error", "ok"), ("error", "ok"), ("ok", "error")]
for state, expected in zip(results["states"], expected_statuses):
    assert tuple(state["readers"][name]["status"] for name in queries) == expected
assert results["states"][-1]["rows"] == [(1, "Alice updated"), (2, "Bob"), (3, "New user 새 사용자")]
assert results["states"][-1]["rows"] == results["states"][-2]["rows"]
assert [col[1] for col in results["states"][-1]["columns"]] == ["id", "name"]
assert fingerprints() == before, "Release file changed during verification"
results["release_sha256"] = before
results["checks"] = "Passed: expected reader compatibility, inserted/updated/untouched data survives down, original column names restored, release files unchanged."
print(json.dumps(results, ensure_ascii=False, indent=2))
db.close()
