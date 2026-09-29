import json
import sys
import unittest
import observer

class NoRepresentation:
    def __repr__(self): raise AssertionError('unexpected repr')

class Contract(unittest.TestCase):
    def test_equal(self): self.assertEqual([1, b'\x00\xff'], [1, b'\x00\xff'])
    def test_identity(self): self.assertIsNot(NoRepresentation(), NoRepresentation())
    def test_regression(self): self.assertEqual(1, 2 if 'broken' in sys.argv else 1)

mode=sys.argv[1]
if mode=='existing-profile':
    callback=lambda *args: None
    sys.setprofile(callback)
    try:
        try:observer.observe()
        except RuntimeError:pass
        else:raise AssertionError('hook replaced')
        assert sys.getprofile() is callback
    finally:sys.setprofile(None)
    raise SystemExit(0)
if mode=='encoder-error':
    def broken(*args):raise ValueError('controlled observer failure')
    observer.encode=broken
report=None
try:
    if mode!='off':report=observer.observe(max_bytes=128 if mode=='byte-limit' else 4096,max_records=1 if mode=='record-limit' else 64)
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
finally:
    output=report.close() if report else None
if report:
    value=json.loads(output)
    assert len(output.encode('ascii')) <= (128 if mode=='byte-limit' else 4096)
    assert not value['complete']
    print(output)
raise SystemExit(not result.wasSuccessful())
