# Success-state false-pass correction

Implementation: `b7058c6`. This is executable regression evidence, **not a new
model efficiency result**. The prior recovery experiment remains tied to `699cdba`;
its 17.2% token / 67.0% time savings do not measure this revision.

## Demonstrated failures, then fixes

Three new behavioral tests were run against the existing helper before editing
it. All three failed because the helper incorrectly accepted the relevant cases.
After the correction, all 13 helper tests pass, including the three regressions.

| Component behavior | Prior observation | Corrected observation |
| --- | --- | --- |
| Writes the right result, then raises `RuntimeError` from a success callback | Case passed despite captured exception | Case fails and identifies query/exception |
| Older success preserves result but pollutes the error field | Stale-success case passed | Stale-success case fails |
| First success displays an error, second success clears it | Normal sequence passed | Normal and normal-boundary fail at the first checkpoint |

The transient-error test verifies that the final error is clear **and** the
retained failing checkpoint still contains the earlier unexpected error. This
prevents a final-state snapshot from erasing the reproduction evidence.

The helper now checks the supplied error attribute on all success paths and
rejects exceptions during controlled successful responses. Injected failure
responses remain distinguishable from unexpected success-path exceptions.
Failure details are emitted only for failing checkpoints; no extra sequence or
model invocation is added.

## Practical interface boundary

The skill now describes the helper's real contract: zero-argument constructor,
injected async fetch, directly stored payload, and optional JSON-serializable
error state with falsy/clear and truthy/displayed semantics. Existing adequate
project tests take precedence. Other interfaces require project-specific checks,
not production-source changes to accommodate this helper. The cooperative timeout
is explicitly not a hard deadline for blocking imports or synchronous callbacks.

These routing instructions have not yet been evaluated in fresh model sessions
against incompatible project interfaces. Documentation alone does not prove
correct selection in actual use.

## Verification and cost limits

```sh
python3 -B -m unittest discover -s tests -p test_mother_in_law_sequence_probe.py
python3 -B -m unittest discover -s tests
python3 -B scripts/validate.py
python3 -B scripts/sync_featured_benchmark.py --check
```

Full local regression: **270 tests passed in 42.978 seconds**. Skill schema,
repository links/catalog and featured-language/chart synchronization passed.

Author replay on the prior recovery fixtures preserves their outcomes and four
sequences per invocation. Compact JSON case-array size increases from 718 to 756
bytes on the clean fixture and 736 to 924 bytes on the sticky-error fixture.
The added bytes describe error state and actionable failure evidence; they are
not token counts. No fresh model tokens or end-to-end time were measured, so no
new efficiency percentage is claimed. Existing featured charts are unchanged.

The broad objective remains open: practical project integration, automatic
selection and reliable resource improvement across all eight skills still need
stronger evidence than these local helper regressions.
