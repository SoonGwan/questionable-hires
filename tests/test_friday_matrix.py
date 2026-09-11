import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/friday/scripts/sqlite_matrix.py"
spec = importlib.util.spec_from_file_location("friday_matrix", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def phase(name, sql="", files=None):
    return {"name": name, "files": files or [], "sql": sql}


class MatrixTests(unittest.TestCase):
    def test_rename_and_rollback_keep_new_data(self):
        recipe = {"phases": [
            phase("before", "CREATE TABLE users(id, name); INSERT INTO users VALUES(1, 'old');"),
            phase("up", "ALTER TABLE users RENAME COLUMN name TO display_name; INSERT INTO users VALUES(2, 'new');"),
            phase("down", "ALTER TABLE users RENAME COLUMN display_name TO name;")],
            "checks": {"old": "SELECT name FROM users ORDER BY id", "new": "SELECT display_name FROM users ORDER BY id"}}
        result = helper.matrix(recipe, SCRIPT.parent)
        self.assertTrue(result["complete"])
        checks = [row["checks"] for row in result["phases"]]
        self.assertEqual([(c["old"]["ok"], c["new"]["ok"]) for c in checks],
                         [(True, False), (False, True), (True, False)])
        self.assertEqual(checks[2]["old"]["rows"], [("old",), ("new",)])

    def test_compatible_additive_schema_and_file_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "up.sql"
            source = b"ALTER TABLE users ADD COLUMN display_name TEXT;"
            path.write_bytes(source)
            result = helper.matrix({"phases": [phase("before", "CREATE TABLE users(name);"),
                phase("up", files=["up.sql"])], "checks": {"old": "SELECT name FROM users",
                "new": "SELECT display_name FROM users"}}, directory)
            self.assertTrue(all(c["ok"] for c in result["phases"][1]["checks"].values()))
            self.assertEqual(path.read_bytes(), source)

    def test_check_cannot_write_even_if_statement_previously_authorized(self):
        result = helper.matrix({"phases": [phase("before", "CREATE TABLE t(x); INSERT INTO t VALUES(1);")],
            "checks": {"write": "INSERT INTO t VALUES(1);", "read": "SELECT * FROM t"}}, SCRIPT.parent)
        self.assertFalse(result["phases"][0]["checks"]["write"]["ok"])
        self.assertEqual(result["phases"][0]["checks"]["read"]["rows"], [(1,)])

    def test_external_database_and_extension_denied(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "forbidden.db"
            for sql in [f"ATTACH DATABASE '{target}' AS outside;", "PRAGMA temp_store_directory='.';",
                        "SELECT load_extension('missing');", f"VACUUM INTO '{target}';"]:
                with self.subTest(sql=sql):
                    result = helper.matrix({"phases": [phase("bad", sql), phase("unreachable")],
                        "checks": {"read": "SELECT 1"}}, directory)
                    self.assertFalse(result["complete"])
                    self.assertEqual(len(result["phases"]), 1)
                    self.assertFalse(target.exists())

    def test_partial_migration_stops_without_checks(self):
        result = helper.matrix({"phases": [phase("partial", "CREATE TABLE t(x); INVALID;"), phase("next")],
            "checks": {"read": "SELECT * FROM t"}}, SCRIPT.parent)
        self.assertFalse(result["complete"])
        self.assertEqual(result["phases"][0]["checks"], {})
        self.assertEqual(len(result["phases"]), 1)

    def test_recursive_query_times_out(self):
        result = helper.matrix({"phases": [phase("before")], "checks": {"loop":
            "WITH RECURSIVE t(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM t) SELECT sum(x) FROM t"}},
            SCRIPT.parent, timeout=0.01)
        self.assertFalse(result["complete"])
        self.assertFalse(result["phases"][0]["checks"]["loop"]["ok"])

    def test_rows_truncated_explicitly(self):
        result = helper.matrix({"phases": [phase("before")], "checks": {"rows":
            "WITH RECURSIVE t(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM t WHERE x<30) SELECT x FROM t"}}, SCRIPT.parent)
        check = result["phases"][0]["checks"]["rows"]
        self.assertEqual(len(check["rows"]), 20)
        self.assertTrue(check["truncated"])

    def test_path_escape_and_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "real.sql").write_text("SELECT 1;")
            (root / "link.sql").symlink_to(root / "real.sql")
            for filename in ["../outside.sql", str(root / "real.sql"), "link.sql"]:
                with self.subTest(filename=filename), self.assertRaises(ValueError):
                    helper.matrix({"phases": [phase("bad", files=[filename])],
                                   "checks": {"read": "SELECT 1"}}, root)

    def test_cli_failed_reader_is_not_execution_failure_and_blob_is_json(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "--spec", "-"], input=json.dumps({
            "phases": [phase("before")], "checks": {"blob": "SELECT x'ff'", "missing": "SELECT * FROM absent"}}),
            text=True, capture_output=True, check=True)
        output = json.loads(result.stdout)
        self.assertEqual(output["phases"][0]["checks"]["blob"]["rows"], [[{"blob_hex": "ff"}]])
        self.assertFalse(output["phases"][0]["checks"]["missing"]["ok"])


if __name__ == "__main__":
    unittest.main()
