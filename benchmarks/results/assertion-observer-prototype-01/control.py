import json
import sys
import unittest
from observer import observe

class NoRepresentation:
    def __repr__(self): raise AssertionError('unexpected repr')

class Contract(unittest.TestCase):
    def test_equal(self): self.assertEqual([1, b'\x00\xff'], [1, b'\x00\xff'])
    def test_identity(self): self.assertIsNot(NoRepresentation(), NoRepresentation())
    def test_regression(self): self.assertEqual(1, 2 if 'broken' in sys.argv else 1)

if 'existing-profile' in sys.argv:
    callback=lambda *args: None
    sys.setprofile(callback)
    try:
        try: observe()
        except RuntimeError: pass
        else: raise AssertionError('replaced existing profile')
        assert sys.getprofile() is callback
    finally: sys.setprofile(None)
    print('existing profile preserved')
    raise SystemExit(0)
rows=errors=None
try:
    if 'observe' in sys.argv: rows,errors=observe()
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Contract))
finally:
    sys.setprofile(None)
if rows is not None:
    assert len(rows)==3 and not errors
    assert rows[1]['method']=='assertIsNot'
    print(json.dumps({'observations':rows,'errors':errors}))
raise SystemExit(not result.wasSuccessful())
