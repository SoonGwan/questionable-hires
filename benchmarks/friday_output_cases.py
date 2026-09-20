"""Authored SQL-only release/output tasks; no model performance claims."""
import json
from pathlib import Path
import runpy
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    '001.sql': "CREATE TABLE stock(sku TEXT PRIMARY KEY, quantity INTEGER NOT NULL);\n"
               "INSERT INTO stock VALUES ('A',10),('C',0);\n"
               "CREATE VIEW legacy_stock AS SELECT sku, quantity AS units FROM stock;\n",
    '002.sql': "ALTER TABLE stock ADD COLUMN reserved INTEGER NOT NULL DEFAULT 0;\n"
               "DROP VIEW legacy_stock;\n"
               "CREATE VIEW legacy_stock AS SELECT sku, quantity-reserved AS units FROM stock;\n",
    '003.sql': "UPDATE stock SET quantity=12, reserved=5 WHERE sku='A';\n"
               "INSERT INTO stock VALUES ('B',4,1);\n",
    '004.sql': "DROP VIEW legacy_stock;\n"
               "CREATE VIEW legacy_stock AS SELECT sku, quantity AS units FROM stock;\n",
    'readers.py': "OLD = 'SELECT sku, units FROM legacy_stock ORDER BY sku'\n"
                  "NEW = 'SELECT sku, quantity-reserved AS units FROM stock ORDER BY sku'\n",
}
RELEASE = '''# Stock release contract
This is an authored SQL-only SQLite review. Literal queries in readers.py define
the complete consumers; no application runtime, concurrent transactions, crash
recovery or other engine is in scope. No dependencies or external services.

OLD requires ordered columns [sku, units], one complete row per SKU in lexical
order, where units is total quantity, including reserved stock. NEW requires the
same columns/order but units is quantity minus reserved. Neither permits omitting
zero values. Expected total quantities initially are A=10, C=0; after writes,
A=12, B=4, C=0. Reservations after writes are A=5, B=1, C=0.

Review this exact order: (1) 001.sql, OLD active; (2) 002.sql, OLD active;
(3) 003.sql, OLD and NEW active; (4) drain NEW and restart OLD with no SQL;
(5) 004.sql, OLD active. Evaluate both literal queries at all five phases,
including inactive consumers, but inactive errors alone are not blockers.
All quantities and reservations written at step 3 must survive step 5. No
zero-downtime or deployment authorization beyond this proposed sequence is implied.
Do not change SQL, contracts, files or Git state. Any necessary scratch must be
project-local and removed; prefer in-memory execution. Report scoped limitations.
'''


def build_cases():
    cases = []
    common = ('Read release.md and review the exact SQL proposal without fixing or deploying it. '
              'Execute the actual supplied SQL and both literal readers at every phase. '
              'Compare full ordered columns/rows with the explicit contracts, including zero '
              'values and committed quantity/reservation survival after rollback. Identify the '
              'first incompatible step, last compatible checkpoint and a scoped mitigation; '
              'distinguish inactive-reader errors from active failures. Preserve supplied files '
              'and Git state, leave no scratch, and use no dependencies/external services. ')
    criteria = [
        'Actual five-phase SQL execution with both literal queries at each phase; full ordered columns/rows and zero-valued SKU checked against contracts.',
        'Find semantic OLD failure after new writes at step 3, continuing through step 4, not at step 2; step 2 is last compatible checkpoint. NEW step-1 error is inactive.',
        'Verify down restores OLD totals and retains quantities/reservations, with supported mitigation and SQL-only limitations.',
        'Preserve supplied files, Git HEAD/index and skill resources; no external activity or leftover scratch.',
    ]
    for mode in ('contracts', 'observations'):
        extra = ('Give a concise evidence-backed decision with phase/check outcomes and decisive '
                 'expected/observed mismatches. A full raw matrix is not requested; keep the '
                 'verification reproducible and identify the reader file/constants used.')
        if mode == 'observations':
            extra = ('Also print a complete machine-readable JSON observation record to command '
                     'output: ordered phases with names, each reader\'s ordered columns and full '
                     'rows or actual error, and completion/truncation information. Include reader '
                     'provenance (file, constant, source line, byte SHA-256, exact SQL). Do not '
                     'replace this requested raw record with only pass/fail summaries. Final '
                     'answer may summarize and point to the recorded command output.')
        cases.append(dict(id='stock-' + mode, skill='friday',
                          files={**FILES, 'release.md': RELEASE}, task=common + extra,
                          criteria=criteria + [extra],
                          provenance={'kind': 'Related authored synthetic tasks, not independent real-world holdouts',
                                      'output_contract': mode}))
    return cases


