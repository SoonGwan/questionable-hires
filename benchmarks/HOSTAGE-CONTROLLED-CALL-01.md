# Hostage controlled-call candidate

The [whole-bundle checkpoint](BUNDLE-CONTRACT-06-REVIEW.md#pending-form--skill)
retains repeated custom asyncio entry/release gates in generated save tests.
The skill costs more despite fewer tests in that pair. This does not attribute
cost causally to gates, but motivates a reusable mechanism instead of more
generic scope advice.

New optional `assets/controlled_call.py` is copied into permitted project test
support only when no equivalent exists. It accepts zero/positional/keyword
arguments, exposes actual entry handles, records call references/counts and
delivers exact result/exception objects. Each call owns a distinct future. Tests
still own application tasks, pending-state/duplicate/instance/recovery assertions,
cleanup and bounded waits. It does not implement the app or assert its policy.

Seven native tests pass in 0.229s: no-argument/value identity, repeated argument
reverse completion, exception identity/recovery, isolated cancellation and invalid
late completion, entry-timeout recovery/invalid bounds, standalone copied execution,
and the retained real Form implementation. The Form control checks pending state,
duplicate suppression, value/error propagation and cancellation cleanup through
actual submit. The same probe rejects a missing duplicate guard with the intended
`duplicate callback invoked while original pending` AssertionError. The retained
source is unchanged. Fifteen installer tests pass in 1.917s; skill validation passes.
Full local suite: **452 tests pass in 71.363s**, no failures/skips. Repository
links and featured-language synchronization checks pass; this is not hosted CI.

This is author native evidence, not a model benchmark or a claim that all required
application contracts are covered. The asset's positive path alone cannot prove
instance isolation or synchronous callback failure: the task's tests must exercise
those when required. Arguments are references, not immutable deep snapshots.
No browser/network/thread evidence; async waits cannot stop blocking or
cancellation-resistant application code. Use a process bound where needed.

New reference loading, copying and test adaptation also cost work. Model adoption,
token/time impact and transfer beyond the exposed save example are unmeasured.
Historical and featured results remain unchanged. This capability is a candidate
for the all-eight objective, not a substitute for proving that objective.
