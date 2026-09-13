# Con Artist: same-process caller prechecks without temporary binding modules

The [all-eight gate](BUNDLE-CONTRACT-03-REVIEW.md) records Con Artist loading
helper implementation and creating a temporary imported binding module before
the audit. Core outcomes were valid, but token cost rose 70.42% against its
baseline. This change addresses that observed orchestration burden; it does
not retroactively change those costs or prove a new performance gain.

## Interface

Optional JSON `precheck` is Python assertion code executed after copied imports
and before each test/probe **in that same child process**. The public example
checks the real unittest method's global save identity, without a temporary
module or additional import-only process. Normal recipes remain supported.
Shared batch prechecks are supported and become part of both reusable correct
test and probe identities; changed prechecks invalidate reuse.

Precheck exceptions, including SystemExit(0), print a labeled diagnostic and
return reserved check exit 6. With precheck enabled, exit 6 stops even a mutant
phase as incomplete, not a killed fault. Existing timeout/output/cleanup handling
also applies. This conservatively treats test/probe exit 6 as incomplete in that
mode rather than risking mistaken coverage credit.

The check establishes binding **at its execution point**, not that a later test
calls the function or that fixtures never rebind it. Call traces still require
actual observation when requested. Pytest test imports can bypass rewriting;
the reference directs post-collection binding needs to native fixtures/hooks,
not this pre-import shortcut. Trusted code only, not a sandbox. Do not alter
behavior in a precheck to make evidence pass.

No entrypoint/description/UI/automatic-selection change. Helper and its existing
public reference change; the skill-creator principle applied is moving repeated
deterministic orchestration behind a usable interface while keeping limitations.

## Author checks

Five new tests exercise actual child processes:

- A real imported test global equals copied implementation in all four phases;
  existing checks survive missing append and the stronger assertion kills it.
  Original fixture bytes and owned-copy cleanup are checked.
- Wrong assertion, early successful exit and mutation-sensitive precheck stop
  as incomplete. In particular, a precheck failing only on mutant code is not
  mistaken for test sensitivity and later probes do not run.
- Changed precheck invalidates both cached correct observations (four fresh
  executions), invalid types execute nothing, and shared batch prechecks work.
- An endless precheck times out, stops before further phases and cleans copies.

Focused suite: **60 tests pass (9.733 seconds)**. The initial author test run
failed because its binding assertion named SaveTests instead of the fixture's
actual Tests class; correcting that test selector fixes the preflight. No model
benchmark was rerun or hidden. Skill/catalog/featured consistency checks pass.
Full repository suite: **364 tests pass (51.475 seconds)**, including packaging;
no skill resource edits occurred during that run.

Remaining evidence: real model adoption without unnecessary source inspection,
equivalent verification and lower end-to-end costs on separate realistic tasks.
Do not repeat the exposed persistence case for a preferred score or substitute
these helper tests for all-eight real-development improvement. Featured figures
and previous adverse results are unchanged.

## Shipped example integration

The public two-fault recipe now includes the optional same-process binding
precheck. The single-audit reference names the same actual example method,
`SaveTests.test_acknowledges_save`, instead of an unrelated illustrative selector.
Both interfaces remain optional; no entrypoint or helper algorithm changed here.

A packaging regression builds the distributable into a path containing spaces,
copies the actual example source files into a separate project, extracts the
literal JSON from the bundled reference, and executes it through the bundled
CLI with stdin. It also executes the public batch recipe unchanged. Both preserve
all project file bytes/modes and leave no scratch files; existing tests survive
the faults, correct probes pass, and mutant probes produce AssertionError. The
batch keeps correct-observation reuse and exposes duplicate stored values.

An author-only negative control changes the live implementation binding after
the test import. The shipped precheck then produces assertion evidence and
reserved exit 6; CLI exit 2 and only the correct-test phase confirm that no
mutation success is awarded. This intentionally altered precheck is test support,
not a recommended user recipe or a measured model action.

Packaging suite: **12 tests pass (2.948 seconds)**. This validates local built
resources and documentation usability, not remote installation, model adoption,
token savings or a new benchmark. No featured/chart values change.
Full repository suite: **365 tests pass (52.354 seconds)**; skill/catalog,
localization/featured consistency and patch whitespace checks pass.
