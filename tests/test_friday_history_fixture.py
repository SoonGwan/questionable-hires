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
    def test_stateless_pair_reuse_preserves_every_phase_observation(self):
        fixture = load('friday_history_reuse', 'benchmarks/friday_history_cases.py')
        case = next(c for c in fixture.cases() if c['id'].endswith('compatible'))
        versions = {'old': case['history'][0]['files'], 'new': case['files']}
        producers = {v: code_module(files['producer.py']).enqueue for v, files in versions.items()}
        workers = {v: code_module(files['worker.py']).consume for v, files in versions.items()}
        titles = ['x', 'queued before rollout', '  spaces  ', '한글 🚀', 'line\nbreak', 'title', 'name']
        observations = []

        def enqueue_checks(label, jobs, active_workers):
            for worker in active_workers:
                for expected, payload in jobs:
                    observations.append((label, worker, expected, dict(payload)))

        for producer in producers:
            enqueue_checks('pair', [(t, producers[producer](t)) for t in titles], workers)
        states = [('baseline', ['old'], ['old']), ('first worker', ['old'], ['old', 'new']),
                  ('producer switch', ['old', 'new'], ['old', 'new']),
                  ('all workers', ['old', 'new'], ['new'])]
        for label, queued, active in states:
            jobs = [(t, producers[p](t)) for p in queued for t in titles]
            enqueue_checks(label, jobs, active)
            jobs += [(t, producers['old'](t)) for t in titles]
            for rollback_workers in (active, sorted(set(active + ['old'])), ['old']):
                enqueue_checks(label + ' rollback', jobs, rollback_workers)

        # This is author-only evidence for these pure fixture functions, not a
        # general memoizer for stateful writers, queues, migrations or services.
        cache, full, reused = {}, [], []
        for label, worker, expected, payload in observations:
            full.append(workers[worker](dict(payload)))
            key = (worker, tuple(sorted(payload.items())))
            if key not in cache:
                cache[key] = workers[worker](dict(payload))
            reused.append(cache[key])
            self.assertEqual(reused[-1], expected, label)
        self.assertEqual(full, reused)
        self.assertEqual(len(full), 392)
        self.assertEqual(len(cache), 28)

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
