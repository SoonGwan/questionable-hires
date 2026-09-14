"""Local SQLite release review; no deployment or application-writer simulation."""
import hashlib
import json
from pathlib import Path
import runpy
import sqlite3


ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "release.md", "001_initial.sql", "002_up.sql", "002_down.sql",
    "old_reader.py", "new_reader.py",
)


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in FILES}


before = hashes()
queries = {name: runpy.run_path(str(ROOT / f"{name}_reader.py"))["QUERY"]
           for name in ("old", "new")}
db = sqlite3.connect(":memory:")
result = {
    "engine": "SQLite",
    "sqlite_version": sqlite3.sqlite_version,
    "scope": "In-memory schema/reader verification, not staging or application writers",
    "queries": queries,
    "states": [],
}


def inspect(state):
    observed = {
        "state": state,
        "schema": db.execute("SELECT sql FROM sqlite_master WHERE name = 'users'").fetchone()[0],
        "readers": {},
    }
    for name, query in queries.items():
        try:
            observed["readers"][name] = {
                "rows": sorted(db.execute(query).fetchall()),
            }
        except sqlite3.Error as error:
            observed["readers"][name] = {"error": str(error)}
    result["states"].append(observed)
    return observed["readers"]


db.executescript((ROOT / "001_initial.sql").read_text())
db.executemany("INSERT INTO users (id, name) VALUES (?, ?)",
               [(1, "Alice"), (2, "Bob")])
db.commit()
initial = inspect("initial")
assert initial["old"]["rows"] == [(1, "Alice"), (2, "Bob")]
assert initial["new"]["error"] == "no such column: display_name"

db.executescript((ROOT / "002_up.sql").read_text())
up = inspect("up_before_new_schema_data")
assert up["old"]["error"] == "no such column: name"
assert up["new"]["rows"] == initial["old"]["rows"]

# Deliberately constructed SQL fixtures; no application writer was supplied.
mutations = [
    ("UPDATE users SET display_name = ? WHERE id = ?", ["Alice Updated", 1]),
    ("INSERT INTO users (id, display_name) VALUES (?, ?)", [3, "New User"]),
]
for statement, parameters in mutations:
    db.execute(statement, parameters)
db.commit()
result["representative_sql_fixtures_not_application_writers"] = mutations
changed = inspect("up_after_committed_insert_update_before_down")
expected = [(1, "Alice Updated"), (2, "Bob"), (3, "New User")]
assert changed["new"]["rows"] == expected
assert changed["old"]["error"] == "no such column: name"

db.executescript((ROOT / "002_down.sql").read_text())
down = inspect("down_after_new_schema_data")
assert down["old"]["rows"] == expected
assert down["new"]["error"] == "no such column: display_name"
result["rollback_data_check"] = {
    "updated_existing_row_survives": True,
    "untouched_existing_row_survives": True,
    "inserted_row_survives": True,
    "original_updated_value_restored": False,
}
db.close()
assert hashes() == before, "Release files changed during verification"
result["release_file_sha256_before_and_after"] = before
result["all_assertions_passed"] = True
print(json.dumps(result, indent=2))
