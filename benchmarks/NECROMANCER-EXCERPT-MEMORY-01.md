# Lower excerpt-parser allocation, unchanged evidence

Candidate a16e57d changes selected_patch_excerpt, not Git subprocess collection or
skill selection. The parser previously stored a formatted numbered string for every
patch row, although only selected rows and three neighbors could be returned.
It now retains selected windows plus a three-row lookbehind and formats only rows
actually rendered. Full patch syntax/count validation still runs to completion.
The original splitlines semantics, target-first budget and omission markers remain.

Author micro-measurement: prebuilt 100,000-context-row single-file unified diff,
select new line 50,000, default 8,000-character excerpt budget. Input allocation
occurs before tracemalloc starts. Old function from dbb0c28 versus candidate:

| Function | Peak traced additional allocation | Median seconds, five untraced calls |
| --- | ---: | ---: |
| old | 17,988,734 bytes | 0.085281 |
| candidate | 8,805,575 bytes | 0.083706 |

Both return exactly the same 293-character excerpt. Measured additional peak
allocation is about 51% lower for this input. Timing is approximately equal;
five local calls without randomized order do not establish a speed advantage.
This is function allocation, not process RSS, end-to-end model tokens or session
time. Full Git output, raw patch text and split line strings are still retained;
there is no whole-process memory cap or bounded Git capture claim.

A retained behavioral test selects distant beginning/middle/end windows in 20,000
rows and checks correct row numbers, neighboring evidence, omission markers and
budget. Appending malformed unselected content still rejects the excerpt. All 19
history tests and 162 repository tests pass (18.471 seconds for the full suite).

Additional author comparison uses seed 20260911, 100 mixed add/delete/context
patches, valid and malformed tails, and budgets 3/80/400/8000. All 800 old/new
results agree. This is a bounded regression corpus, not proof for all possible Git
output. The selected-line/parser fallback contract, entrypoint and UI are unchanged.
No model benchmark was rerun merely to turn this local memory gain into a broader
performance claim. Whole-bundle objective remains unmet.
