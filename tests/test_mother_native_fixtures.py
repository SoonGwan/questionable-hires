"""Validate transfer-fixture ground truth, not model performance."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from mother_project_cases import cases


ORACLE = '''import asyncio, json
from catalog.controller import Catalog
from tests.support import ControlledAPI

async def check(boundary, old_failure):
    api = ControlledAPI()
    view = Catalog(api)
    tasks = []
    async def start(query):
        task = asyncio.create_task(view.search(query))
        tasks.append(task)
        assert await asyncio.wait_for(api.entered.get(), 0.5) == query
        return task
    try:
        old = await start('old')
        if boundary:
            await view.search('   ')
            expected = []
        else:
            new = await start('new')
            api.pending['new'].set_result([{'title': 'Latest'}])
            await new
            expected = ['Latest']
        before = [list(view.titles), view.problem]
        assert before == [expected, None], before
        if old_failure:
            api.pending['old'].set_exception(RuntimeError('old failure'))
        else:
            api.pending['old'].set_result([{'title': 'Stale'}])
        await old
        return [view.titles, view.problem] == before
    finally:
        for task in tasks:
            if not task.done(): task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

async def main():
    result = {}
    for boundary in (False, True):
        for failure in (False, True):
            name = ('clear' if boundary else 'newer') + ('-error' if failure else '-success')
            result[name] = await check(boundary, failure)
    print(json.dumps(result))

asyncio.run(asyncio.wait_for(main(), 3))
'''


class MotherNativeFixturesTests(unittest.TestCase):
    def test_committed_fixtures_match_generator(self):
        frozen = json.loads((ROOT / 'benchmarks/mother-native-project-cases.json').read_text())
        self.assertEqual(frozen, cases())

    def test_existing_suite_and_independent_ordering_oracle(self):
        for case in cases():
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as tmp:
                project = Path(tmp)
                for name, contents in case['files'].items():
                    target = project / name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(contents)
                existing = subprocess.run(
                    [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-t', '.'],
                    cwd=project, capture_output=True, text=True, timeout=10)
                self.assertEqual(existing.returncode, 0, existing.stderr)
                oracle = subprocess.run([sys.executable, '-B', '-c', ORACLE],
                                        cwd=project, capture_output=True, text=True, timeout=10)
                self.assertEqual(oracle.returncode, 0, oracle.stderr)
                guarded = case['id'] == 'native-catalog-guarded'
                self.assertEqual(json.loads(oracle.stdout), {
                    'newer-success': guarded, 'newer-error': True,
                    'clear-success': guarded, 'clear-error': True})
                for name, contents in case['files'].items():
                    self.assertEqual((project / name).read_text(), contents)


if __name__ == '__main__':
    unittest.main()
