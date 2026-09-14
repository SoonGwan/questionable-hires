# Discovery routing candidate — 2026-09-14

Instruction resource `07fa9e2`; previous candidate `5e957ca`. The initial design
rationale below preceded measurement. The subsequent [four-cell screen](DISCOVERY-ROUTING-01-REVIEW.md)
is adverse/incomplete: atomic skill costs more, Store skill times out after a
connection reset. It does not establish an efficiency improvement.

Checkpoint 06 showed repeated file discovery/keyword inspection in Landlord and
separate instruction discovery after known source reads in Hostage Negotiator.
Their measured pairs were adverse despite supported outcomes. This observation
motivates a routing change; it does not prove discovery caused the whole delta.

Both entrypoints now group missing file/instruction discovery, batch known
relevant reads, and reserve additional search for unresolved coverage/bindings.
Hostage also distinguishes redundant verification from requested repetition,
changed state, nondeterminism and remaining uncertainty. No tool-call quota,
test-count cap, instruction bypass or reduced acceptance scope is introduced.
Landlord still cannot infer absent consumers from narrow discovery, and Hostage
retains state/error/cancellation invariants and bounded async tests.

Both skill-creator validators and the repository validator pass; localization
and featured synchronization are checked. These verify packaging, not model
adoption, maintained task success or reduced time/tokens. No runtime code changed.

The subsequent behavioral check uses the existing native Store review and nested
atomic-export task, not only the tiny cases that motivated this change. Preserve
their original inputs and compare fresh baseline/skill cells after native
preflight. Inspect actual instruction coverage, concrete consumer bindings,
failure-before/fix-after output, exception identity, temporary cleanup and
remaining discovery calls. These existing authored tasks are exposed development
inputs, not holdout or organic customer usage. Freeze scheduling before execution
and retain adverse outcomes; do not change featured figures on this basis.
