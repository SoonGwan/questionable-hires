import unittest
from build_plan import plan

class PlanTests(unittest.TestCase):
    def test_chain(self):
        graph = {"ship": ["compile"], "compile": ["fetch"], "fetch": []}
        result = plan(graph)
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result), {"fetch", "compile", "ship"})

    def test_cycle(self):
        with self.assertRaisesRegex(ValueError, "dependency cycle"):
            plan({"a": ["b"], "b": ["a"]})

    def test_independent_nodes(self):
        self.assertEqual(set(plan({"a": [], "b": []})), {"a", "b"})
        self.assertEqual(plan({}), [])
