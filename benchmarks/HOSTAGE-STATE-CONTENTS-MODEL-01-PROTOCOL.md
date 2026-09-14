# State-content instruction: fresh adoption screen

Frozen resource `691f896`. Unchanged exposed preview task source
`hostage-javascript-preview-cases.json`, SHA-256
`fd9d98e8557845c3f25aff22f7576c850323f7c0a815528427f7c486338f8c5c`.
The [candidate correction](HOSTAGE-STATE-CONTENTS-01.md) has local validation,
not model adoption evidence. This is an author-designed development screen.

Run **one fresh explicit-skill session**, Astra medium, seed 20260911, jobs 1,
timeout 240 seconds. Do not inject the previous solution, test repair or detected
counterexample into the model task. No baseline cell this time: this is a narrow
behavioral adoption gate, not a new efficiency comparison or proof that the
instruction caused a change. Report absolute costs only. No favorable retry.

Preflight: 476 local tests passed in 65.156s, no skips/failures; skill/repository/
featured-language checks passed. Native author-copy repair accepts correct
replacement and correct in-place state updates and rejects stale content writes;
the frozen original model tests still reproduce the missed fault. Neither author
test suite nor reference owner is provided to the new model session.

Keep all original fixture obligations and existing tests unchanged. Preserve
attempts, timeout/unknown usage, initial test failures, capture gaps and scope
exceptions. No task/resource edits or author test workloads during model timing.

After timing, review actual owner behavior and retained native assertions for all
original obligations. In particular, inspect field snapshots before stale work,
payload/reason identity, and unchanged contents after completion, rather than
accepting container identity or test-count growth as proof. Reconcile raw events,
usage, frozen resources, exact reviewed inventory and original test preservation.

In separate disposable copies, run retained tests unchanged against final and
original code, guarded in-place success/error updates, and unguarded in-place
stale success/error. Keep native actual/expected output and per-process bounds.
Accepting valid mutable updates matters: do not impose immutable architecture
that the project never requested. Preserve all replay attempts and distinguish
them from original model evidence. Further obvious obligation defects found in
review must be disclosed, not ignored because this targeted gate passed.

No historical score, featured chart, EN/KO metric or overall-efficiency claim is
updated from this skill-only screen. Update current candidate status with actual
adoption outcome and limitations after review.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-javascript-preview-cases.json --output benchmarks/local-runs/hostage-state-contents-model-01 --arms skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```
