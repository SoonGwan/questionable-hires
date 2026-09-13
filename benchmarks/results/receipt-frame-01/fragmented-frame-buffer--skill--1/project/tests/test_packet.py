import unittest
from packet import Decoder


def frame(payload):
    return len(payload).to_bytes(2, 'big') + payload


class DecoderTests(unittest.TestCase):
    def test_complete_batch_and_empty_frame(self):
        decoder = Decoder()
        self.assertEqual(decoder.feed(frame(b'one') + frame(b'') + frame(b'two')), [b'one', b'', b'two'])
        self.assertEqual(decoder.feed(b''), [])

    def test_split_header(self):
        decoder = Decoder()
        encoded = frame(b'hello')
        self.assertEqual(decoder.feed(encoded[:1]), [])
        self.assertEqual(decoder.feed(encoded[1:]), [b'hello'])

    def test_instances_are_independent(self):
        first, second = Decoder(), Decoder()
        self.assertEqual(first.feed(b'\x00'), [])
        self.assertEqual(second.feed(frame(b'x')), [b'x'])
        self.assertEqual(first.feed(b'\x01y'), [b'y'])

    def test_partial_payload_with_empty_feed(self):
        decoder = Decoder()
        encoded = frame(b'hello')
        self.assertEqual(decoder.feed(encoded[:3]), [])
        self.assertEqual(decoder.feed(b''), [])
        self.assertEqual(decoder.feed(encoded[3:]), [b'hello'])
        self.assertEqual(decoder.feed(b''), [])

    def test_complete_then_partial_then_multiple(self):
        decoder = Decoder()
        pending = frame(b'world')
        self.assertEqual(decoder.feed(frame(b'first') + pending[:4]), [b'first'])
        self.assertEqual(decoder.feed(pending[4:] + frame(b'last')), [b'world', b'last'])
        self.assertEqual(decoder.feed(b''), [])
