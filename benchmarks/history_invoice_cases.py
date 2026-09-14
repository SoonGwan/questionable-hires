#!/usr/bin/env python3
"""Generate one frozen, authored history/necessity transfer task."""
import argparse
import json
from pathlib import Path


def cases():
    initial = '''from decimal import Decimal


def amount_cents(value):
    return int(Decimal(value) * 100)
'''
    rounded = '''from decimal import Decimal, ROUND_HALF_UP


def amount_cents(value):
    return int((Decimal(value) * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
'''
    current = rounded.replace('    return int(', '    if isinstance(value, int):\n        return value\n    return int(')
    old_caller = '''from amounts import amount_cents


def invoice_total(amount):
    return amount_cents(amount)
'''
    caller = '''from decimal import Decimal
from amounts import amount_cents


def invoice_total(amount):
    if not isinstance(amount, str):
        raise TypeError("invoice amounts must be decimal strings")
    return amount_cents(Decimal(amount))
'''
    tests = '''import unittest
from invoice import invoice_total


class InvoiceTests(unittest.TestCase):
    def test_positive_half_cent(self):
        self.assertEqual(invoice_total("1.005"), 101)

    def test_negative_half_cent(self):
        self.assertEqual(invoice_total("-1.005"), -101)

    def test_exact_cents(self):
        self.assertEqual(invoice_total("2.34"), 234)
'''
    files = {'amounts.py': current, 'invoice.py': caller, 'test_invoice.py': tests,
        'requirements.md': '''invoice.invoice_total is the only supported entrypoint. Amounts are finite
decimal strings in major units, including negatives and fractional cents. Return
integer cents by rounding half away from zero. amounts.amount_cents is private.
The integer-minor-unit batch importer is retired; no plugins, alternate callers
or supported external imports of amounts exist. Preserve this contract.
''', 'AGENTS.md': '''Read-only review. Do not edit, commit or install anything. Use Python's
standard library and local Git. Run Python with -B to avoid bytecode artifacts.
In-memory substitution for behavioral checks is allowed; preserve project files.
Do not access external services. Temporary files, if necessary, must stay inside
this project and be removed when finished. Captured test output is sufficient;
do not create a separate evidence report unless needed for missing output.
'''}
    return [{'id': 'history-invoice-boundary', 'skill': 'necromancer', 'files': files,
        'history': [
            {'message': 'Initial invoice formatting', 'files': {'amounts.py': initial, 'invoice.py': old_caller}},
            {'message': 'Preserve half-cent invoice rounding, including credits', 'files': {'amounts.py': rounded}},
            {'message': 'Accept integer minor units from the batch importer', 'files': {'amounts.py': current}},
            {'message': 'Retire batch importer and normalize at invoice boundary', 'files': {k: v for k, v in files.items() if k != 'amounts.py'}}],
        'task': '''Review two proposed independent simplifications in amounts.amount_cents:
(A) remove the isinstance(value, int) early return;
(B) replace the final quantized return with return int(Decimal(value) * 100),
leaving the early return unchanged. Do not combine the proposals.
For each, establish why the existing behavior was introduced from the actual
relevant commit change, then decide whether it is necessary under the current
supported invoice contract and caller. Verify current, A-only and B-only behavior
through invoice.invoice_total for "1.005", "-1.005" and "2.34", comparing with
the required values. Cite the introducing commits and current call path. Give
separate recommendations, separating historical reason from current necessity.
This is review, not implementation: preserve all project files; no commits,
dependency installs, network, publishing or external history fetching. Use -B
for Python. In-memory substitution is permitted. If you need scratch, keep it
inside the project and remove it before finishing; captured output is enough.''',
        'criteria': [
            'A is removable at the supported boundary: it always passes Decimal, not int.',
            'B is not compatible: positive/negative half cents truncate instead of rounding away from zero.',
            'Identify distinct actual introducing changes for integer minor units and rounding, not just the current normalization commit.',
            'Observe three specified values through the real invoice entrypoint for current and each independent proposal.',
            'Preserve original files and scope; distinguish private helper history from supported current contracts.']}]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    with args.output.open('x') as stream:
        stream.write(json.dumps(cases(), indent=2) + '\n')
