"""Actual Search imports and two-order assertions for unchanged exposed interval fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TEST = '''import asyncio
import unittest
from search import Search
PROTECTED = {protected!r}
class Orders(unittest.IsolatedAsyncioTestCase):
    async def scenario(self, order):
        target = Search()
        target.result = 'existing'
        pending = {{q: asyncio.get_running_loop().create_future() for q in ('old', 'new')}}
        entered = {{q: asyncio.Event() for q in pending}}
        async def fetch(q):
            entered[q].set()
            return await pending[q]
        tasks = {{}}
        try:
            for q in pending:
                tasks[q] = asyncio.create_task(target.run(q, fetch))
                await asyncio.wait_for(entered[q].wait(), 1)
            self.assertEqual(target.result, 'existing')
            pending[order[0]].set_result(order[0])
            await asyncio.wait_for(tasks[order[0]], 1)
            if PROTECTED and order[0] == 'old':
                self.assertEqual(target.result, 'existing')
            pending[order[1]].set_result(order[1])
            await asyncio.wait_for(tasks[order[1]], 1)
            self.assertEqual(target.result, 'new')
        finally:
            for task in tasks.values():
                if not task.done(): task.cancel()
            await asyncio.wait_for(asyncio.gather(*tasks.values(), return_exceptions=True), 1)
            self.assertTrue(all(t.done() for t in tasks.values()))
    async def test_normal(self):
        await self.scenario(('old', 'new'))
    async def test_reversed(self):
        await self.scenario(('new', 'old'))
'''


def check():
    cases = {c['id']: c for c in json.loads((ROOT/'mother-interval-cases.json').read_text())}
    guarded = cases['search-protected']['files']['search.py']
    transient = guarded.replace('        self.generation = 0', '        self.generation = 0\n        self.completed_generation = 0').replace('            self.result = result', '            self.result = result\n            self.completed_generation = generation')
    transient += '        if generation < self.generation and self.completed_generation < self.generation:\n            self.result = result\n'
    rows=[]
    for case,variant,source,expected,detail in (
        ('search-protected','original',guarded,0,None),
        ('search-protected','transient',transient,1,"'old' != 'existing'"),
        ('search-order','original',cases['search-order']['files']['search.py'],1,"'old' != 'new'"),
        ('search-order','guarded',guarded,0,None)):
        with tempfile.TemporaryDirectory(prefix='mother-interval-preflight-') as d:
            root=Path(d);(root/'search.py').write_text(source)
            (root/'test_orders.py').write_text(TEST.format(protected=case=='search-protected'))
            imported=subprocess.run([sys.executable,'-B','-c','from search import Search; assert callable(Search.run); print("public Search import ready")'],cwd=root,capture_output=True,text=True,timeout=10)
            assert imported.returncode==0,imported.stderr
            result=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_orders'],cwd=root,capture_output=True,text=True,timeout=10)
            assert result.returncode==expected and 'Ran 2 tests' in result.stderr,(case,variant,result.stderr)
            assert ('FAILED (failures=1)' in result.stderr and detail in result.stderr) if expected else '\nOK\n' in result.stderr
            rows.append(dict(case=case,variant=variant,exit_code=result.returncode,public_import_exit=imported.returncode,output=(result.stdout+result.stderr).replace(str(root),'<PREFLIGHT>')))
    return rows
