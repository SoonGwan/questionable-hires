# Receipt lossless output formatting

Author interface arithmetic, not a model benchmark. Starting repository `b2bac2a`.
The retained source-layout model run used resource `53b2765`; its raw outputs and
measured costs remain unchanged.

Read the comparison command's first JSON object in
`results/receipt-src-model-01/src-settings-fix--skill--1/commands.json` using
`json.JSONDecoder().raw_decode`. Serialize that same object with either
`json.dumps(value, indent=2)` or `json.dumps(value, separators=(',', ':'))`, adding
one trailing newline to each. Parsed objects are identical. Pretty output is
5,969 characters; compact output is 5,447: **522 characters / 8.75% fewer**.
These counts use the retained redacted payload, not the full shell output.

The helper now defaults to compact JSON and offers `--pretty` for the old human
layout. It removes only structural whitespace, not any fields, original hashes,
cleanup status, assertion details or whitespace inside captured test strings.
No summaries or token-based truncation are introduced. Runner output limits and
exit semantics are unchanged; one invocation still performs one comparison.

A native before-failure/after-pass fixture supplies the actual result object for
both CLI rendering modes. Tests parse and compare all values, including exact
captured failure strings, and verify one comparison call per rendering. The real
incomplete-import CLI test also requires a single JSON line and still exits 2.
Final full regression: 414 tests passed in 67.848 seconds; skill validation,
metadata/link, featured synchronization and whitespace checks passed.

Character reduction is not model-token or whole-session savings. The model's
reading/adoption behavior and new resource's net cost are unmeasured. Preserve
the original source-layout result and all-eight gate; no chart changes follow.
