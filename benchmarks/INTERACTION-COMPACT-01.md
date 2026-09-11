# Compact interaction instructions: runnable handoff, mixed cost

Revision `d1be060`, execution HEAD `4af2fcc`. One fresh Astra-medium skill session
on the existing broken-search case; no retry, baseline or full-team screen.
Raw evidence: ignored `local-runs/interaction-compact-01`.

Current **68,328 tokens / 54.530 seconds**, versus screen 05's **84,310 / 46.709**:
19.0% fewer tokens, 16.7% more time. These single separated samples do not establish
causality or a combined efficiency win. Shorter instructions are not themselves
performance evidence.

The generated 80-line `test_search_qa.py` contains both deterministic completion
orders and its own five-second parent subprocess deadline, including cleanup.
Its final handoff `python3 test_search_qa.py` preserves that deadline without another
skill or an omitted shell wrapper. Normal order expects the latest result; reverse
order reveals the older response overwriting it. Assertions exercise actual Search;
browser rendering remains explicitly untested. Original production files remain intact.

## Capture limitation and separate verification

The original model command exits 1 but its aggregated output is empty, flagged by
capture diagnostics. The final model answer reports one passing and one failing
test; the captured exit alone does **not** establish that breakdown or distinguish
an assertion failure from setup failure. Do not present its missing log as observed
model evidence.

Author replay of the exact retained file after the model finishes confirms normal
order passes and reverse order fails with the expected stale-result assertion;
exit 1, two tests, exactly one failure. This is separate artifact evidence, not a
retroactive reconstruction of the missing original output.

An additional author fault check runs the retained parent entrypoint while
intercepting only its child-launch arguments to inject cancellation-resistant,
no-dispatch Search behavior in memory. The actual parent's five-second timeout
and error handler return exit 2 with INCOMPLETE before the author's eight-second
safety deadline. No original file is edited. This checks handoff containment, not
the original stale-result task or a model-run adversarial test.

Both fixture originals and both installed skill resources match committed inputs
and `d1be060`; no rejected patch. Direct unittest discovery or `--worker` bypasses
the parent's deadline; the documented script entrypoint is the supported bounded
reproduction. No claim that every invocation is self-bounding.

Disposition: retained artifact demonstrates correct task behavior and executable
deadline handoff, but original runtime detail is partially unobservable. Preserve
the adverse time result and capture caveat. The current compact candidate has not
received another protected-search check or whole-team gate.
