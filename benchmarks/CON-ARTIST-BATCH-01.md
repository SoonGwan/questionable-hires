# Shared baseline: deterministic work removal, model effect unmeasured

The HTTPX isolation trace performed the same correct-code test suite twice for
two distinct faults. The optional batch interface now accepts shared input files,
imports and runner arguments with up to eight independently specified mutations.
It reuses only a successful baseline with matching selected bytes, file modes,
imports, runner arguments, interpreter, timeout and environment within one call.
Every mutant and every stronger probe still executes in a fresh copy.

This is not an automatic mutation campaign or cross-session cache. It is unsuitable
when the next fault depends on the first result, or external state, dependency
changes, randomness or flaky tests require fresh baseline observations. No new
entrypoint mandate requires batches. Reused evidence is explicitly marked and
must not be counted as an independent execution.

## Verification

Six additional behavioral tests exercise actual child processes, result parity,
process-count reduction, failed-correct-probe stopping, file/environment cache
invalidation, CLI dispatch and rejection of unsupported batch scope overrides.
Two four-check audits use seven child processes rather than eight; probes remain
independent. The full suite passes 126 tests in 11.684 seconds. Repository and
skill validators also pass. These checks establish mechanics, not model gains.

Author replay extracted the two exact JSON recipes from the original
`httpx-isolation-01/wsgi-cleanup--skill--1/stdout.original.jsonl` and combined their
identical shared fields. It used the existing HTTPX source at
`26d48e0634e6ee9cdc0533996db289ce4b430177` and preinstalled Python 3.9.6 environment.
No new model session ran and no original result was replaced.

- Five actual child processes, versus six in the recorded separate invocations.
- First fault: correct suite passes; disabled cleanup produces nonzero exit and
  iterator-finalization failure evidence.
- Second fault: same successful baseline reused and marked; existing mutant suite
  passes 12 tests; correct resource-cleanup probe passes; mutant probe fails.
- No timeout; source repository remains clean after disposable copies are removed.

The check count is a directly observed work reduction, not a 16.7% wall-time or
token claim. Baseline reuse reduces independent observations; different faults
remain independently exercised. Actual model adoption and net cost, including
the longer optional interface, are unmeasured. The overall objective remains unmet.
