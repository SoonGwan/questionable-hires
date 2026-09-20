import unittest
from allocation import reserve

class AllocationTests(unittest.TestCase):
    def test_duplicate_lines_accumulate(self):
        stock = {"a": 8, "b": 4}
        self.assertEqual(reserve(stock, [("a", 2), ("a", 3)]), {"a": 3, "b": 4})
        self.assertEqual(stock, {"a": 8, "b": 4})

    def test_aggregate_shortage_is_atomic(self):
        stock = {"a": 8, "b": 4}
        with self.assertRaisesRegex(ValueError, "insufficient stock"):
            reserve(stock, [("b", 1), ("a", 5), ("a", 4)])
        self.assertEqual(stock, {"a": 8, "b": 4})

    def test_distinct_lines_control(self):
        self.assertEqual(reserve({"a": 8, "b": 4}, [("a", 2), ("b", 3)]), {"a": 6, "b": 1})

    def test_empty_order_control(self):
        stock = {"a": 8}
        result = reserve(stock, [])
        self.assertEqual(result, stock)
        self.assertIsNot(result, stock)

    def test_invalid_order_control(self):
        for lines in [[("a", 0)], [("a", -1)], [("missing", 1)]]:
            with self.subTest(lines=lines), self.assertRaisesRegex(ValueError, "invalid order"):
                reserve({"a": 8}, lines)
