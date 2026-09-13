# Frozen Receipt seeded-HTTPX pair

Freeze this protocol and `run_receipt_httpx.py` before execution. Use the prepared
fixture `8ed44f4f3d3c06bc408b378e435f9e106a7d4254` from the
[native-test preflight](RECEIPT-HTTPX-PREFLIGHT-01.md), not a freshly reseeded copy.
Receipt resources are frozen at `562c25a`, including consolidated entry `f32de37`.
No historical benchmark or original upstream source is modified.

One fresh baseline and skill session; baseline first, serial, Astra medium,
240-second limits. No retry, exclusions, candidate edits, altered criteria or
concurrent author tests during timing. The task text in the runner is identical
apart from explicit skill invocation and includes the exact native three-test
command and preinstalled interpreter. Stop scheduling on recognized account limits.
Preserve failed/incomplete outcomes. Runner interruption is not permission to retry.

Assessment: captured set-parameter assertion failure with add/remove controls
passing before production edits; all three unchanged tests passing afterward;
correct replacement logic/public API; only `_urls.py` production change; all
other 124 tracked files preserved; focused diff review; no dependency install,
outside-project discovery or changed runner settings. Do not credit setup errors,
skipped tests or final prose as actual before/after execution. Inspect original
events, resource hashes, final project, flags and statuses, not completion alone.
Record any additional work or repairs rather than assuming equivalent effort.

Report every input-plus-output token count (cached input included once), process
wall time and task outcome. This is actual upstream code with an authored fault,
not an organic historical bug, causal compression experiment, held-out all-eight
gate or broad superiority proof. n=1 and shared host/cache/order limit conclusions.
Fewer calls do not establish savings; adverse results remain. No automatic
featured/localized chart replacement and no exposed-task rerun for better scores.

```sh
python3 -B benchmarks/run_receipt_httpx.py \
  --fixture benchmarks/local-runs/receipt-httpx-preflight-01 \
  --output benchmarks/local-runs/receipt-httpx-01
```
