# Bounded log collection

The previous helper (`99dbf23`) used `communicate()` to capture the full test
output before slicing its last 12,000 characters. A local regression emitting
8,000,000 ASCII characters plus a final marker measured 24,027,277 bytes of
peak parent Python allocation with `tracemalloc`; its 2 MB budget failed.
Another regression emitting invalid UTF-8 raised `UnicodeDecodeError` instead
of returning the child's exit status.

The replacement drains the merged output pipe in 4 KB chunks, incrementally
decodes UTF-8 with replacement, and retains a 12,000-character tail. It uses
the same deadline for pipe collection and process completion; timeout still
terminates the owned process group and marks the audit incomplete. Stdin is
closed so unattended test input cannot consume the caller's terminal input.
Timed-out output can be incomplete; this is documented rather than represented
as a full log. This remains a trusted-test runner, not a security sandbox.

The 8 MB workload after the change measured 106,995 bytes peak parent Python
allocation in a separate local check, retaining the final marker and exit 0.
This is an internal allocation comparison, not total RSS, child memory, model
token savings or end-to-end skill speed. The child deliberately allocates its
large output string. No model benchmark was needed to verify this mechanism.

Five new tests cover bounded large-output allocation, invalid UTF-8 with exit
7, continuous output under deadline, multibyte characters split across chunks,
and a process that closes stdout/stderr but keeps running. The full local suite
passes 70 tests, including previous mutation, import, timeout, mode preservation,
copy integrity and packaging checks. The character and invocation contract
are unchanged; only helper implementation and its limitations documentation
changed. Broad all-skill performance remains unproven.
