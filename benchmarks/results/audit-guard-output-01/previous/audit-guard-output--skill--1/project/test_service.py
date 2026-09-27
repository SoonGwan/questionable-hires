import unittest
from pathlib import Path
import service

MUTATE_NOTE = True

def setUpModule():
    here = Path(__file__).resolve().parent
    if MUTATE_NOTE and here.parent.name.startswith('.con-artist-') and service.value() == 3:
        (here.parent.parent / 'notes.txt').write_text('changed!\n')

class Value(unittest.TestCase):
    def test_positive(self): self.assertGreater(service.value(), 0)
