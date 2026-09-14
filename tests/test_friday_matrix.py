import importlib.util
import io
import json
import copy
import hashlib
import sqlite3
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
    def test_shared_reader_module_is_parsed_once_without_reusing_sql_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            text = "FIRST = 'SELECT x FROM t ORDER BY x'\nSECOND = 'SELECT count(*) FROM t'\n"
            (root / 'readers.py').write_text(text)
            recipe = {'phases': [phase('before', 'CREATE TABLE t(x); INSERT INTO t VALUES(1);'),
                                 phase('after', 'INSERT INTO t VALUES(2);')],
                      'checks': {name: {'python_file': 'readers.py', 'constant': constant}
                                 for name, constant in [('rows', 'FIRST'), ('count', 'SECOND'), ('again', 'FIRST')]}}
            real_open, opened = Path.open, []
            def tracked_open(path, *args, **kwargs):
                opened.append(path)
                return real_open(path, *args, **kwargs)
            with patch.object(helper.ast, 'parse', wraps=helper.ast.parse) as parsed, \
                    patch.object(Path, 'open', tracked_open):
                result = helper.matrix(recipe, root)
            self.assertEqual(parsed.call_count, 1)
            self.assertEqual(opened, [root.resolve() / 'readers.py'])
            self.assertEqual(result['phases'][0]['checks']['count']['rows'], [(1,)])
            self.assertEqual(result['phases'][1]['checks']['count']['rows'], [(2,)])
            self.assertEqual(result['phases'][1]['checks']['rows']['rows'], [(1,), (2,)])
            self.assertEqual(result['phases'][1]['checks']['again'], result['phases'][1]['checks']['rows'])
            for label, entry in result['reader_sources'].items():
                self.assertEqual(entry['sha256'], hashlib.sha256(text.encode()).hexdigest())
                self.assertEqual(entry['line'], 2 if label == 'count' else 1)
            (root / 'readers.py').write_text(text.replace('count(*)', 'sum(x)'))
            self.assertEqual(helper.matrix(recipe, root)['phases'][1]['checks']['count']['rows'], [(3,)])

    def test_cached_declarations_still_validate_each_selection_before_sql(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'readers.py').write_text("QUERY = 'SELECT 1'\nNOT_SQL = 42\n")
            for constant in ('MISSING', 'NOT_SQL'):
                with patch.object(helper.sqlite3, 'connect') as connect:
                    with self.assertRaisesRegex(ValueError, 'literal SQL string'):
                        helper.matrix({'phases': [phase('checkpoint')], 'checks': {
                            'first': {'python_file': 'readers.py', 'constant': 'QUERY'},
                            'second': {'python_file': 'readers.py', 'constant': constant}}}, root)
                    connect.assert_not_called()

    def test_optional_phase_fields_match_explicit_defaults_without_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = "CREATE TABLE t(x); INSERT INTO t VALUES(x'ff0080');"
            (root / 'initial.sql').write_text(source)
            recipe = {'phases': [
                {'name': 'file only', 'files': ['initial.sql']},
                {'name': 'inline only', 'sql': "INSERT INTO t VALUES(x'');"},
                {'name': 'checkpoint'}], 'checks': {'reader': 'SELECT x FROM t'}}
            before = copy.deepcopy(recipe)
            explicit = copy.deepcopy(recipe)
            for entry in explicit['phases']:
                entry.setdefault('files', [])
                entry.setdefault('sql', '')
            result = helper.matrix(recipe, root)
            self.assertTrue(result['complete'])
            self.assertEqual(result, helper.matrix(explicit, root))
            self.assertEqual(result['phases'][-1]['checks']['reader']['rows'],
                             [(bytes.fromhex('ff0080'),), (b'',)])
            self.assertEqual(recipe, before)
            self.assertEqual((root / 'initial.sql').read_text(), source)
            process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source', str(root), '--spec', '-'],
                                     input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout), json.loads(helper.format_result(result)))

    def test_optional_phase_fields_do_not_accept_typos_or_nulls(self):
        invalid = [{}, {'sql': ''}, {'name': ''}, {'name': None},
                   {'name': 'bad', 'file': []}, {'name': 'bad', 'sql': None},
                   {'name': 'bad', 'files': None}, {'name': 'bad', 'files': ''},
                   {'name': 'bad', 'sql': []}]
        for entry in invalid:
            with self.subTest(entry=entry), patch.object(helper.sqlite3, 'connect') as connect:
                with self.assertRaises(ValueError):
                    helper.matrix({'phases': [entry], 'checks': {'read': 'SELECT 1'}}, '.')
                connect.assert_not_called()

    def test_optional_fields_still_enforce_preparation_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'large.sql').write_bytes(b' ' * 1_000_001)
            invalid = [{'name': 'inline', 'sql': '--' + '가' * 700000},
                       {'name': 'file', 'files': ['large.sql']},
                       {'name': 'escape', 'files': ['../outside.sql']}]
            for entry in invalid:
                with self.subTest(name=entry['name']), patch.object(helper.sqlite3, 'connect') as connect:
                    with self.assertRaises(ValueError):
                        helper.matrix({'phases': [entry], 'checks': {'read': 'SELECT 1'}}, root)
                    connect.assert_not_called()

    def test_literal_references_execute_the_existing_release_fixture_without_custom_extraction(self):
        fixtures = json.loads((SCRIPT.parents[3] / 'benchmarks/bundle-contract-v2-cases.json').read_text())
        fixture = next(case for case in fixtures if case['id'] == 'rolling-schema')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, source in fixture['files'].items():
                (root / name).write_text(source)
            recipe = {'phases': [
                phase('initial', "INSERT INTO users VALUES (1, 'original'), (2, 'untouched');", ['001_initial.sql']),
                phase('up', files=['002_up.sql']),
                phase('writes', "UPDATE users SET display_name='updated' WHERE id=1; INSERT INTO users VALUES(3, 'new');"),
                phase('down', files=['002_down.sql'])],
                'checks': {label: {'python_file': label + '_reader.py', 'constant': 'QUERY'}
                           for label in ('old', 'new')}}
            process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source', str(root), '--spec', '-'],
                                     input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            result = json.loads(process.stdout)
            self.assertTrue(result['complete'])
            self.assertEqual([(p['checks']['old']['ok'], p['checks']['new']['ok']) for p in result['phases']],
                             [(True, False), (False, True), (False, True), (True, False)])
            self.assertEqual(result['phases'][3]['checks']['old']['rows'],
                             [[1, 'updated'], [2, 'untouched'], [3, 'new']])
            self.assertEqual({p.name: p.read_text() for p in root.iterdir()}, fixture['files'])

    def test_literal_reader_references_match_native_sql_and_preserve_provenance(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            old = b'"""Public reader declaration."""\r\nQUERY = "SELECT name FROM users ORDER BY id"\r\n'
            new = 'QUERY = "SELECT display_name FROM users ORDER BY id"\n'
            (root / 'old.py').write_bytes(old)
            (root / 'new.py').write_text(new)
            phases = [phase('before', "CREATE TABLE users(id, name); INSERT INTO users VALUES(1, 'old');"),
                      phase('up', "ALTER TABLE users RENAME COLUMN name TO display_name; INSERT INTO users VALUES(2, '새 값');"),
                      phase('down', 'ALTER TABLE users RENAME COLUMN display_name TO name;')]
            recipe = {'phases': phases, 'checks': {
                'old': {'python_file': 'old.py', 'constant': 'QUERY'},
                'new': {'python_file': 'new.py', 'constant': 'QUERY'},
                'inline': 'SELECT count(*) FROM users'}}
            before = copy.deepcopy(recipe)
            result = helper.matrix(recipe, root)
            plain = copy.deepcopy(recipe)
            plain['checks']['old'] = 'SELECT name FROM users ORDER BY id'
            plain['checks']['new'] = 'SELECT display_name FROM users ORDER BY id'
            self.assertEqual(result['phases'], helper.matrix(plain, root)['phases'])
            self.assertEqual(result['phases'][2]['checks']['old']['rows'], [('old',), ('새 값',)])
            self.assertEqual(result['reader_sources']['old']['sha256'], hashlib.sha256(old).hexdigest())
            self.assertEqual(result['reader_sources']['old']['line'], 2)
            self.assertEqual(result['reader_sources']['old']['query'], plain['checks']['old'])
            self.assertEqual(recipe, before)
            self.assertEqual((root / 'old.py').read_bytes(), old)
            self.assertEqual((root / 'new.py').read_text(), new)
            process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source', str(root), '--spec', '-'],
                                     input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(json.loads(process.stdout), json.loads(helper.format_result(result)))

    def test_literal_reader_rejects_dynamic_or_ambiguous_modules_without_execution(self):
        variants = [
            "QUERY = 'SELECT 1'\nQUERY = 'SELECT 2'\n",
            "QUERY = 'SELECT 1'\nimport pathlib\npathlib.Path('sentinel').touch()\n",
            "QUERY = 'SELECT 1'\nif True:\n    QUERY = 'SELECT 2'\n",
            "OTHER = 'SELECT 1'\nQUERY = OTHER\n",
            "QUERY = f'SELECT {1}'\n",
            "def reader():\n    QUERY = 'SELECT 1'\n",
            "QUERY: str = 'SELECT 1'\n",
            "QUERY = OTHER = 'SELECT 1'\n",
            'QUERY = 3\n', 'OTHER = "SELECT 1"\n', 'QUERY = (\n']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for source in variants:
                with self.subTest(source=source):
                    source = source.replace("Path('sentinel')", 'Path(' + repr(str(root / 'sentinel')) + ')')
                    (root / 'reader.py').write_text(source)
                    with patch.object(helper.sqlite3, 'connect') as connect, self.assertRaises(ValueError):
                        helper.matrix({'phases': [phase('before')], 'checks': {
                            'reader': {'python_file': 'reader.py', 'constant': 'QUERY'}}}, root)
                    connect.assert_not_called()
                    self.assertEqual(sorted(path.name for path in root.iterdir()), ['reader.py'])

    def test_literal_reader_references_enforce_paths_and_schema(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'reader.py').write_text('QUERY = "SELECT 1"\n')
            (root / 'link.py').symlink_to(root / 'reader.py')
            (root / 'nested').mkdir()
            (root / 'dirlink').symlink_to(root / 'nested', target_is_directory=True)
            (root / 'nested/query.py').write_text('QUERY = "SELECT 1"\n')
            invalid = [{'python_file': name, 'constant': 'QUERY'} for name in
                       ('../reader.py', str(root / 'reader.py'), 'link.py', 'dirlink/query.py', '.', 'missing.py')]
            invalid += [{}, {'python_file': 'reader.py'}, {'python_file': 'reader.py', 'constant': ''},
                        {'python_file': 3, 'constant': 'QUERY'},
                        {'python_file': 'reader.py', 'constant': 'QUERY', 'execute': True}]
            for reference in invalid:
                with self.subTest(reference=reference), self.assertRaises(ValueError):
                    helper.matrix({'phases': [phase('before')], 'checks': {'r': reference}}, root)

    def test_literal_reader_input_budget_prevents_sql_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'reader.py').write_bytes(b'#' + b' ' * 999_970 + b'\nQUERY = "SELECT 1"\n')
            reference = {'python_file': 'reader.py', 'constant': 'QUERY'}
            recipe = {'phases': [phase('before')], 'checks': {'a': reference, 'b': reference, 'c': reference}}
            with patch.object(helper.sqlite3, 'connect') as connect, \
                    self.assertRaisesRegex(ValueError, 'SQL exceeds 2 MB'):
                helper.matrix(recipe, root)
            connect.assert_not_called()
            (root / 'reader.py').write_bytes(b' ' * 1_000_001)
            with patch.object(Path, 'open') as opened, patch.object(helper.sqlite3, 'connect') as connect, \
                    self.assertRaisesRegex(ValueError, 'exceeds 1 MB'):
                helper.matrix({'phases': [phase('before')], 'checks': {'a': reference}}, root)
            opened.assert_not_called()
            connect.assert_not_called()

    def test_literal_reader_does_not_bypass_read_only_checks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'reader.py').write_text('QUERY = "DELETE FROM t"\n')
            result = helper.matrix({'phases': [phase('before', 'CREATE TABLE t(x); INSERT INTO t VALUES (7);')],
                                    'checks': {'write': {'python_file': 'reader.py', 'constant': 'QUERY'},
                                               'read': 'SELECT x FROM t'}}, root)
            self.assertFalse(result['phases'][0]['checks']['write']['ok'])
            self.assertEqual(result['phases'][0]['checks']['read']['rows'], [(7,)])

    def test_reader_column_contract_is_visible_when_values_do_not_change(self):
        recipe = {'phases': [phase('old view', "CREATE VIEW reader AS SELECT 7 AS old_name;"),
                             phase('new view', "DROP VIEW reader; CREATE VIEW reader AS SELECT 7 AS new_name;")],
                  'checks': {'reader': 'SELECT * FROM reader',
                             'empty': 'SELECT * FROM reader WHERE 0',
                             'duplicate labels': 'SELECT 1 AS repeated, 2 AS repeated',
                             'unicode': 'SELECT 3 AS "표시 이름"',
                             'invalid': 'SELECT * FROM absent'}}
        result = helper.matrix(recipe, SCRIPT.parent)
        self.assertTrue(result['complete'])
        self.assertEqual(result['phases'][0]['checks']['reader']['rows'],
                         result['phases'][1]['checks']['reader']['rows'])
        for index, row in enumerate(result['phases']):
            expected = ['old_name' if index == 0 else 'new_name']
            self.assertIn('columns', row['checks']['reader'])
            self.assertEqual(row['checks']['reader']['columns'], expected)
            self.assertEqual(row['checks']['empty']['columns'], expected)
            self.assertEqual(row['checks']['empty']['rows'], [])
            self.assertEqual(row['checks']['duplicate labels']['columns'], ['repeated', 'repeated'])
            self.assertEqual(row['checks']['duplicate labels']['rows'], [(1, 2)])
            self.assertEqual(row['checks']['unicode']['columns'], ['표시 이름'])
            self.assertNotIn('columns', row['checks']['invalid'])
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--spec', '-'],
                                 input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(json.loads(process.stdout), json.loads(helper.format_result(result)))

    def test_named_consumer_breaks_despite_equal_positional_values(self):
        db = sqlite3.connect(':memory:')
        self.addCleanup(db.close)
        db.row_factory = sqlite3.Row
        old = db.execute('SELECT 7 AS old_name').fetchone()
        new = db.execute('SELECT 7 AS new_name').fetchone()
        self.assertEqual(tuple(old), tuple(new))
        self.assertEqual(old['old_name'], 7)
        with self.assertRaises(IndexError):
            _ = new['old_name']

    def test_no_statement_is_not_a_successful_empty_reader(self):
        placeholders = {'empty': '', 'whitespace': ' \n\t', 'line comment': '-- reader TODO',
                        'block comment': '/* SELECT * FROM t */', 'semicolon': ';',
                        'mixed': '; -- reader TODO\n /* not a query */ ;'}
        recipe = {'phases': [phase('empty table', 'CREATE TABLE t(id INTEGER);'),
                             phase('new row', 'INSERT INTO t VALUES (7);')],
                  'checks': dict(placeholders, reader='-- actual query\nSELECT id FROM t',
                                 zero_rows='SELECT id FROM t WHERE 0')}
        result = helper.matrix(recipe, SCRIPT.parent)
        self.assertTrue(result['complete'])
        self.assertEqual(len(result['phases']), 2)
        for index, row in enumerate(result['phases']):
            for name in placeholders:
                check = row['checks'][name]
                self.assertFalse(check['ok'], (row['name'], name, check))
                self.assertIn('no result set', check['error'])
                self.assertNotIn('rows', check)
            self.assertEqual(row['checks']['reader'],
                             {'ok': True, 'rows': [] if index == 0 else [(7,)], 'columns': ['id'], 'truncated': False})
            self.assertEqual(row['checks']['zero_rows'],
                             {'ok': True, 'rows': [], 'columns': ['id'], 'truncated': False})
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--spec', '-'],
                                 input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)  # Complete observations, not all checks passed.
        self.assertEqual(json.loads(process.stdout), json.loads(helper.format_result(result)))

    def test_public_formatter_matches_cli_without_rerunning_or_mutating(self):
        recipe = {'phases': [phase('values')], 'checks': {
            'mixed': "SELECT 7, 1.25, NULL, '한글', x'00ff', x''",
            'missing': 'SELECT * FROM absent'}}
        result = helper.matrix(recipe, SCRIPT.parent)
        before = copy.deepcopy(result)
        with self.assertRaises(TypeError):
            json.dumps(result)
        with patch.object(helper.sqlite3, 'connect') as connect:
            formatted = helper.format_result(result)
        connect.assert_not_called()
        self.assertEqual(result, before)
        self.assertEqual(result['phases'][0]['checks']['mixed']['rows'],
                         [(7, 1.25, None, '한글', b'\x00\xff', b'')])
        decoded = json.loads(formatted)
        self.assertEqual(decoded['phases'][0]['checks']['mixed']['rows'],
                         [[7, 1.25, None, '한글', {'blob_hex': '00ff'}, {'blob_hex': ''}]])
        process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--spec', '-'],
                                 input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, formatted + '\n')
        self.assertFalse(decoded['phases'][0]['checks']['missing']['ok'])
        self.assertNotIn('rows', decoded['phases'][0]['checks']['missing'])

    def test_public_formatter_preserves_incomplete_execution_and_rejects_unknown_values(self):
        result = helper.matrix({'phases': [phase('partial', 'CREATE TABLE t(x); INVALID;'),
                                           phase('unreachable')],
                                'checks': {'read': 'SELECT * FROM t'}}, SCRIPT.parent)
        decoded = json.loads(helper.format_result(result))
        self.assertFalse(decoded['complete'])
        self.assertEqual(len(decoded['phases']), 1)
        self.assertIn('migration_error', decoded['phases'][0])
        self.assertEqual(decoded['phases'][0]['checks'], {})
        with self.assertRaisesRegex(TypeError, 'Unsupported result value: object'):
            helper.format_result({'unsupported': object()})

    def test_compact_formatter_preserves_retained_model_observations(self):
        evidence = SCRIPT.parents[3] / 'benchmarks/results/bundle-contract-08/rolling-schema--skill--1/commands.json'
        commands = json.loads(evidence.read_text())
        observations = []
        for command in commands:
            for line in command['aggregated_output'].splitlines():
                if line.startswith('{"engine": "sqlite-memory"'):
                    observations.append(json.loads(line))
        self.assertEqual(len(observations), 1)
        original = observations[0]
        before = copy.deepcopy(original)
        compact = helper.format_result(original)
        self.assertEqual(json.loads(compact), original)
        self.assertEqual(original, before)
        self.assertLess(len(compact.encode()), len(json.dumps(original).encode()))
        self.assertEqual(len(original['phases']), 4)
        self.assertEqual(sum(not check['ok'] for phase in original['phases']
                             for check in phase['checks'].values()), 4)
        self.assertEqual(set(original['reader_sources']), {'old', 'new'})

    def test_documented_api_example_executes_with_blob_rows(self):
        reference = (SCRIPT.parents[1] / 'references/sqlite-matrix.md').read_text()
        example = reference.split('```python\n', 1)[1].split('\n```', 1)[0]
        example = example.replace('<skill-dir>', str(SCRIPT.parents[1]))
        output = io.StringIO()
        from contextlib import redirect_stdout
        namespace = {'recipe': {'phases': [phase('example')], 'checks': {'blob': "SELECT x'ff'"}},
                     'project_root': SCRIPT.parent}
        with redirect_stdout(output):
            exec(compile(example, '<documented-friday-api>', 'exec'), namespace)
        self.assertEqual(json.loads(output.getvalue())['phases'][0]['checks']['blob']['rows'],
                         [[{'blob_hex': 'ff'}]])

    def test_core_api_reuses_single_execution_for_binary_comparisons(self):
        reference = (SCRIPT.parents[1] / 'references/sqlite-matrix.md').read_text()
        example = reference.split('```python\n', 1)[1].split('\n```', 1)[0]
        example = example.replace('<skill-dir>', str(SCRIPT.parents[1]))
        fixture = json.loads((SCRIPT.parents[3] / 'benchmarks/friday-binary-rollback-cases.json').read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, content in fixture['files'].items():
                (root / name).write_text(content)
            recipe = {'phases': [{'name': name, 'files': [name]} for name in
                      ('001_initial.sql', '002_up.sql', 'verification_writes.sql', '002_down.sql')],
                      'checks': {name: {'python_file': name + '_reader.py', 'constant': 'QUERY'}
                                 for name in ('old', 'new')}}
            output = io.StringIO()
            from contextlib import redirect_stdout
            namespace = {'recipe': recipe, 'project_root': root}
            with patch.object(sqlite3, 'connect', wraps=sqlite3.connect) as connect, redirect_stdout(output):
                exec(compile(example, '<documented-friday-api>', 'exec'), namespace)
                result = namespace['result']
                self.assertTrue(result['complete'])
                current = result['phases'][2]['checks']['new']
                down = result['phases'][3]['checks']['old']
                for check in (current, down):
                    self.assertTrue(check['ok'])
                    self.assertFalse(check['truncated'])
                expected = {key: bytes.fromhex(value) for key, value in current['rows']}
                actual = dict(down['rows'])
                self.assertEqual(expected, {1: b'\xff\x00\x80', 2: b'\x01\xfe', 3: b'', 4: b'\x00\x01\xff'})
                self.assertEqual(set(actual), set(expected))
                self.assertEqual([key for key in actual if actual[key] != expected[key]], [1, 2, 4])
                self.assertEqual({key: bytes.fromhex(value.decode('ascii')) for key, value in actual.items()}, expected)
                connect.assert_called_once_with(':memory:', cached_statements=0)
            self.assertEqual(json.loads(output.getvalue()), json.loads(helper.format_result(result)))
            self.assertEqual({p.name: p.read_text() for p in root.iterdir()}, fixture['files'])

    def test_core_guide_recipe_executes_native_compatibility_and_rollback(self):
        reference = (SCRIPT.parents[1] / 'references/sqlite-matrix.md').read_text()
        recipe = json.loads(reference.split('```json\n', 1)[1].split('\n```', 1)[0])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {'schema.sql': 'CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);',
                     'up.sql': 'ALTER TABLE users RENAME COLUMN name TO display_name;',
                     'down.sql': 'ALTER TABLE users RENAME COLUMN display_name TO name;'}
            for name, source in files.items():
                (root / name).write_text(source)
            process = subprocess.run([sys.executable, '-B', str(SCRIPT), '--source', str(root), '--spec', '-'],
                                     input=json.dumps(recipe), capture_output=True, text=True, timeout=10)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            result = json.loads(process.stdout)
            self.assertTrue(result['complete'])
            self.assertEqual([(p['checks']['old reader']['ok'], p['checks']['new reader']['ok'])
                              for p in result['phases']], [(True, False), (False, True), (True, False)])
            self.assertEqual(result['phases'][2]['checks']['old reader']['rows'], [[1, 'old'], [2, 'new']])
            self.assertEqual({p.name: p.read_text() for p in root.iterdir()}, files)

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
