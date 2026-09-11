# Landlord compression: behavior retained, no measured efficiency win

[Frozen protocol](LANDLORD-COMPACT-PROTOCOL.md), runner `69f327c`.
Previous resources `19af8ae` (entrypoint `5f67c6e`), candidate `09cc591`.
One exposed Store task, fresh Astra medium sessions, previous then candidate,
serial, 240-second limit, no retries/exclusions. Local originals:
`local-runs/landlord-compact-01/`. Both arms explicitly load Landlord; neither
is a no-skill baseline.

[Inspectable exported evidence](results/landlord-compact-01/README.md) includes
both command/output traces, answers, metadata and synthetic final projects.
Private original logs remain local; exported local paths are redacted.

| Version | Input + output tokens | Seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Previous | 68,427 | 34.981 | 5 |
| Compact | 68,495 | 41.409 | 5 |

Candidate +0.10% tokens / +18.38% time. Input/output: previous 67,619/808,
candidate 67,684/811; cached inputs 54,912/55,936 are included once, not added.
Entrypoint shrinks 278 → 212 whitespace-delimited words, 2,048 → 1,615 bytes.
This reduces instruction text, not observed whole-session token cost.

Both run the documented two-test contract group and a separate direct-Backend
probe with successful exits and complete decisive output. Actual probes show
creation returning None, duplicates raising Duplicate, original value preservation
and OSError propagation. Both recommend keeping semantic translation, explain
that compatible inlining moves driver policy into service.save, and use a future
driver-signaling change to ground maintenance cost. Neither edits implementation,
fabricates a staging receipt nor claims unavailable staging verification.

Both retain line-numbered source on first reading and use five commands. Previous
loads the skill separately before source; candidate combines skill/source reads
but reads tests separately. Candidate's initial discovery lists .git internals
because of its glob selection, before it reads the changed skill body. Do not
attribute this initial choice or the timing difference solely to compression.

All twelve original file instances match fixture bytes; final diffs are empty.
All four installed resource instances match the frozen Git content and before/
after inventories. Original output and redacted records match after the intended
path substitutions. No capture flags, timeout or event errors; decisive outputs
were inspected rather than treating flag absence as proof. No author replay is
credited as model execution.

The compact entrypoint remains a smaller candidate with preserved behavior in
this one regression, **not a validated performance improvement**. Shared host/cache,
fixed order, single repeat and exposed synthetic task limit attribution. Retain
the [earlier adverse citation result](LANDLORD-CITATION-01.md); don't pool this
previous-versus-candidate pair with no-skill comparisons or repeat unchanged cells
for a favorable score. Further efficiency work must reduce actual work, not assume
that wording compression translates into an equivalent total-token reduction.
