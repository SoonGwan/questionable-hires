# Friday core guide — less routine reading, unchanged execution

2026-09-14, previous reference source `c1f639c`. The rolling-schema skill cell in
[checkpoint 07](BUNDLE-CONTRACT-07-REVIEW.md) read the core SQLite guide and ran
the helper once, yet used more tokens than its baseline. That result does not
prove the guide caused the difference; verification artifacts and work differed.
It does identify a routinely loaded resource worth making less repetitive.

The core guide now keeps the CLI/API examples, phase defaults, literal-reader
selection, provenance limits, successful/failed/truncated result interpretation,
result reuse, exit codes and database/path/budget restrictions. Detailed BLOB JSON,
input-shape rejection and migration/budget error fields move to the existing
details reference. The core explicitly routes those needs there; no new mandatory
file read or wrapper API is introduced. Production safety still requires actual
runtime evidence. No executable code or historical result changes.

| Reference size | Before | Candidate |
| --- | ---: | ---: |
| Core UTF-8 bytes | 4,884 | 3,645 |
| Core whitespace-delimited words | 646 | 473 |
| Core + details bytes | 7,387 | 7,205 |
| Core + details words | 1,005 | 976 |

Core bytes decrease **25.37%**; total reference bytes decrease only **2.46%**.
This is progressive disclosure, not deleting all detailed guidance. These are
file sizes, **not model tokens**, actual read behavior or task-performance gains.
A task requiring the detailed document may read both; model adoption/cost for
this candidate remains unmeasured. Do not promote this into a benchmark chart.

## Verification

The existing 35 native SQLite matrix tests pass in 0.398s, including execution
of the actual core JSON recipe and API example with BLOB results. They cover
successful and incompatible readers, rollback preserving new data, empty/duplicate
columns, real consumer column failure, denied writes/external databases, truncation,
input rejection and budget exhaustion. No tests were removed or rewritten for
the shorter guide. The script and skill entrypoint remain byte-identical.

The skill-creator principle applied here is progressive disclosure: move conditional
detail to an existing routed reference and preserve information that changes a
decision. This is a documentation candidate, not proof that a model reads less
or performs all release reviews correctly. Existing adverse results stay linked.
