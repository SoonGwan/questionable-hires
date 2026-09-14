"""Packaging checks for unpromoted candidates; not behavioral model scores."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lean_entries', ROOT/'benchmarks/lean_entries.py')
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


class LeanEntryTests(unittest.TestCase):
    def test_all_eight_preserve_exact_selection_metadata_and_resolve_resources(self):
        skills = {p.name for p in (ROOT/'skills').iterdir() if (p/'SKILL.md').is_file()}
        self.assertEqual(set(candidate.BODIES), skills)
        for name in sorted(skills):
            with self.subTest(skill=name):
                root = ROOT/'skills'/name
                original = (root/'SKILL.md').read_bytes()
                output = candidate.rewrite_entry(name, original)
                self.assertEqual(original.split(b'\n---\n', 1)[0],
                                 output.split(b'\n---\n', 1)[0])
                self.assertLess(len(output), len(original))
                for link in re.findall(r'\]\(([^)]+)\)', output.decode()):
                    target = root/link.split('#')[0]
                    self.assertTrue(target.resolve().is_relative_to(root.resolve()), link)
                    self.assertTrue(target.is_file(), link)
                self.assertEqual((root/'SKILL.md').read_bytes(), original)

    def test_rewriting_is_deterministic_and_does_not_mutate_inputs(self):
        original = (ROOT/'skills/receipt/SKILL.md').read_bytes()
        first = candidate.rewrite_entry('receipt', original)
        self.assertEqual(first, candidate.rewrite_entry('receipt', original))
        self.assertEqual(first, candidate.rewrite_entry('receipt', first))

    def test_invalid_frontmatter_or_unknown_name_refused(self):
        for original in (b'not a skill', b'---\nname: receipt\n'):
            with self.assertRaises(ValueError):
                candidate.rewrite_entry('receipt', original)
        with self.assertRaises(KeyError):
            candidate.rewrite_entry('unknown', (ROOT/'skills/receipt/SKILL.md').read_bytes())


if __name__ == '__main__':
    unittest.main()
