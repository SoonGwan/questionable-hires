# Browser-generated input: local search-order check

Executed with Node 24.16.0, playwright-core 1.63.0 and installed Chrome
152.0.7977.83. The optional dependency is pinned with an npm lockfile under
`benchmarks/browser`; installation used `--ignore-scripts`, with no downloaded
browser, host-profile changes or dependencies added to the shipped skills.

```sh
npm ci --prefix benchmarks/browser --ignore-scripts --no-audit --no-fund
node benchmarks/browser/input-check.mjs '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

Supply an installed compatible Chrome path. One owned headless browser serves two
separate contexts, closed after their checks. HTTP(S) page requests are blocked;
the fixture loads from a local file. Browser launch is limited to 15 seconds and
page actions to five seconds; context/browser close currently has no separate
outer process deadline. Do not call this a fully bounded production QA runner.

The fixture's new manual mode does not dispatch its own input sequence. Playwright
fills the real input element; each captured input event has `isTrusted: true`.
The exposed fixture API only completes controlled response promises. Both variants
receive exactly old/new/normal inputs. New response first displays `new result`;
old response afterward displays `old result` without the guard and leaves
`new result` with it. Normal completion displays `normal result`, focus remains
on the input, and neither context reports page errors. The runner exits 0 with
`complete: true` and the full observations.

This advances beyond self-dispatched DOM events, but uses browser automation,
not physical keyboard input. It does not yet cover key-by-key typing, navigation,
error recovery, assistive technology, real network cancellation or model-driven
QA. The original dump-DOM runner and its intermittent timeouts remain separate
evidence; this single success does not diagnose those timeouts or establish broad
browser stability. No model benchmark or skill modification occurred.

Implementation follows the [Playwright browser launch API](https://playwright.dev/docs/api/class-browsertype#browser-type-launch).
That API cautions that arbitrary installed browser versions are not guaranteed
compatible. This report establishes only the versions actually executed above.

## Keyboard-path expansion

The runner subsequently executes four independent contexts: fill/keyboard ×
unguarded/guarded. Keyboard mode clicks the input, uses `ControlOrMeta+A` to
select its contents, and presses `o`, then replaces it with `n`, then `r`.
Those single-character queries stand for old/new/normal requests; the controlled
response sequence is unchanged. The fixture records keydown events separately
from submitted input events.

On the same Chrome version, the actual output contains Meta, A and each requested
character with `trusted: true`; submitted values are exactly o/n/r, also trusted.
All four contexts produce the expected broken/guarded stale-response difference,
normal result and preserved focus, with no page errors. Fill mode produces no
recorded keydown events, which is why its earlier evidence was not a keyboard
test. The command exits 0 with four observations. No physical keyboard, IME,
multi-character composition, navigation or error recovery is claimed. The missing
outer close deadline and original dump-DOM instability remain open.

## Controlled error recovery

The next expansion retains all four contexts and their stale-response checks.
After normal completion, each context submits another query, rejects its
controlled response promise, then submits a replacement query and completes it.
Chrome 152.0.7977.83 executed all four paths successfully (exit 0,
`complete: true`). Assertions check the exact error message, retained input and
focus after failure, error clearing when retry starts, `recovered result` after
success, cleared error and focus after success, all five trusted submitted
values, and no uncaught page errors. Recovery details are included in each
observation rather than inferred from command completion.

This is synthetic promise rejection and retry, not a real backend outage or
network cancellation. Both guarded and deliberately unguarded variants recover;
this addition does not measure a skill advantage. Navigation, IME, model-driven
QA, a separate outer close deadline and the original dump-DOM timeout diagnosis
remain outside this evidence.

## Workflow deadline

The command now defaults to a 60,000 ms watchdog covering launch, connection,
interaction and cleanup. An optional third argument changes it (1–300,000 ms).
It launches an owned browser server bound to `127.0.0.1`, connects locally, and
emits success only after both connection and server close finish. On deadline it
writes `complete: false` and the completed observations to stderr, calls the
server's force-kill operation, and exits 1. A further five-second timer limits
waiting for that kill operation. This follows the official
[BrowserServer lifecycle API](https://playwright.dev/docs/api/class-browserserver).

Actual Chrome 152.0.7977.83 execution with the default deadline passed all four
contexts and exited 0. Running the same command with `1000` as the third argument
timed out after two completed fill contexts, preserved those observations and
exited 1 without a success receipt. A subsequent process listing found no runner
or Playwright temporary-profile browser processes. This is a deliberately short
deadline test, not an interaction defect or a model benchmark.

The watchdog is an in-process Node timer, not an independent OS supervisor: a
blocked event loop can delay it. Force-kill cleanup failure may leave temporary
files; no fault-injected hung-close test or cross-platform termination guarantee
is claimed. The older dump-DOM timeout diagnosis is still unresolved.

## Same-document view disposal

The fixture now includes Search/Settings buttons. Leaving Search invalidates
pending request ownership, hides the search control, clears the old error and
focuses the Settings heading. Returning restores the search control and focus.
Promises deliberately continue running: this tests stale UI writes, not transport
cancellation. The unguarded variant ignores ownership and remains a negative control.

Chrome 152.0.7977.83 completed all four fill/keyboard × guarded/unguarded contexts
with `complete: true` and exit 0. After leaving with a pending request, late success
overwrites Settings only without the guard; a separate late failure adds the
search error only without the guard. Both variants successfully search after
returning, and heading/input focus assertions pass. Existing request-order and
error-retry checks remain in the same execution. No uncaught page errors occurred.

This is same-document synthetic view switching, not URL routing, full-document
navigation, back/forward cache, component destruction or a model-driven QA session.
The skill itself is unchanged; no token/time or comparative model claim follows.
