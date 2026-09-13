import unittest
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
