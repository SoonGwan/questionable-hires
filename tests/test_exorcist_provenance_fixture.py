import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


class ProvenanceFixtureTests(unittest.TestCase):
    def test_success_counts_hide_cross_tenant_origin(self):
        path = Path(__file__).resolve().parents[1] / 'benchmarks/exorcist-provenance-cases.json'
        case = json.loads(path.read_text())[0]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, contents in case['files'].items():
                (root / name).write_text(contents)
            modules = {}
            for name in ('invoices', 'worker'):
                spec = importlib.util.spec_from_file_location(name, root / (name + '.py'))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules[name] = module
            for ids, expected_reads, expected_text in [
                ((7, 7), [('alpha', 7)], ['alpha:7', 'alpha:7']),
                ((7, 8), [('alpha', 7), ('beta', 8)], ['alpha:7', 'beta:8']),
            ]:
                with self.subTest(ids=ids):
                    reads = []
                    def read(tenant, invoice):
                        reads.append((tenant, invoice))
                        return f'{tenant}:{invoice}'
                    service = modules['invoices'].Invoices(read)
                    responses = [modules['worker'].handle(
                        dict(tenant=tenant, invoice=invoice), service)
                        for tenant, invoice in zip(('alpha', 'beta'), ids)]
                    self.assertEqual(sum(r['ok'] for r in responses), 2)
                    self.assertEqual(reads, expected_reads)
                    self.assertEqual([r['text'] for r in responses], expected_text)
            for name, contents in case['files'].items():
                self.assertEqual((root / name).read_text(), contents)


if __name__ == '__main__':
    unittest.main()
