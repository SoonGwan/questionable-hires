# First local rendered-DOM interaction check

The synthetic [search fixture](browser/search-order.html) now runs in an actual
headless Chrome process, with a fresh temporary profile per variant. No model
session, application backend or external service is part of this check.

Observed sequence: dispatch old input, dispatch new input, complete new response,
complete old response, then complete a normal request. With the guard disabled,
the visible result changes from `new result` to `old result`. With the guard
enabled it remains `new result`. Both variants display `normal result` afterward,
submit exactly old/new/normal, and preserve DOM focus on the input.

```sh
python3 -B benchmarks/browser/check_search.py --browser '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

Use the actual path to an installed compatible Chrome. The runner is currently
POSIX-only and is not part of the default dependency-free unit suite. It uses no
Playwright dependency or existing browser profile. JSON reports actual DOM
observations; the deliberately broken variant must fail its behavioral predicate
and the guarded variant must pass for the runner to succeed.

The first attempt timed out during the guarded browser launch. It is incomplete,
not a behavioral failure or pass. After adding Chrome's dump timeout, disabling
unneeded startup services, and terminating the owned process group on the outer
deadline, both variants completed with the observations above. A post-run process
inspection found no remaining dedicated profile processes. This does not prove
which startup flag resolved the delay or guarantee every future launch.

Limits: input events are dispatched by fixture JavaScript, not physical keyboard
input or browser input automation. Focus is inspected through `activeElement`;
no screenshot, assistive-technology check, navigation/recovery test or network
request cancellation is covered. This supplies actual DOM-layer evidence for one
sequence, not Mother-in-law model quality or completion of the browser release
gate. No skill instructions, automatic routing or benchmark scores changed.

## Subsequent lifecycle regression

The runner now terminates its owned process group on cancellation as well as
timeout, tolerates an already-exited group, and bounds cleanup pipe draining and
root-process waiting. Two browser-free mechanics tests exercise those paths;
they are mocks of process lifecycle, not evidence of rendered behavior.

A subsequent actual Chrome run again timed out in `guard=on`, despite the startup
flags above. It exited with an explicit incomplete error, and post-run process
inspection found no dedicated-profile processes. The earlier successful pair is
preserved but does not establish reliable startup/termination. Investigate this
runtime instability before adding browser checks to required CI or claiming the
browser release gate is satisfied. No favorable retry followed in that work cycle.

A later diagnostic run instrumented process completion/output sizes to distinguish
missing output from possible shutdown delay. Both variants exited 0 on that run:
stdout 2,013/2,011 characters and stderr 2,125 characters each, with the same DOM
observations as the earlier success. The timeout did not recur, so its cause
remains unknown. This run is diagnostic, not a replacement for either failure.
Runner `074c2e4` now reports captured stdout/stderr byte counts on future timeouts
without including raw browser logs in the diagnostic message. Three mechanics
tests pass, including UTF-8 byte counting and suppression of raw diagnostic text.

Runner `9e40178` preserves completed variant observations when a later browser
times out, exits nonzero, or returns no valid JSON receipt. The CLI emits
`complete: false`, an error and `completed_variants`, with exit status 1. It does
not synthesize a missing variant or reinterpret an incomplete run as success.
Successful runs retain the existing two-observation list format. Browser stderr
is no longer included in nonzero-exit messages. Four mechanics tests pass,
including a completed broken variant followed by a guarded-variant timeout.
This change was unit-tested with controlled process results, not credited as a
new real-browser behavioral pass.

The next actual invocation of that runner completed both variants with the same
expected stale/guarded DOM results, normal-path result and focus preservation.
No timeout diagnostics were exercised in that invocation, so the intermittent
cause remains unresolved. Do not keep repeating the same self-dispatched input
fixture to claim readiness; the next coverage expansion should use actual browser
input automation and retain the current fixture as a lower-layer regression.
