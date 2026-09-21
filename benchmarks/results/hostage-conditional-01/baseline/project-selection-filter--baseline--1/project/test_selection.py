import unittest
from selection import visible
class Existing(unittest.TestCase):
    def test_archived_and_identity(self):
        a, b = {"project_id": 0}, {"project_id": 1, "archived": True}
        self.assertEqual(visible([a, b]), [a])
        self.assertIs(visible([a])[0], a)
        self.assertEqual(visible([a, b], include_archived=True), [a, b])


class ProjectSelection(unittest.TestCase):
    def test_none_keeps_existing_behavior(self):
        rows = [{"project_id": 0}, {}, {"project_id": 1, "archived": True}]
        self.assertEqual(visible(rows, project_ids=None), rows[:2])
        self.assertEqual(
            visible(rows, project_ids=None, include_archived=True), rows
        )

    def test_one_shot_ids_preserve_order_duplicates_and_identity(self):
        first = {"project_id": 2}
        zero = {"project_id": 0}
        equal_but_distinct = {"project_id": 2}
        rows = [first, {"project_id": 1}, zero, first, equal_but_distinct]
        result = visible(iter(rows), project_ids=iter([0, 2]))
        expected = [first, zero, first, equal_but_distinct]
        self.assertEqual(len(result), len(expected))
        for actual, original in zip(result, expected):
            self.assertIs(actual, original)

    def test_empty_iterables_select_nothing(self):
        rows = [{"project_id": 0}, {"project_id": 1, "archived": True}]
        for ids in ([], (), iter(())):
            with self.subTest(ids=ids):
                self.assertEqual(
                    visible(rows, project_ids=ids, include_archived=True), []
                )

    def test_archived_filter_and_inputs_are_preserved(self):
        rows = [
            {"project_id": 0},
            {"project_id": 0, "archived": True},
            {"project_id": 1, "archived": True},
        ]
        originals = list(rows)
        snapshot = [dict(row) for row in rows]
        ids = [0, 0]
        self.assertEqual(visible(rows, project_ids=ids), rows[:1])
        self.assertEqual(
            visible(rows, project_ids=ids, include_archived=True), rows[:2]
        )
        self.assertEqual(rows, snapshot)
        for actual, original in zip(rows, originals):
            self.assertIs(actual, original)
        self.assertEqual(ids, [0, 0])

    def test_project_ids_is_keyword_only(self):
        with self.assertRaises(TypeError):
            visible([], False, [0])
