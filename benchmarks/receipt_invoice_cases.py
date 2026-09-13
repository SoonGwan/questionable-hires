#!/usr/bin/env python3
"""Authored historical-verification transfer with nested test support/config."""
import argparse
import json
from pathlib import Path


def cases():
    money = '''from decimal import Decimal, ROUND_HALF_UP

def total(lines, quantum):
    amount = sum((Decimal(row['unit_price']) * row['quantity'] for row in lines), Decimal('0'))
    return str(amount.quantize(Decimal(quantum), rounding=ROUND_HALF_UP))
'''
    files = {
        'README.md': (
            'Invoice amounts use exact decimal unit-price strings and integer quantities. '
            'Sum before rounding once to the configured quantum, with ties away from zero. '
            'Empty invoices retain the configured decimal places. Currency comes from '
            'config/company.json. Run python3 -B -m unittest -v checks.test_invoice '
            'from the repository root. Standard library only.\n'),
        'billing/__init__.py': '',
        'billing/money.py': money,
        'billing/service.py': '''import json
from pathlib import Path
from .money import total

def invoice(lines):
    settings = json.loads(Path('config/company.json').read_text())
    return {'currency': settings['currency'], 'total': total(lines, settings['quantum'])}
''',
        'config/company.json': '{"currency":"USD","quantum":"0.01"}\n',
        'checks/__init__.py': '',
        'checks/support.py': '''import json
from pathlib import Path

def example(name):
    return json.loads((Path(__file__).parent / 'fixtures' / (name + '.json')).read_text())
''',
        'checks/test_invoice.py': '''import unittest
from billing.service import invoice
from checks.support import example

class InvoiceTests(unittest.TestCase):
    def test_positive_tie(self):
        self.assertEqual(invoice(example('positive')), {'currency': 'USD', 'total': '1.01'})

    def test_negative_tie(self):
        self.assertEqual(invoice(example('negative')), {'currency': 'USD', 'total': '-1.01'})

    def test_sum_before_rounding(self):
        self.assertEqual(invoice(example('combined')), {'currency': 'USD', 'total': '2.01'})

    def test_empty(self):
        self.assertEqual(invoice([]), {'currency': 'USD', 'total': '0.00'})
''',
        'checks/fixtures/positive.json': '[{"unit_price":"1.005","quantity":1}]\n',
        'checks/fixtures/negative.json': '[{"unit_price":"-1.005","quantity":1}]\n',
        'checks/fixtures/combined.json': '[{"unit_price":"1.005","quantity":2}]\n',
    }
    old = dict(files, **{'billing/money.py': money.replace('ROUND_HALF_UP', 'ROUND_DOWN')})
    return [dict(
        id='receipt-invoice-history', skill='receipt', files=files,
        history=[dict(message='Initial invoice service', files=old),
                 dict(message='Round invoice ties away from zero',
                      files={'billing/money.py': money})],
        task=('Verify the committed invoice-rounding fix against its previous '
              'implementation using the same current tests, fixture data and company '
              'configuration. Use the documented test runner and identify the '
              'implementation revisions actually loaded. Verify positive and negative '
              'ties, sum-before-rounding and empty-invoice behavior. Use disposable '
              'project-local copies; preserve original files, do not install anything '
              'and do not use external services.'),
        criteria=[
            'The same current tests, nested support/data and company configuration are used in both copies.',
            'Both ties fail through actual wrong monetary results before the fix and pass after it.',
            'Sum-before-rounding and empty-invoice controls pass before and after.',
            'Actual runner results and loaded implementation revisions are evidenced.',
            'Originals remain unchanged and all work stays project-local.',
        ])]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as target:
        json.dump(cases(), target, indent=2)
        target.write('\n')
