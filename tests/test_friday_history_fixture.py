import importlib.util
from pathlib import Path
import tempfile
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def code_module(source):
    module = types.ModuleType('release_version')
    exec(compile(source, '<release-version>', 'exec'), module.__dict__)
    return module


class FridayHistoryFixtureTests(unittest.TestCase):
    def test_identical_current_files_require_different_historical_conclusions(self):
        fixture = load('friday_history', 'benchmarks/friday_history_cases.py')
        runner = load('history_fixture_runner', 'benchmarks/run.py')
        cases = fixture.cases()
        self.assertEqual(cases[0]['files'], cases[1]['files'])
        for case in cases:
            with self.subTest(case=case['id']), tempfile.TemporaryDirectory() as temp:
                project = Path(temp) / 'project'
                runner.prepare(case, project)
                old_producer, old_worker = [code_module(runner.command(
                    ['git', 'show', 'HEAD~1:' + name + '.py'], project))
                    for name in ('producer', 'worker')]
                new_producer, new_worker = [code_module((project / (name + '.py')).read_text())
                                            for name in ('producer', 'worker')]
                queue = [old_producer.enqueue('before'), new_producer.enqueue('during'),
                         old_producer.enqueue('after rollback')]
                self.assertEqual([new_worker.consume(job) for job in queue],
                                 ['before', 'during', 'after rollback'])
                self.assertEqual(old_worker.consume(queue[0]), 'before')
                self.assertEqual(old_worker.consume(queue[2]), 'after rollback')
                if case['id'].endswith('gap'):
                    with self.assertRaises(KeyError):
                        old_worker.consume(queue[1])
                else:
                    self.assertEqual(old_worker.consume(queue[1]), 'during')
                self.assertEqual(runner.command(['git', 'status', '--porcelain'], project), '')
