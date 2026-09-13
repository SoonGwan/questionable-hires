# Receipt HTTPX launch correction, before any model execution

The initial launch at `946af3b` failed in `freeze_skill`: its existing allowlist
accepted Con Artist, Landlord and Exorcist but not Receipt. This occurred after
creating the output directory and **before** snapshot export, manifest creation,
`disabled_skills` or any `run_cell` call. The empty
`benchmarks/local-runs/receipt-httpx-01/` directory remains. No model cell was
started, timed, discarded or retried.

A real snapshot regression fails on the original allowlist and passes when
Receipt is accepted. It compares every exported resource byte/hash with the
committed source, including the entrypoint, metadata, historical procedure and
comparison helper. No existing task profile, frozen Receipt resource or fixture
changes. The runner's task, order, limits and assessment remain those in
[the frozen protocol](RECEIPT-HTTPX-01-PROTOCOL.md).

After committing this launch correction, use the new output path
`benchmarks/local-runs/receipt-httpx-02`. Preserve the failed preparation; do not
delete it or describe it as a completed model attempt. The forthcoming run's
manifest records its actual launcher revision.
