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
