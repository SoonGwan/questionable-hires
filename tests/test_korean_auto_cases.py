import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from korean_auto_cases import cases
import run


class KoreanAutoCasesTests(unittest.TestCase):
    def test_ten_cases_preserve_exposed_inputs_without_naming_skills(self):
        selected = cases()
        original = {c['id']: c for c in json.loads((ROOT / 'benchmarks/cases.json').read_text())}
        self.assertEqual(len(selected), 10)
        self.assertEqual(len({c['expected_primary'] for c in selected[:8]}), 8)
        self.assertEqual([c['expected_primary'] for c in selected[8:]], [None, None])
        for case in selected[:8]:
            old = original[case['source_case']]
            for key in ('files', 'history', 'criteria'):
                self.assertEqual(case.get(key), old.get(key))
            self.assertNotIn('$', case['task'])
            for skill in (p.name for p in (ROOT / 'skills').iterdir() if p.is_dir()):
                self.assertNotIn(skill, case['task'])

    def test_native_positive_and_defect_controls(self):
        selected = {c['source_case']: c for c in cases()[:8]}
        def exercise(identity, script, expected=0, output=None, replacement=None):
            with tempfile.TemporaryDirectory(dir=ROOT / 'benchmarks') as scratch:
                project = Path(scratch) / 'project'
                run.prepare(selected[identity], project)
                if replacement:
                    name, old, new = replacement
                    path = project / name
                    text = path.read_text()
                    self.assertEqual(text.count(old), 1)
                    path.write_text(text.replace(old, new))
                result = subprocess.run([sys.executable, '-B', '-c', script], cwd=project,
                    capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                if output:
                    self.assertIn(output, result.stdout + result.stderr)
        exercise('history-active', 'from consumer import partner_label; assert partner_label() == "Ada"')
        exercise('history-active', 'from consumer import partner_label; partner_label()', 1, "KeyError: 'display_name'",
                 ('labels.py', "payload.get('display_name') or payload['name']", "payload['display_name']"))
        exercise('boundary-fix', 'from eligibility import eligible; assert eligible(18), "18 rejected"', 1, '18 rejected')
        exercise('boundary-fix', 'from eligibility import eligible; assert [eligible(n) for n in (17,18,19)] == [False,True,True]',
                 replacement=('eligibility.py', 'age > 18', 'age >= 18'))
        exercise('formatter-review', 'from invoice import total_label; assert [total_label(n) for n in (0,105,-105)] == ["$0.00","$1.05","$-1.05"]')
        async_script = '''import asyncio
from search import Search
async def check():
    owner = Search()
    entered = asyncio.Queue()
    async def fetch(key):
        response = asyncio.get_running_loop().create_future()
        entered.put_nowait((key, response))
        return await response
    tasks = []
    try:
        for key in ('old', 'new'):
            tasks.append(asyncio.create_task(owner.run(key, fetch)))
        first = await asyncio.wait_for(entered.get(), 1)
        second = await asyncio.wait_for(entered.get(), 1)
        for index in ORDER:
            key, response = (first, second)[index]
            response.set_result(key)
            await asyncio.wait_for(tasks[index], 1)
        assert owner.result == 'new', repr(owner.result)
    finally:
        for task in tasks: task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
asyncio.run(check())
'''
        for identity in ('search-order', 'search-diagnosis'):
            exercise(identity, async_script.replace('ORDER', '(0, 1)'))
            exercise(identity, async_script.replace('ORDER', '(1, 0)'), 1, "AssertionError: 'old'")
        exercise('persistence-test', 'import unittest; unittest.main(module="test_service")')
        exercise('persistence-test', 'import unittest; unittest.main(module="test_service")',
                 replacement=('service.py', '    store.append(record)\n', ''))
        exercise('persistence-test', 'from service import save; s=[]; save(s,"record"); assert s == ["record"], repr(s)',
                 1, 'AssertionError: []', ('service.py', '    store.append(record)\n', ''))
        exercise('rolling-schema', '''import sqlite3
from pathlib import Path
from old_reader import QUERY as old
from new_reader import QUERY as new
c=sqlite3.connect(':memory:')
c.executescript(Path('001_initial.sql').read_text())
c.execute("INSERT INTO users VALUES (1, 'Ada')")
assert c.execute(old).fetchall() == [(1,'Ada')]
c.executescript(Path('002_up.sql').read_text())
assert c.execute(new).fetchall() == [(1,'Ada')]
try: c.execute(old)
except sqlite3.OperationalError as e: assert 'no such column: name' in str(e)
else: raise AssertionError('Old reader unexpectedly worked before down')
c.executescript(Path('002_down.sql').read_text())
assert c.execute(old).fetchall() == [(1,'Ada')]
''')
