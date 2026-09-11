# Two-module Receipt transfer: faster, more tokens

[Protocol](RECEIPT-ASSEMBLY-PROTOCOL.md), runner `e2006ca`, fixture `208047e`,
Receipt `aac3a92`. Fresh serial Astra medium, skill then baseline, one repeat,
240-second limits. Both completed without retries, exclusions or timeouts.
Local originals and hashes: `local-runs/receipt-assembly-01/`.

| Arm | Input + output tokens | Seconds | Shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 86,588 | 61.676 | 4 |
| Receipt | 109,124 | 42.496 | 5 |

Receipt: +26.03% tokens / −31.10% time. Input/output/cache: baseline
85,010/1,578/75,264; skill 108,184/940/95,104. Cache is included in input once;
reasoning output is not added again. No dollar estimate or attribution to the
recent permission-detection change.

Both run the current two-test suite against before
`8049ad168aa16233dbee11dcb04c9f9270551e16` and after
`171834cfcdab209e892292434872e617123bc428`, holding current tests, settings and
samples fixed. Both export all four assembly files; service and package-init are
identical across revisions, while reader and writer change together. Before
fails both numeric ordering and empty output; after passes both. Actual runner
outputs and loaded-copy evidence are present.

Receipt uses its helper without reading its implementation, verifying all four
package imports in each test process and reporting revisions, fixed hashes and
separate nontruncated outputs. It adds a final status/temporary-directory check.
Baseline builds a custom harness, uses verbose import traces for the actual
runner, executes separate output/import probes, prints matching loaded/expected
Git blob hashes, and hashes originals including .git. These additional checks
and different reporting are unequal work despite equal requested outcomes.

All 20 original file instances match fixture bytes, final diffs are empty, and
four installed skill resources match frozen hashes and before/after inventories.
Commands stay project-scoped. Capture diagnostics have no flags; decisive outputs
were inspected rather than treating flags as proof of complete capture. No author
replay is credited as model execution, and no installation/publication occurred.

The combined token/time objective is not met. Retain this beside the favorable
[parser pair](RECEIPT-EQUAL-REQUIREMENTS-01.md), not as a pooled headline gain.
One exposed authored task, one repeat, shared host/cache and unequal work prevent
broad or causal claims. Do not repeat unchanged cells for favorable scores.
