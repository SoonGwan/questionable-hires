"""Local SQLite compatibility and rollback probe; no application writers supplied."""
import ast
import hashlib
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "001_initial.sql", "002_up.sql", "002_down.sql",
    "old_reader.py", "new_reader.py", "release.md",
)


def fingerprints():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def query_from(name):
    module = ast.parse((ROOT / name).read_text())
    return next(
        ast.literal_eval(node.value)
        for node in module.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "QUERY" for t in node.targets)
    )


before = fingerprints()
db = sqlite3.connect(":memory:")
queries = {name: query_from(name) for name in ("old_reader.py", "new_reader.py")}
result = {
    "engine": "SQLite " + sqlite3.sqlite_version,
    "scope": "Synthetic SQL probes, not evidence of application writer compatibility or staging readiness",
    "queries": queries,
    "states": {},
}


def capture(label):
    state = {
        "schema": db.execute("SELECT sql FROM sqlite_master WHERE name = 'users'").fetchone()[0],
        "rows": db.execute("SELECT * FROM users ORDER BY id").fetchall(),
        "readers": {},
    }
    for name, sql in queries.items():
        try:
            state["readers"][name] = {"ok": True, "rows": db.execute(sql).fetchall()}
        except sqlite3.Error as exc:
            state["readers"][name] = {"ok": False, "error": str(exc)}
    result["states"][label] = state


db.executescript((ROOT / "001_initial.sql").read_text())
db.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "Alice"), (2, "Bob")])
db.commit()
capture("initial")
db.executescript((ROOT / "002_up.sql").read_text())
capture("up_before_writes")
db.execute("UPDATE users SET display_name = ? WHERE id = ?", ("Alice updated", 1))
db.execute("INSERT INTO users (id, display_name) VALUES (?, ?)", (3, "Carol new"))
db.commit()
result["synthetic_new_schema_writes"] = [
    "UPDATE users SET display_name = 'Alice updated' WHERE id = 1",
    "INSERT INTO users (id, display_name) VALUES (3, 'Carol new')",
]
capture("up_after_writes_before_rollback")
db.executescript((ROOT / "002_down.sql").read_text())
capture("down_after_writes")

states = result["states"]
for label, old_ok, new_ok in (
    ("initial", True, False),
    ("up_before_writes", False, True),
    ("up_after_writes_before_rollback", False, True),
    ("down_after_writes", True, False),
):
    assert states[label]["readers"]["old_reader.py"]["ok"] == old_ok
    assert states[label]["readers"]["new_reader.py"]["ok"] == new_ok
expected = [(1, "Alice updated"), (2, "Bob"), (3, "Carol new")]
assert states["up_after_writes_before_rollback"]["rows"] == expected
assert states["down_after_writes"]["rows"] == expected
assert states["down_after_writes"]["readers"]["old_reader.py"]["rows"] == expected
assert before == fingerprints(), "Release files changed during verification"
result["release_sha256"] = before
result["assertions"] = "passed: expected reader matrix, rollback data preservation, unchanged release files"
db.close()
output = Path(__file__).with_name("results.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
