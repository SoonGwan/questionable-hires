import asyncio
import unittest
from app.publisher import Publisher

class ExistingTests(unittest.IsolatedAsyncioTestCase):
    async def test_arguments_and_result_identity(self):
        payload, result = object(), object()
        observed = []
        async def write(document_id, *, payload):
            observed.append((document_id, payload))
            return result
        self.assertIs(await asyncio.wait_for(Publisher().publish('doc', payload, write), 1), result)
        self.assertEqual(observed[0][0], 'doc')
        self.assertIs(observed[0][1], payload)

    async def test_exception_identity(self):
        error = ValueError('write failed')
        async def write(document_id, *, payload):
            raise error
        with self.assertRaises(ValueError) as caught:
            await asyncio.wait_for(Publisher().publish('doc', object(), write), 1)
        self.assertIs(caught.exception, error)
