import os
import unittest
from unittest.mock import patch
import worker

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(os.environ, {'REQUEST_RETRIES': '0'})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def test_disabled_retries(self):
        calls = []
        def send():
            calls.append('attempt')
            raise RuntimeError('offline failure')
        with self.assertRaises(RuntimeError):
            worker.deliver(send)
        self.assertEqual(len(calls), 1)
