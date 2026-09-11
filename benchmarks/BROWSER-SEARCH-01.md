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
browser release gate is satisfied. No favorable retry followed this observation.
