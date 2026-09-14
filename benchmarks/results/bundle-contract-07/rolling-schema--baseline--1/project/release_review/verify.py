"""Local SQLite rehearsal; synthetic writes are not application-writer evidence."""
import ast
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "001_initial.sql", "002_up.sql", "002_down.sql",
    "old_reader.py", "new_reader.py", "release.md",
)


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}


def supplied_query(name):
    tree = ast.parse((ROOT / name).read_text())
    assignments = [node for node in tree.body if isinstance(node, ast.Assign)
                   and any(isinstance(target, ast.Name) and target.id == "QUERY"
                           for target in node.targets)]
    assert len(assignments) == 1
    return ast.literal_eval(assignments[0].value)


before = hashes()
db = sqlite3.connect(":memory:")
queries = {name: supplied_query(name) for name in ("old_reader.py", "new_reader.py")}
evidence = {
    "engine": "SQLite " + sqlite3.sqlite_version,
    "scope": "In-memory local rehearsal; direct synthetic SQL writes only. No staging, deployment, or application-writer verification.",
    "queries": queries,
    "states": {},
    "release_sha256_before": before,
}


def inspect(label, expected_reader, expected_rows):
    state = {"schema": db.execute("PRAGMA table_info(users)").fetchall(), "readers": {}}
    for name, query in queries.items():
        try:
            rows = db.execute(query).fetchall()
            state["readers"][name] = {"rows": rows}
            assert name == expected_reader, (label, name, "unexpected success")
            assert sorted(rows) == expected_rows
        except sqlite3.OperationalError as error:
            state["readers"][name] = {"error": str(error)}
            assert name != expected_reader, (label, name, str(error))
            missing = "display_name" if name == "new_reader.py" else "name"
            assert str(error) == "no such column: " + missing
    evidence["states"][label] = state


db.executescript((ROOT / "001_initial.sql").read_text())
db.executemany("INSERT INTO users (id, name) VALUES (?, ?)", [(1, "Alice"), (2, "Bob")])
db.commit()
inspect("initial", "old_reader.py", [(1, "Alice"), (2, "Bob")])
db.executescript((ROOT / "002_up.sql").read_text())
inspect("up", "new_reader.py", [(1, "Alice"), (2, "Bob")])

evidence["synthetic_new_schema_writes"] = [
    {"sql": "UPDATE users SET display_name = ? WHERE id = ?", "parameters": ["Alice updated", 1]},
    {"sql": "INSERT INTO users (id, display_name) VALUES (?, ?)", "parameters": [3, "New user 한글"]},
]
for write in evidence["synthetic_new_schema_writes"]:
    db.execute(write["sql"], write["parameters"])
db.commit()
survivors = [(1, "Alice updated"), (2, "Bob"), (3, "New user 한글")]
inspect("up_after_new_schema_writes_before_down", "new_reader.py", survivors)
db.executescript((ROOT / "002_down.sql").read_text())
inspect("down_after_new_schema_writes", "old_reader.py", survivors)
db.close()
evidence["release_sha256_after"] = hashes()
assert before == evidence["release_sha256_after"], "Release files changed"
evidence["assertions"] = "PASS: compatibility matrix, surviving rows, and unchanged release files"
output = json.dumps(evidence, indent=2, ensure_ascii=False) + "\n"
(ROOT / "release_review" / "evidence.json").write_text(output)
print(output)
