# URL masking audit: precheck adopted, token cost nearly doubles

[Protocol](../../HTTPX-URL-REPR-01-PROTOCOL.md), [run](run.json),
[metadata](summary.json), [author integrity checks](author-integrity.json).
Launch `dde9397`; Con Artist resources `1a75a03`; full HTTPX checkout
`26d48e0634e6ee9cdc0533996db289ce4b430177`. New author-selected task on real
upstream code, not a maintainer ticket or an independent/unexposed project.
Two fresh serial Astra medium sessions, skill first, n=1, 360-second caps.
Both complete; no retries, exclusions, account stops, resource edits or author
test workloads during timing.

| Arm | Input + output tokens | Process seconds | Shell calls | Required native outcomes |
| --- | ---: | ---: | ---: | --- |
| Baseline | 122,689 | 75.869 | 4 | Correct 91 pass; mutant 1 assertion failure / 90 pass |
| Con Artist | 243,250 | 64.985 | 6 | Correct 91 pass; mutant 1 assertion failure / 90 pass |

**+98.27% tokens / −14.35% time.** Cached input is included once in input;
reasoning output is not added again. This fails the similar/lower-token objective.
Shared host/cache, n=1, order and different extra work prevent causal claims.
Faster time is not overall acceptance and does not erase earlier adverse results.

## Actual work

[Skill commands](url-repr-password--skill--1/commands.json) read the entry and two
references (15,155 output characters), then run the collector with a whole-test-file
`--full` selector plus known auth-test/repr definitions. Collector output is
46,431 characters; the numbered test_url.py source alone is 30,696. It subsequently
reads test_url.py lines 166–455 again, relevant imports/setup/parser code and helper
implementation sections. These are observed reads, not a causal token attribution.

The final audit uses **precheck** and no stronger probe: two copied pytest
processes, each verifying imported URL/parser identity, implementation paths,
code filenames and hashes. Controls and additional password-case field assertions
run in those same prechecks. No extra binding module, separate import-only process,
temporary script or stronger-test implementation is created. Helper copy cleanup
is checked afterward. The precheck establishes current bindings, not a test-call
trace or immunity to subsequent fixture rebinding.

[Baseline commands](url-repr-password--baseline--1/commands.json) use targeted
source searches/reads and create a Python wrapper inline. Two project-local
copies run two native pytest processes with copied URL imports/source/hash and
normal controls in each. A Python audit hook rejects connect/bind/getaddrinfo
events; it is extra verification, not a full network sandbox. The wrapper checks
original-file hashes and removes copies in finally. Its native children do not
have their own timeout (the outer model cell still has its limit).

Both run the exact requested tests and pytest options without warning-policy or
plugin-autoload changes. Both omit only password masking in disposable copies
(skill uses pass; baseline uses a self-assignment). Existing test_auth_hidden_url
fails at line 307 with actual expected `[secure]` versus observed example-password;
all 90 selected URL tests still pass. Username-only and no-userinfo controls pass
on both implementations. No new production vulnerability is claimed: the harmful
change is an isolated deliberate fault and real upstream behavior is protected.
Both answers scope coverage to that fault rather than all credential edge cases.

## Evidence preservation and limits

Post-run author comparison verifies all **125 original files** in both final
snapshots against pinned upstream bytes and permission bits, with exact final
file inventory. Both agent diffs are empty; no new harness/report remains. Skill
resource inventories are unchanged; terminal usage and original/redacted events
reconcile. Captures have no invalid/empty-output/rejected-patch flags, and decisive
native outcomes/controls are present. Diagnostics alone do not prove complete
capture of every token the agent saw.

This export retains complete event/command/answer logs and six selected upstream
files per cell, including LICENSE.md; project-export.json identifies the excerpt
selection. It is **not a standalone full project**: recover remaining source from
the pinned upstream revision. Full local snapshots remain in the private run.
Workspace/home paths and the supplied interpreter path are redacted; `<PYTHON>`
means the preinstalled interpreter recorded by the protocol, not a literal command.
Source hashes identify original unredacted logs. No measured event is repaired.

## Candidate change after measurement

The new precheck was adopted but did not prevent source inspection or large,
partially repeated context reads. Con Artist entry/reference now distinguishes
the suite's **execution scope** from the assertion bodies needed for this audit:
prefer relevant known definitions/targeted search, retaining whole-file reading
when justified and all required test execution. Helper behavior/selection policy
remain unchanged. This follows skill-creator's decision-changing guidance principle;
it does not ban necessary source review or claim a measured saving for the change.
Do not rerun this exposed task for a preferred score. Separate transfer and the
all-eight objective remain open; featured graphs and localized claims are unchanged.

Post-run checks: context suite **22 pass (0.362s)**, evidence-export suite **4
pass (0.019s)**, full repository **378 pass (52.503s)**. Skill/catalog, local
links, featured consistency and privacy-pattern checks pass. These author checks
do not establish model transfer of the later reading-scope change.
