# Receipt frame parsing: equal required verification

Freeze `receipt-frame-cases.json` and all Receipt resources at `f13a097` before
execution. This new authored task is a development transfer check, not an
independent real-repository holdout or a replacement for all-eight acceptance.
It changes task complexity relative to earlier boundary/invoice tasks; no causal
comparison to their recorded scores is allowed.

Both arms receive the same five supplied tests and an explicit requirement to
run them before production changes and unchanged afterward. The author preflight
in `tests/test_receipt_frame_fixture.py` observes three passes/two assertion
failures on the original implementation and all five passing on a separate
author-only witness. Actual failure output contains the missing hello and
world/last payload lists, not support exceptions. Original inputs remain byte
identical apart from the author witness's production file. Tests are in-memory;
there are no fixture scratch files, external services or dependency installs.
The witness is not copied into either model project.

One fresh baseline and skill session, serial, Astra medium, 240 seconds per cell,
seed 20260911. No retries, candidate edits, changed tests/criteria, exclusions or
concurrent author tests during timing. Retain incomplete/failed sessions and stop
new scheduling on a recognized account limit. The runner records resource hashes,
fixtures, order, usage and traces. This consumes model usage already within the
owner's requested benchmark workflow.

Review original command outputs, before/after ordering, unchanged test bytes,
final implementation, diff review, installed-resource integrity and scope before
comparing costs. Completion is not a pass. Missing outputs remain unknown; author
replay cannot fill original evidence gaps. Extra coverage/repair/runner changes
must be reported as unequal work, not silently counted as equal verification.
Required coverage is the same; equal effort is not presumed from that design.

Report all input-plus-output tokens (cached input included once), process wall
time and observed work. A favorable n=1 result does not prove broad 20–30%
improvement; an adverse result remains visible. No featured-chart change follows
automatically. Do not repeat this task to obtain a preferred score.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/receipt-frame-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 \
  --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/receipt-frame-01
```
