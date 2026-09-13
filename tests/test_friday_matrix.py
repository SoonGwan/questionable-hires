import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "skills/friday/scripts/sqlite_matrix.py"
spec = importlib.util.spec_from_file_location("friday_matrix", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def phase(name, sql="", files=None):
    return {"name": name, "files": files or [], "sql": sql}


class MatrixTests(unittest.TestCase):
    def test_combined_budget_stops_before_opening_overflow_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'large.sql'
            source.write_bytes(b' ' * 999_990)
            recipe = {'phases': [phase('oversized', files=['large.sql'] * 100)],
                      'checks': {'read': 'SELECT 1'}}
            opened = []
            original_open = Path.open
            def tracked_open(path, *args, **kwargs):
                opened.append(path)
                return original_open(path, *args, **kwargs)
            with patch.object(Path, 'open', tracked_open), \
                    patch.object(helper.sqlite3, 'connect') as connect, \
                    self.assertRaisesRegex(ValueError, 'SQL exceeds 2 MB'):
                helper.matrix(recipe, root)
            self.assertEqual(opened, [source.resolve(), source.resolve()])
            connect.assert_not_called()
            self.assertEqual(source.stat().st_size, 999_990)

    def test_inline_and_check_budget_rejects_before_any_file_read(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'schema.sql'
            source.write_text('SELECT 1;')
            for inline, query in ((' ' * 2_000_000, 'SELECT 1'), ('', '가' * 700_000)):
                with self.subTest(inline_bytes=len(inline)), \
                        patch.object(Path, 'open') as opened, \
                        patch.object(helper.sqlite3, 'connect') as connect, \
                        self.assertRaisesRegex(ValueError, 'SQL exceeds 2 MB'):
                    helper.matrix({'phases': [phase('big', inline, ['schema.sql'])],
                                   'checks': {'read': query}}, directory)
                opened.assert_not_called()
                connect.assert_not_called()

    def test_crlf_file_bytes_count_without_changing_sql_results(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'schema.sql'
            contents = b'CREATE TABLE t(x);\r\nINSERT INTO t VALUES(7);\r\n'
            source.write_bytes(contents)
            result = helper.matrix({'phases': [phase('ok', files=['schema.sql'])],
                                    'checks': {'read': 'SELECT x FROM t'}}, directory)
            self.assertEqual(result['phases'][0]['checks']['read']['rows'], [(7,)])
            self.assertEqual(source.read_bytes(), contents)

    def test_exact_combined_budget_remains_executable(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'a.sql').write_bytes(b' ' * 1_000_000)
            (root / 'b.sql').write_bytes(b' ' * 999_992)
            result = helper.matrix({'phases': [phase('limit', files=['a.sql', 'b.sql'])],
                                    'checks': {'read': 'SELECT 1'}}, root)
            self.assertTrue(result['complete'])
            self.assertEqual(result['phases'][0]['checks']['read']['rows'], [(1,)])

    def test_growth_after_stat_is_bounded_before_decode_or_sql(self):
        class GrowingFile(io.BytesIO):
            requested = []
            def read(self, size=-1):
                self.requested.append(size)
                return super().read(size)
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / 'a.sql').write_bytes(b' ')
            grown = GrowingFile(b' ' * 1_000_002)
            with patch.object(Path, 'open', return_value=grown), \
                    patch.object(helper.sqlite3, 'connect') as connect, \
                    self.assertRaisesRegex(ValueError, 'exceeds 1 MB'):
                helper.matrix({'phases': [phase('growing', files=['a.sql'])],
                               'checks': {'read': 'SELECT 1'}}, directory)
            self.assertEqual(grown.requested, [1_000_001])
            connect.assert_not_called()

    def test_deadline_between_migration_chunks_stops_before_next_sql(self):
        now = [0.0]
        executed = []
        connect = helper.sqlite3.connect
        def traced_connect(*args, **kwargs):
            db = connect(*args, **kwargs)
            def trace(sql):
                executed.append(sql)
                if sql == "CREATE TABLE t(x);":
                    now[0] = 2.0
            db.set_trace_callback(trace)
            return db
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "schema.sql"
            source.write_text("CREATE TABLE t(x);")
            recipe = {"phases": [phase("partial", "INSERT INTO t VALUES(1);", ["schema.sql"]),
                                 phase("unreachable", "DROP TABLE t;")],
                      "checks": {"unrun": "SELECT * FROM t"}}
            with patch.object(helper.sqlite3, "connect", side_effect=traced_connect), \
                    patch.object(helper.time, "monotonic", side_effect=lambda: now[0]):
                result = helper.matrix(recipe, directory, timeout=1)
            self.assertEqual(source.read_text(), "CREATE TABLE t(x);")
        self.assertIn("CREATE TABLE t(x);", executed)
        self.assertNotIn("INSERT INTO t VALUES(1);", executed)
        self.assertNotIn("DROP TABLE t;", executed)
        self.assertNotIn("SELECT * FROM t", executed)
        self.assertFalse(result["complete"])
        self.assertEqual(len(result["phases"]), 1)
        self.assertEqual(result["phases"][0]["checks"], {})
        self.assertEqual(result["error"], "time budget exhausted")

    def test_sql_budget_counts_utf8_bytes(self):
        with self.assertRaises(ValueError):
            helper.matrix({"phases": [phase("oversized", "--" + "가" * 700000)],
                           "checks": {"read": "SELECT 1"}}, SCRIPT.parent)

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
        result = helper.matrix({"phases": [phase("before"), phase("unreachable")], "checks": {"loop":
            "WITH RECURSIVE t(x) AS (VALUES(1) UNION ALL SELECT x+1 FROM t) SELECT sum(x) FROM t",
            "unrun": "SELECT 1"}},
            SCRIPT.parent, timeout=0.01)
        self.assertFalse(result["complete"])
        self.assertFalse(result["phases"][0]["checks"]["loop"]["ok"])
        self.assertNotIn("unrun", result["phases"][0]["checks"])
        self.assertEqual(len(result["phases"]), 1)
        self.assertEqual(result["error"], "time budget exhausted")

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
