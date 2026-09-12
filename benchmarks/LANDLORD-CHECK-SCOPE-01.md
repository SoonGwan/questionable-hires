# Correct check scope, no efficiency advantage

Snapshot 9020c6d, fixture/protocol 84be5b5, Landlord c66db8f, runner fd8d578.
One fresh Astra medium baseline/skill pair, baseline first, serial seed 20260911,
240-second deadline. No retries, exclusions or candidate edits. Private original
outputs remain in `local-runs/landlord-check-scope-01/`.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| baseline | 65,062 | 30.580 | 5 |
| skill | 69,110 | 34.510 | 5 |

Skill uses **6.2% more tokens / 12.9% more time**. Cached input is already included.
This single synthetic pair is descriptive, not causal evidence for the new wording.

Both run the documented complete lightweight contract group (two tests, with
three key subcases inside one test), not a custom subset or broad discovery.
Both execute an additional in-memory probe showing that direct Backend use changes
successful creation to None and duplicates to exceptions, while preserving the
original value and operational-error propagation. Commands capture actual outputs
and successful independent exits for both the probe and contract tests.

Both recommend retaining the adapter's semantic responsibility. Baseline explicitly
allows inlining if the translation moves into service.save and notes the modest
tradeoff for one caller. Skill grounds keeping the boundary in changing driver
exception semantics. Neither equates fewer classes with lower maintenance cost.
No implementation changes or manufactured staging evidence. Both explicitly state
staging remains unverified and do not execute the unavailable staging group.

Both read the project once, then reread several small files with line numbers for
references. Skill's first discovery also lists .git internals because of its glob
selection; it stays inside the allowed project, and this occurs before reading
the skill body. Do not attribute that initial command to the new test-selection
guidance. Equal shell counts and largely equivalent behavioral checks provide no
observed execution-work reduction in this task.

All twelve original file copies match the frozen fixture. No staging receipt
exists. Both installed skill resources match frozen Git hashes and before/after
manifests; no capture flags, patch rejections, event errors or timeouts. Original
commands remain scoped. No author replay is credited as model execution.

Repository validation passes. The prior 158-test author run validates fixture and
repository mechanics, not model performance. This transfer confirms appropriate
known check scope for both arms, not spontaneous runtime estimation or a causal
advantage for Landlord. No new skill rule or repeated exposed-case run is justified
by this result; the overall performance objective remains unmet.
