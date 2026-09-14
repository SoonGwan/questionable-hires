# Native-probe routing candidate 01 — 2026-09-14

Previous source `bf571bc`. In [SQLite transfer 01](CON-ARTIST-SQLITE-01-REVIEW.md)
the model used native file probes correctly, but read the complete advanced guide
for that interface, including unused batch, import-root and diagnostic sections.
The skill cell used 99,868 tokens versus baseline 86,152; unequal work and the
baseline capture gap prevent attributing that difference to these reads alone.

Move native file-probe instructions into
[python-audit-probes.md](../skills/con-artist/references/python-audit-probes.md).
The common guide points directly there. The old advanced `#stronger-probes`
heading remains as a compatibility link, with no duplicated interface body.
The new guide preserves same-runner native fixture use, correct/faulty isolation,
conditional-probe semantics, input collisions/limits, pytest collection/exit
propagation and links for batch/diagnostics only when needed. Its executable
example uses standard-library unittest and retains existing plus binary data.
SKILL.md and runtime scripts are unchanged.

| Reading path / inventory | Bytes |
| --- | ---: |
| Previous common + entire advanced guide | 15,136 |
| Candidate common + native-probe guide | 7,785 |
| All three candidate guides | 15,725 |

The relevant two-document path is **48.57% smaller**; total documentation is
**3.89% larger**. These are byte counts, not model tokens or measured adoption.
An agent that loads every guide still pays more. Do not advertise a 48.57% model
improvement or update frozen charts from these figures.

Local validation:

- 12 packaging tests pass in 3.413s. Extended existing execution coverage extracts
  the actual shipped native-probe JSON, combines it with the shipped CLI recipe,
  and runs the built package from paths containing spaces. Correct native probe
  passes, mutant probe fails with the intended binary stored-record AssertionError;
  both report one actual test. Original files/modes and scratch cleanup remain
  checked. Original single/batch recipes and wrong-binding negative controls pass.
- 76 mutation-helper tests pass in 13.972s, retaining collision, collection,
  timeout, integrity, native-probe and conditional/batch controls.
- Catalog/local links and skill structure validate. No model timing overlaps tests.

Next evidence is actual model routing and task outcomes after this change, not
another byte count. Preserve the SQLite baseline's original output gap and all
earlier adverse costs. This candidate does not establish all-eight performance
or hosted release readiness.

The subsequent [model screen](CON-ARTIST-PROBE-ROUTING-MODEL-01-REVIEW.md) adopts
the focused path and retains the four native phases. Its descriptive cost changes
are much smaller than the document-byte reduction and do not prove causality.
