---
name: exorcist
description: Diagnose an uncertain bug by designing experiments that distinguish competing causes, especially speculative cache, timing, environment, or concurrency explanations.
---

# Exorcist

> You keep saying cache. Let's test that belief.

## Find the decision-changing observation

Start at the reported failure using supplied paths or the repository file list. Reuse existing reproduction evidence; trace only until plausible causes diverge. Don't manufacture hypotheses for an established mechanism.

Observe that boundary in the actual implementation: submission versus persistence, dispatch versus completion, configuration versus effective state. Prefer existing observations or a recording dependency. Another layer recording the same value adds nothing unless its provenance is unresolved. A rewritten simulation or repeated success flag cannot establish an unobserved effect.

Choose the runner before inspecting setup: use existing tests when they exercise the distinction, otherwise one small probe with comparable inputs and controlled timing. Inspect fixtures/configuration if that path uses them or they could explain the symptom. Retain normal controls; repeat only for unresolved intermittency or a required check.

Before another experiment, ask which possible result changes the diagnosis or next action. If none, stop. A symptom without a suspected dependency shows that dependency is unnecessary for this reproduction, not every production incident. Explain why the existing safeguard does or doesn't address the observed mechanism.

## Match containment to the exercised path

Run a bounded local computation with the chosen interpreter or existing test runner. The optional helper is not the default probe command: use it for an identified hang risk that the runner's existing process deadline does not contain. Synchronous code can also block; choose from the actual operations, not the presence of `async` alone.

For asynchronous probes, bound signals that may never arrive and clean up owned tasks. Asyncio timeouts can wait indefinitely for suppressed cancellation. When an additional process deadline is needed, the installed POSIX helper supplies one (replace paths/interpreter):

```sh
python3 /path/to/exorcist/scripts/run_probe.py --timeout 10 -- python3 -B experiments/probe.py
```

Trusted local foreground commands only: this kills remaining process-group members even after normal completion; it is not a sandbox. JSON retains child status, timeout and bounded output. Timeout or truncated decisive output means incomplete evidence, not causal proof. See [runner details](references/bounded-probe.md) for exit mapping, limits or adaptation; routine invocation doesn't require source inspection.

## Finish at the evidence boundary

Keep diagnostic output focused on decisive ordered observations, normal controls,
native failures and counts. Inspect needed source separately; a large source dump
in the experiment output can crowd out the observations. Use captured output when
it fits. For longer or requested traces, write one project-local record and read
the relevant segments; don't duplicate the entire record on stdout. Confirm the
claimed events are actually visible before reporting them. Missing segments stay
unverified; recover retained records before considering a safe rerun. Preserve
required artifacts and remove disposable records only after review. Keep the
reproduction rerunnable.

Report the supported mechanism, decisive command/result, safeguard and uncertainty. Name the missing observation if blocked, rather than expanding simulations. Link the reproduction instead of repeating it. A restart alone isn't causal proof; preserve evidence and user state before an authorized reset.

Diagnosis leaves production code unchanged. A requested fix stays scoped and reruns the original reproduction plus relevant checks. Preserve user changes and explicit requirements. Keep humor optional.
