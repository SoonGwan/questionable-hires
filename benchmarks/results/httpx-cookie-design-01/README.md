# Cookie design transfer: correct review, mixed resource cost

[Frozen protocol](../../HTTPX-COOKIE-DESIGN-01-PROTOCOL.md), launch `0d4ed35`,
Landlord `e267919`, pinned full HTTPX checkout. Two fresh serial Astra medium
cells, skill then baseline, no retries/exclusions. No resource/fixture edits or
author test workloads during model timing. Authored real-source task, not an
organic ticket or blind holdout; shared host/cache and one repeat per arm.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| Baseline | 146,708 | 98.197 | 7 |
| Skill | 164,827 | 81.966 | 8 |
| Skill change | +12.35% | −16.53% | |

Cached input counts once. Both recommend retaining Cookies/CookieJar, identify
actual request/response/sync/async/redirect consumers, cite public scope contracts,
explain the policy that a replacement must retain, and recommend existing dict
input normalization rather than name-only internal storage. Both execute scoped
duplicate and single-cookie controls and preserve all original files.

Baseline runs 15 cookie-selected tests (0.09s), then retains one project-local
probe exercising request selection, copy/deletion, sync and async response
persistence, Secure filtering and normal controls. Its projection outputs expose
scope loss but are observations rather than asserted projection expectations.
Skill runs all 45 tests in those three modules (0.14s), then an inline probe with
four same-name records across two hosts/two paths, scoped deletion, response and
sync client persistence, single-cookie control, and explicit last-wins projection
assertions including an unrelated host. It additionally verifies Secure metadata
loss on conversion and an expired cookie's exclusion, but does not execute the
baseline's async probe. Neither implements the proposed replacement. The existing
dict-input conversion demonstrates information loss, not every possible design.

Native outputs and assertions support both reviews; work is not identical, so
the wall-time difference is not a causal efficiency win. Baseline's retained
`.cookie-review/probe.py` is within the requested project-local diagnostic scope;
deletion was not required. Skill creates no diagnostic file, so its selected
export correctly lists that baseline-only path as missing. No original edit,
out-of-scope command or capture diagnostic flag was found. Empty flags alone do
not establish capture completeness.

All 125 original files per arm match the pinned source. Both frozen skill files
match installed before/after inventories. Terminal usage matches metadata and
redacted events match original captures. [Integrity audit](integrity-review.json)
is final-snapshot evidence, not proof against transient edits or outside writes.
Complete execution events/commands, selected source, LICENSE and baseline probe
are retained here; explicit private interpreter paths are replaced with `<PYTHON>`.
No author replay is credited as model evidence.

## Next improvement, not measured by this pair

The batching candidate retains runtime verification but still emits large
keyword searches and then reads overlapping source. Both arms show this pattern;
skill's first broad match output is 18,610 characters before its implementation
and test reads. This is an observed cost opportunity, not a proven attribution
of the 12.35% token difference. The next candidate replaces discovery prose with
filename-first discovery for unknown locations and bounded definition/consumer
context, avoiding full match dumps before reading known files. It must preserve
search expansion for unresolved consumers, runtime unknowns and required checks.
Its performance is unmeasured; do not rerun this exposed task for a preferred score.

Repository preflight: 406 tests passed in 63.226 seconds; seven native cookie
tests passed before scheduling. This pair does not update the featured benchmark,
localized numerical claims or charts, and does not establish an all-eight gain.
