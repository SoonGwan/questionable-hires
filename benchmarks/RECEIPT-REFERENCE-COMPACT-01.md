# Receipt reference consolidation: smaller input, unmeasured performance

The [range pair](results/receipt-ranges-01/README.md) actually adopted watch/report
without a custom wrapper, but used **43.79% more tokens** despite 39.99% lower
process time. Its trace loads the entire existing-fix reference. That is evidence
of loading, not causal proof that this reference explains the cost difference.

Only `skills/receipt/references/existing-fix.md` changes. Entrypoint/description,
automatic selection, helper implementation and UI metadata remain unchanged.
The reference is consolidated in place, with no new mandatory reference layer:
895 → 566 whitespace-separated words; 6,983 → 4,726 bytes. This is **resource
arithmetic**, not model-token savings or a before/after performance experiment.

Preserved obligations and interfaces:

- Same current assertions/inputs on isolated implementations, comparable runtime
  and configuration; existing evidence reuse, incompatibility disclosure, no
  dependency installs and no substitution for a pre-edit failure requirement.
- Targeted support discovery, no unnecessary repository reinventory; optional
  helper preference with native fallback and no routine implementation loading.
- Both literal committed/uncommitted CLI examples remain unchanged. Explicit
  revision selection, working-vs-staged distinction and snapshot identities remain.
- Fixed/vary/watch semantics, hidden directory leaves, disjoint selections,
  path/symlink/Git/root/empty-directory restrictions and entry/byte budgets remain.
- Watch-only originals, reusable hash/mode/cleanup report, broader integrity
  limits, child-local temp defaults and no global-TMPDIR workaround remain.
- Actual assertions/coverage/import provenance, individual statuses, truncation,
  no-execution behavior, timeout/child cleanup, no automatic retry while exit is
  unconfirmed, non-atomic snapshots and non-sandbox boundaries remain.

The skill-creator principle applied is to consolidate repeated instructions while
retaining decision-changing constraints. No test obligation or skill capability
was removed to make a comparison cheaper. Existing caller paths remain valid.

Focused helper suite: **40 tests pass (12.052 seconds)**, including executing both
literal reference commands against real Git fixtures and actual failure/pass
assertions. Skill/catalog validation and featured synchronization checks pass.
This author validation checks executable examples and helper behavior, not whether
a model reliably retains every prose constraint or improves end-to-end efficiency.
Full repository suite: **350 tests pass (50.017 seconds)**, including packaging;
no resource edits occurred during validation.

Further confirmation must use separate realistic tasks and preserve prior costs,
outcomes and all-eight scope. Do not rerun the exposed range task for a favorable
score. No featured/localized chart or historical measurement changes here.