def preflight():
    helper = runpy.run_path(str(ROOT / 'skills/friday/scripts/sqlite_matrix.py'))
    recipe = {'phases': [{'name': 'initial', 'files': ['001.sql']},
                         {'name': 'up', 'files': ['002.sql']},
                         {'name': 'writes', 'files': ['003.sql']},
                         {'name': 'old restart'},
                         {'name': 'down', 'files': ['004.sql']}],
              'checks': {name: {'python_file': 'readers.py', 'constant': name}
                         for name in ('OLD', 'NEW')}}
    with tempfile.TemporaryDirectory(prefix='stock-preflight-', dir=ROOT / 'benchmarks') as scratch:
        root = Path(scratch)
        for name, content in FILES.items():
            (root / name).write_text(content)
        before = {p.name: p.read_bytes() for p in root.iterdir()}
        result = helper['matrix'](recipe, root)
        if not result['complete'] or len(result['phases']) != 5:
            raise AssertionError(result)
        controls = []
        for i in range(5):
            total = [('A', 10), ('C', 0)] if i < 2 else [('A', 12), ('B', 4), ('C', 0)]
            available = [('A', 10), ('C', 0)] if i < 2 else [('A', 7), ('B', 3), ('C', 0)]
            for name in ('OLD', 'NEW'):
                if i == 0 and name == 'NEW':
                    observation = result['phases'][i]['checks'][name]
                    if observation['ok'] or 'no such column: reserved' not in observation['error']:
                        raise AssertionError(observation)
                    controls.append(dict(phase=i, check=name, outcome='expected inactive error', detail=observation['error']))
                    continue
                expected = total if name == 'OLD' else available
                try:
                    helper['assert_rows'](result, i, name, columns=['sku', 'units'], rows=expected)
                except AssertionError as error:
                    if name != 'OLD' or i not in (2, 3):
                        raise
                    message = str(error)
                    if 'expected' not in message or 'observed' not in message or "('A', 12)" not in message or "('A', 7)" not in message:
                        raise AssertionError(message)
                    controls.append(dict(phase=i, check=name, outcome='expected contract failure', detail=message))
                else:
                    if name == 'OLD' and i in (2, 3):
                        raise AssertionError('Missing semantic incompatibility')
                    controls.append(dict(phase=i, check=name, outcome='contract pass'))
        survival_recipe = {**recipe, 'checks': {'stored': 'SELECT sku, quantity, reserved FROM stock ORDER BY sku'}}
        survival = helper['matrix'](survival_recipe, root)
        helper['assert_rows'](survival, 4, 'stored', columns=['sku', 'quantity', 'reserved'],
                              rows=[('A', 12, 5), ('B', 4, 1), ('C', 0, 0)])
        if before != {p.name: p.read_bytes() for p in root.iterdir()}:
            raise AssertionError('Source files changed')
        # Separate author-only compatible proposal; never supplied to the model.
        healthy_sql = FILES['002.sql'].replace('quantity-reserved AS units', 'quantity AS units')
        healthy_recipe = {**recipe, 'phases': [dict(phase) for phase in recipe['phases']]}
        healthy_recipe['phases'][1] = {'name': 'up', 'sql': healthy_sql}
        healthy = helper['matrix'](healthy_recipe, root)
        for i in range(5):
            expected = [('A', 10), ('C', 0)] if i < 2 else [('A', 12), ('B', 4), ('C', 0)]
            helper['assert_rows'](healthy, i, 'OLD', columns=['sku', 'units'], rows=expected)
        if before != {p.name: p.read_bytes() for p in root.iterdir()}:
            raise AssertionError('Healthy control changed source files')
    return dict(observations=json.loads(helper['format_result'](result)), controls=controls,
                survival=json.loads(helper['format_result'](survival)),
                compatible_proposal=json.loads(helper['format_result'](healthy)), originals_preserved=True)


if __name__ == '__main__':
    print(json.dumps(dict(cases=build_cases(), preflight=preflight()), ensure_ascii=False, indent=2))
