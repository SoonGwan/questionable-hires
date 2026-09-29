import unittest
from dispatch import dispatch


class DispatchTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(dispatch({"id": 1}, [lambda p: "first", lambda p: "second"]), ["first", "second"])

    def test_payload_isolation(self):
        payload = {"items": [1]}
        def mutate(value):
            value["items"].append(2)
            return value
        self.assertEqual(dispatch(payload, [mutate, lambda p: p]), [{"items": [1, 2]}, {"items": [1]}])
        self.assertEqual(payload, {"items": [1]})


if __name__ == "__main__":
    unittest.main()
