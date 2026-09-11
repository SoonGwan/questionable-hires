# Exorcist: verified termination, increased observed cost

Screen 05's retained diagnosis probe waits forever if Search returns without
dispatching. Author verification loaded the actual retained probe and replaced
`Search.run` in memory with a no-dispatch coroutine. Its original scenario exceeded
the author's two-second subprocess deadline. Wrapping that scenario in a 0.1-second
asyncio deadline instead produced TimeoutError. Neither operation edited the
original project or establishes the cause of a production incident.

Revision `8ec7a57` adds one conditional instruction paragraph: bound implementation-
dependent async waits, clean up owned tasks, use a process deadline if cancellation
can stall, and treat timeout as incomplete evidence rather than causal proof.
Character, scope and ordinary synchronous diagnosis remain unchanged.

One fresh Astra-medium skill session on `search-diagnosis`, no retry, baseline
rerun or full-team screen. Raw evidence: ignored `local-runs/exorcist-bounded-01`.

| Sample | Input including cache + output tokens | Seconds |
| --- | ---: | ---: |
| Screen 05 | 68,288 | 42.015 |
| Bounded follow-up | 86,090 | 52.371 |

Tokens increase **26.1%**, time **24.6%**. This is a termination improvement with
an observed cost increase, not the requested efficiency win. One separated sample
does not isolate the instruction's causal cost.

The model still runs actual Search and transport with cache-free recorded requests
in both completion orders and confirms the no-cache headers. Its retained
`experiments/search_race.py` uses one-second signal/task waits, a four-second outer
async timeout, and a five-second SIGALRM process deadline. Cleanup's gather is not
individually bounded, but the process deadline covers cancellation stalls on this
POSIX runtime. This artifact is not a cross-platform general-purpose runner.

After the model completed, author checks executed that exact retained script
through its main entrypoint, under a separate eight-second safety deadline:

| In-memory implementation | Actual outcome |
| --- | --- |
| Original Search | Exit 0, both recorded response-order outcomes reproduced |
| Returns without dispatch | Exit 1 with TimeoutError, 1.081 seconds |
| Never dispatches and swallows cancellation | SIGALRM termination (return code -14), 5.084 seconds |

The latter two did not need the author's eight-second deadline. Their failure is
incomplete evidence, not a reproduced stale overwrite. These are author fault
checks, not additional model sessions or claims the model itself tested the faults.

Both original project files and both installed Exorcist resources match fixture
inputs and `8ec7a57` blobs. Original captured experiment output contains both orders;
no patch rejection, timeout or capture diagnostic is reported. The model correctly
limits its causal conclusion and does not implement a production fix.

Retain the narrow termination instruction while acknowledging cost. Do not rerun
this unchanged task for a favorable number. Broader efficiency remains unproven;
the combined screen 05 predates this instruction change.
