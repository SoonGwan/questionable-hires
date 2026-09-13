#!/usr/bin/env python3
"""New uncommitted graph-fix comparison with explicit execution obligations."""
import argparse
import json
from pathlib import Path


def cases():
    before = '''def order(graph):
    visited = set()
    output = []
    def visit(node):
        if node in visited:
            return
        for dependency in graph[node]:
            visit(dependency)
        visited.add(node)
        output.append(node)
    for node in graph:
        visit(node)
    return output
'''
    after = before.replace('    output = []', '    output = []\n    active = set()').replace(
        '        for dependency',
        '        if node in active:\n            raise ValueError("cyclic dependency")\n'
        '        active.add(node)\n        for dependency').replace(
        '        visited.add(node)', '        active.remove(node)\n        visited.add(node)')
    tests = '''import unittest
import planner

class GraphTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(planner.order({}), [])

    def test_chain(self):
        self.assertEqual(planner.order({"ship": ["build"], "build": ["fetch"], "fetch": []}),
                         ["fetch", "build", "ship"])

    def test_shared_dependency(self):
        self.assertEqual(planner.order({"ship": ["a", "b"], "a": ["base"], "b": ["base"], "base": []}),
                         ["base", "a", "b", "ship"])

    def test_independent_order(self):
        self.assertEqual(planner.order({"b": [], "a": []}), ["b", "a"])

    def check_cycle(self, graph):
        actual = None
        try:
            planner.order(graph)
        except Exception as error:
            actual = (type(error).__name__, str(error))
        self.assertEqual(actual, ("ValueError", "cyclic dependency"))

    def test_self_cycle(self):
        self.check_cycle({"a": ["a"]})

    def test_two_node_cycle(self):
        self.check_cycle({"a": ["b"], "b": ["a"]})
'''
    task = ('Verify the already-present uncommitted planner.py fix against HEAD, without '
            'changing originals. Run all six current test_planner tests unchanged on HEAD '
            'implementation and working implementation in separate project-local copies. '
            'Within each test process, confirm planner.__file__ resolves inside that copy '
            'before executing the native unittest suite. Capture the actual cycle assertion '
            'failures before and passing controls, then all six after outcomes. Identify '
            'the before commit and the working implementation hash. Preserve planner.py, '
            'current test_planner.py and unrelated notes.txt. Delete your comparison copies '
            'before finishing; captured output is sufficient, no retained evidence directory '
            'is required. Do not commit, stash, reset, install dependencies or use external '
            'services. Follow requirements.md and project instructions.')
    return [dict(id='uncommitted-graph-fix', skill='receipt', task=task,
                 files={'AGENTS.md': 'Work only inside this project. Verification only; do not edit original files. Use Python standard library and unittest (-v test_planner). Keep scratch explicitly project-local and remove owned comparison copies before finishing.\n',
                        'requirements.md': 'order(graph) returns dependencies before dependents once each, traversing graph keys and dependency lists in their insertion order. Graph nodes are strings; every dependency is also a key. Empty graphs are valid. Cycles must raise ValueError("cyclic dependency"), not exhaust recursion. Deep acyclic graphs, missing-node policy and concurrent mutation are out of scope. The working fix already exists; this ticket asks only for retrospective verification with the same current tests.\n',
                        'planner.py': before, 'notes.txt': 'Old note.\n'},
                 working_files={'planner.py': after, 'test_planner.py': tests,
                                'notes.txt': 'Unrelated user draft: preserve exactly.\n'},
                 criteria=[
                     'All six unchanged current tests execute on both implementations; before has two cycle assertion failures and four passes, after six passes.',
                     'Each native test process checks its implementation import belongs to its comparison copy.',
                     'Before commit and working implementation hash are identified; original working files remain unchanged.',
                     'Scratch is project-local and comparison copies removed; no commit/stash/reset/install/external actions.'])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
