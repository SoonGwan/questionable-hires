import unittest
from pathlib import Path
from rule import eligible

MUTATE_NOTE = False

def setUpModule():
    here = Path(__file__).resolve().parent
    if MUTATE_NOTE and here.parent.name.startswith('.receipt-'):
        (here.parent.parent / 'notes.txt').write_text('changed!\n')

class Boundary(unittest.TestCase):
    def test_boundary(self): self.assertEqual(eligible(18), True)
    def test_below(self): self.assertEqual(eligible(17), False)
    def test_above(self): self.assertEqual(eligible(19), True)
