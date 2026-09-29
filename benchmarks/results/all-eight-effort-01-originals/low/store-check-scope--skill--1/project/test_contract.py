import unittest
from backend import Backend
from service import save
from store import Store

class Contract(unittest.TestCase):
    def test_new_and_existing(self):
        for key in ('first', 'second', ''):
            with self.subTest(key=key):
                backend = Backend()
                store = Store(backend)
                self.assertIs(save(store, key, 'original')['created'], True)
                self.assertIs(save(store, key, 'replacement')['created'], False)
                self.assertEqual(backend.rows[key], 'original')
    def test_operational_failure_is_not_duplicate(self):
        class Offline:
            def put(self, key, value):
                raise OSError('offline')
        with self.assertRaisesRegex(OSError, 'offline'):
            save(Store(Offline()), 'key', 'value')
