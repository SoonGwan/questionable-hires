# Packaging transfer: correct decision, no overall efficiency win

[Protocol](NECROMANCER-PACKAGING-REVIEW-PROTOCOL.md) and runner frozen at `6e2f582`.
Actual packaging source is `436e409`; installed candidate is `0143ef2`, predecessor
`8844685`. Three fresh serial Astra medium sessions ran candidate, baseline,
predecessor with 240-second deadlines. All completed without retries, exclusions
or timeouts. Local originals: `local-runs/necromancer-packaging-review-01/`.

| Condition | Input + output tokens | Seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| No installed skill | 90,607 | 54.732 | 4 |
| Predecessor | 94,479 | 62.285 | 7 |
| Candidate | 99,038 | 59.246 | 4 |

Candidate versus predecessor: +4.83% tokens, −4.88% time. Versus no-skill:
+9.31% tokens, +8.25% time. Input/output/cache: baseline 89,289/1,318/71,424;
predecessor 93,021/1,458/79,744; candidate 97,635/1,403/85,120. Cache is already
included in input, and reasoning output is not added again. No dollar estimate.

All three inspect actual build code and tests, pass the five unchanged tests,
unwrap the copying handler in memory and rerun the same tests. Three subtests
fail because partial output remains after OSError, RuntimeError and
KeyboardInterrupt. Successful bundle behavior, existing-destination preservation
and original-error checks remain covered by the suite. All recommend retaining
cleanup while keeping exclusive destination creation outside the handler.

Candidate additionally injects a late catalog-copy failure and observes leftover
output, preserved exception identity and failed retry. Baseline executes this
probe against both original and removed-handler implementations. Predecessor
instead constructs an owned minimal source fixture with a missing catalog,
observes failure, restores the catalog and compares successful/blocked retry.
These are useful but unequal experiments. Candidate and predecessor have local
Xcode cache/filesystem warning messages during original tests; tests still pass.
This shared-host variation is not isolated from the timing comparison.

Candidate accepts the README's explicit missing-upstream-history limit and does
not collect blame/log. Predecessor examines snapshot blame/log, correctly labels
origin unknown and does not invent an introducing commit. No history is fetched.
Avoided history is observed, but fewer calls do not produce lower total tokens.
Candidate's broad search also emits snippets of packaged skill references. All
conditions contain those skill files as real package data, and the bundle test
executes the packaged Receipt helper. Thus baseline means no installed/invoked
skill, **not an environment containing no skill code or text**. The candidate
trace shows no separate invocation of those searched skills; exposure remains a
confound, not proof that the text could have had no influence.

Baseline has one discovery command exit 1 after an AGENTS search finds nothing.
Predecessor's similar fail-fast chain exits before source reads, which it then
performs separately. Neither is a failed behavior test. Captured mutation outputs
and summaries were inspected rather than inferred from final shell exits.
Some captured output starts mid-stream; five-test totals and decisive mutation
failures are present, but clean capture flags do not prove every output byte was
retained. Predecessor prints its outcomes rather than asserting all of them.

All 102 original file instances match fixture bytes and all diffs are empty.
Eight installed resource instances match frozen hashes and before/after manifests;
no capture diagnostic flags were reported. No author replay is model evidence.
No project implementation changes, host installation or publication occurred.

The candidate preserves necessary verification and skips unavailable history,
but this transfer does not meet the token/time objective. Retain it alongside
the favorable [dictionary decision-gate screen](NECROMANCER-DECISION-GATE-01.md).
One exposed own-repository snapshot, one repeat, shared cache, packaged skill
exposure and unequal work prevent a general efficiency claim. Do not rerun the
same case merely to select a better score; further improvements need evidence
of a different avoidable workflow cost.
