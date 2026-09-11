# Current Receipt package regression

Freeze all resources and unchanged receipt-package-cases.json at this protocol
commit. Current helper 302066c, entrypoint abb4b93, reference 48ec1c3. Run one
fresh baseline and skill session, Astra medium, serial, seed 20260911, timeout
240 seconds; no retries or exclusions.

This exposed regression follows real helper implementation changes. The prior
package task did show optional helper adoption, unlike recent tiny edit tasks.
Do not require the helper in the user prompt or alter task/criteria to favor it.
The prior baseline did not run historical code; its conclusion was not thereby
wrong, though it missed the stronger frozen-before criterion. Keep that distinction.

Inspect actual current/frozen-data historical checks, package import provenance,
resolved revisions, file preservation and captured failures. Current-only evidence
must not be mislabeled before/after. Tool use is not a score and non-adoption is
valid. Helper performance alone cannot establish model savings.

Report all input + output tokens, cached input once, process wall time, commands,
unequal work and capture limitations. This single development pair is not causal,
held-out or whole-bundle acceptance. Preserve prior favorable and adverse results;
do not rerun the pair merely for better numbers.
