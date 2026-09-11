# Configured consumer under examples: observed, not discarded

[Protocol](LANDLORD-CONFIGURED-PROTOCOL.md), fixture/resources `1a874d9`,
Landlord `26a310d`, runner `1af97bb`. One fresh Astra medium auto session,
serial, 240-second limit, no retries/exclusions. All eight skills installed;
Landlord selected and read without an explicit invocation. Local originals:
`local-runs/landlord-configured-01/`.

Actual commands read app.py, deployment.json and examples/embedded_driver.py;
the answer identifies that provider as supported application code despite its
directory name. `python3 -B app.py` returns created true then false, and the
documented two-test contract group passes. An in-memory substitution of Store
in the test module produces three creation-subtest failures (`None is not True`)
while the operational-error test passes. Separate executed probes capture
None on creation, Duplicate on repetition, preserved original value and Duplicate
from app.run after replacing the loaded provider's factory with Backend.

The experimental command exits 0 because it observes expected failures; it does
not propagate unittest's failed result. Its actual failure output and counts,
not its shell status, establish the counterexample. The unchanged original suite
and application have separate successful commands. No author replay is credited
as model execution.

The recommendation preserves semantic translation, explains compatible inlining
and provider/test updates, and does not claim a demonstrated maintenance saving
or staging verification. Caller-content search excludes installed skill trees
but follows the configured examples path. A separate listing still emits all
27 installed resource paths, so unnecessary discovery output remains.

Usage: **88,967 tokens** (87,939 input + 1,028 output; 79,104 cached input
already included), **47.300 seconds**, eight shell commands. No baseline arm or
causal efficiency claim. This is an explicitly requested, authored configured-path
check, not spontaneous discovery or a general exception-handling guarantee.

All nine original files match the frozen fixture; diff is empty and all 27
resources match frozen Git hashes and before/after inventories. Original/redacted
events match under intended substitutions. Capture diagnostics have no flags;
decisive outputs were inspected. No external services, installed dependencies,
original-file changes or manufactured staging receipt appear in the trace.

This supports the new discovery guidance on this boundary: application relevance,
not directory naming alone, determines what to inspect. Broad efficiency, less
directed requests and other configured-loading mechanisms remain unverified.
