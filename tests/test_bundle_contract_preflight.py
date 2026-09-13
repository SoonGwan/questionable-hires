"""Author executions of exposed gate artifacts, never model-performance evidence."""
import asyncio
import importlib.util
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
CASES = {c['id']: c for c in json.loads((ROOT / 'benchmarks/bundle-contract-cases.json').read_text())}


def module(name, source):
    result = types.ModuleType(name)
    exec(compile(source, name + '.py', 'exec'), result.__dict__)
    return result


def run_suite(tests):
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(tests)
    return result, output.getvalue()


class BundlePreflightTests(unittest.TestCase):
    def test_history_current_consumer_and_actual_commit(self):
        spec = importlib.util.spec_from_file_location('bundle_run', ROOT / 'benchmarks/run.py')
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        case = CASES['history-active']
        with tempfile.TemporaryDirectory() as outer:
            project = Path(outer) / 'project'
            head = runner.prepare(case, project)
            history = subprocess.check_output(['git', '-C', str(project), 'log', '-p', '--', 'labels.py', 'consumer.py'], text=True)
            self.assertIn(head, history)
            self.assertIn("payload['name']", history)
            labels = module('labels', case['files']['labels.py'])
            with patch.dict(sys.modules, labels=labels):
                consumer = module('consumer', case['files']['consumer.py'])
                self.assertEqual(consumer.partner_label(), 'Ada')
                consumer.display_label = lambda payload: payload.get('display_name')
                self.assertIsNone(consumer.partner_label())

    def test_boundary_native_controls_and_actual_regression_failure(self):
        files = CASES['boundary-fix']['files']
        for fixed in (False, True):
            source = files['eligibility.py'].replace('> 18', '>= 18') if fixed else files['eligibility.py']
            eligibility = module('eligibility', source)
            with patch.dict(sys.modules, eligibility=eligibility):
                tests = module('test_eligibility', files['test_eligibility.py'])
                def boundary(self):
                    self.assertEqual(eligibility.eligible(18), True)
                tests.EligibilityTests.test_boundary = boundary
                result, output = run_suite(unittest.defaultTestLoader.loadTestsFromModule(tests))
            self.assertEqual(result.testsRun, 3)
            self.assertEqual(len(result.errors), 0)
            self.assertEqual(len(result.failures), 0 if fixed else 1)
            if not fixed:
                self.assertIn('AssertionError: False != True', output)

    def test_formatter_equivalence_through_actual_consumer(self):
        files = CASES['formatter-review']['files']
        formatting = module('formatting', files['formatting.py'])
        with patch.dict(sys.modules, formatting=formatting):
            invoice = module('invoice', files['invoice.py'])
            for cents in (0, 1, 12345, -99):
                self.assertEqual(invoice.total_label(cents), f'${cents / 100:.2f}')

    def test_actual_search_orders_headers_pending_and_cleanup(self):
        async def scenario(case_id, reverse):
            files = CASES[case_id]['files']
            search = module('search', files['search.py']).Search()
            search.result = ['existing']
            futures = {q: asyncio.get_running_loop().create_future() for q in ('old', 'new')}
            dispatched = {q: asyncio.Event() for q in futures}
            async def request(url, params, headers):
                self.assertEqual(url, '/search')
                self.assertEqual(headers, {'Cache-Control': 'no-cache'})
                return await fetch(params['q'])
            async def fetch(query):
                dispatched[query].set()
                return await futures[query]
            if 'transport.py' in files:
                transport = module('transport', files['transport.py'])
                async def actual_request(url, params, headers):
                    # Record actual transport output; do not replace transport.
                    recorded = dict(headers)
                    observations.append(recorded)
                    return await request(url, params, headers)
                observations = []
                async def actual_fetch(query):
                    return await transport.fetch(query, actual_request)
            else:
                actual_fetch = fetch
                observations = []
            tasks = {}
            try:
                for query in ('old', 'new'):
                    tasks[query] = asyncio.create_task(search.run(query, actual_fetch))
                    await asyncio.wait_for(dispatched[query].wait(), 1)
                self.assertEqual(search.result, ['existing'])
                first, second = ('new', 'old') if reverse else ('old', 'new')
                futures[first].set_result([first])
                await asyncio.wait_for(tasks[first], 1)
                if case_id == 'search-protected' and not reverse:
                    self.assertEqual(search.result, ['existing'])
                futures[second].set_result([second])
                await asyncio.wait_for(tasks[second], 1)
                expected = ['new'] if case_id == 'search-protected' or not reverse else ['old']
                self.assertEqual(search.result, expected)
                if reverse and case_id != 'search-protected':
                    with self.assertRaisesRegex(AssertionError, "old.*new"):
                        self.assertEqual(search.result, ['new'])
                if 'transport.py' in files:
                    self.assertEqual(observations, [{'Cache-Control': 'no-cache'}] * 2)
            finally:
                for task in tasks.values():
                    if not task.done():
                        task.cancel()
                await asyncio.wait_for(asyncio.gather(*tasks.values(), return_exceptions=True), 1)
                self.assertTrue(all(task.done() for task in tasks.values()))
        for case_id in ('search-order', 'search-diagnosis', 'search-protected'):
            for reverse in (False, True):
                with self.subTest(case=case_id, reverse=reverse):
                    asyncio.run(asyncio.wait_for(scenario(case_id, reverse), 3))

    def test_form_contract_success_error_cancellation_and_broken_cleanup(self):
        original = module('form', CASES['necessary-state']['files']['form.py']).Form()
        with self.assertRaisesRegex(AssertionError, 'False is not true'):
            self.assertTrue(hasattr(original, 'pending'))
        # Author witness only, never given to model cells or written to fixture.
        witness = '''class Form:
    def __init__(self):
        self.pending = False
    async def submit(self, save):
        if self.pending:
            return
        self.pending = True
        try:
            return await save()
        finally:
            self.pending = False
'''
        async def scenario(broken):
            source = witness.replace('            self.pending = False', '            pass') if broken else witness
            form_type = module('form_witness', source).Form
            form, other = form_type(), form_type()
            self.assertFalse(form.pending)
            started = asyncio.Event()
            gate = asyncio.get_running_loop().create_future()
            calls = []
            async def save():
                calls.append(1)
                started.set()
                return await gate
            task = asyncio.create_task(form.submit(save))
            try:
                await asyncio.wait_for(started.wait(), 1)
                self.assertTrue(form.pending)
                self.assertFalse(other.pending)
                await asyncio.wait_for(form.submit(save), 1)
                self.assertEqual(calls, [1])
                value = object()
                gate.set_result(value)
                self.assertIs(await asyncio.wait_for(task, 1), value)
                self.assertFalse(form.pending)
                error = ValueError('save failed')
                async def fail():
                    raise error
                try:
                    await asyncio.wait_for(form.submit(fail), 1)
                except ValueError as actual:
                    self.assertIs(actual, error)
                else:
                    self.fail('Save exception not propagated')
                self.assertFalse(form.pending)
                async def immediate():
                    return value
                self.assertIs(await asyncio.wait_for(form.submit(immediate), 1), value)
                started.clear()
                gate = asyncio.get_running_loop().create_future()
                task = asyncio.create_task(form.submit(save))
                await asyncio.wait_for(started.wait(), 1)
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await asyncio.wait_for(task, 1)
                self.assertFalse(form.pending)
            finally:
                if not task.done():
                    task.cancel()
                await asyncio.wait_for(asyncio.gather(task, return_exceptions=True), 1)
                self.assertTrue(task.done())
        asyncio.run(asyncio.wait_for(scenario(False), 3))
        with self.assertRaisesRegex(AssertionError, 'True is not false'):
            asyncio.run(asyncio.wait_for(scenario(True), 3))

    def test_persistence_real_binding_survival_and_stronger_assertion(self):
        files = CASES['persistence-test']['files']
        for faulty in (False, True):
            source = files['service.py'].replace('    store.append(record)\n', '') if faulty else files['service.py']
            service = module('service', source)
            with patch.dict(sys.modules, service=service):
                tests = module('test_service', files['test_service.py'])
                self.assertIs(tests.save, service.save)
                result, _ = run_suite(unittest.defaultTestLoader.loadTestsFromModule(tests))
                self.assertTrue(result.wasSuccessful())
                self.assertEqual(result.testsRun, 1)
                def stored_record(self):
                    store = ['existing']
                    tests.save(store, 'record')
                    self.assertEqual(store, ['existing', 'record'])
                check = type('StoredRecord', (unittest.TestCase,), {'test_record': stored_record})
                result, output = run_suite(unittest.defaultTestLoader.loadTestsFromTestCase(check))
                self.assertEqual(len(result.errors), 0)
                self.assertEqual(len(result.failures), int(faulty))
                if faulty:
                    self.assertIn("['existing'] != ['existing', 'record']", output)

    def test_schema_actual_readers_and_changed_data_through_down(self):
        files = CASES['rolling-schema']['files']
        old = module('old_reader', files['old_reader.py']).QUERY
        new = module('new_reader', files['new_reader.py']).QUERY
        connection = sqlite3.connect(':memory:')
        try:
            connection.executescript(files['001_initial.sql'])
            connection.execute("INSERT INTO users VALUES (1, 'original')")
            self.assertEqual(connection.execute(old).fetchall(), [(1, 'original')])
            with self.assertRaisesRegex(sqlite3.OperationalError, 'no such column: display_name'):
                connection.execute(new)
            connection.executescript(files['002_up.sql'])
            with self.assertRaisesRegex(sqlite3.OperationalError, 'no such column: name'):
                connection.execute(old)
            connection.execute("UPDATE users SET display_name='changed' WHERE id=1")
            connection.execute("INSERT INTO users VALUES (2, 'new')")
            self.assertEqual(sorted(connection.execute(new).fetchall()), [(1, 'changed'), (2, 'new')])
            connection.executescript(files['002_down.sql'])
            self.assertEqual(sorted(connection.execute(old).fetchall()), [(1, 'changed'), (2, 'new')])
            with self.assertRaisesRegex(sqlite3.OperationalError, 'no such column: display_name'):
                connection.execute(new)
        finally:
            connection.close()
