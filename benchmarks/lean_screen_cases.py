"""Fixed all-eight development selection; old task exposure is disclosed."""
import copy
import hashlib
import json
from pathlib import Path

from cases_view_contract import CASE as FRIDAY

ROOT = Path(__file__).resolve().parent
SELECTION = (
    ('history-invoice-01-cases.json', 'history-invoice-boundary', 'necromancer'),
    ('receipt-ledger-cases.json', 'ledger-delivery-b', 'receipt'),
    ('landlord-check-scope-cases.json', 'store-check-scope', 'landlord'),
    ('editor-snapshot-01-cases.json', 'editor-snapshot-present', 'mother-in-law'),
    ('exorcist-runtime-cases.json', 'runner-environment-timing', 'exorcist'),
    ('hostage-refresh-cases.json', 'refresh-owner-a', 'hostage-negotiator'),
    ('con-artist-sqlite-cases.json', 'sqlite-commit-audit', 'con-artist'),
)


def cases():
    selected = []
    for filename, identity, skill in SELECTION:
        matches = [c for c in json.loads((ROOT/filename).read_text()) if c['id'] == identity]
        if len(matches) != 1 or matches[0]['skill'] != skill:
            raise ValueError('Selection does not match frozen role: ' + identity)
        selected.append(matches[0])
    friday = copy.deepcopy(FRIDAY)
    phrase = ' using $friday'
    if friday['task'].count(phrase) != 1:
        raise ValueError('Unexpected Friday task: review neutralization before execution')
    friday['task'] = friday['task'].replace(phrase, '')
    selected.append(friday)
    if len({c['skill'] for c in selected}) != 8 or len({c['id'] for c in selected}) != 8:
        raise ValueError('Expected eight distinct cases and roles')
    return selected


def source_hashes():
    names = [s[0] for s in SELECTION] + ['cases_view_contract.py', 'lean_screen_cases.py']
    return {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in names}
