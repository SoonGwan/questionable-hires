# History invoice boundary 01 — frozen before execution

Date: 2026-09-15. Skill resource: `401eab9` (Necromancer compact CLI). One new
authored Python task, not a real production workload or independent task sample.
No prior model exposure of this payload. This tests the current skill against
no skill; it does not isolate serialization from other skill effects.

## Task and preflight

`history-invoice-01-cases.json` contains four Git commits and the same model-visible
ticket in both conditions. Two independent proposals: remove the integer-cents
branch, or replace half-away-from-zero rounding with truncation. The current sole
supported entrypoint accepts decimal strings and passes Decimal to the private
helper. Historical purpose and current necessity must be judged separately.
Both conditions must observe current, A-only and B-only behavior through the real
entrypoint on the same three disclosed inputs. No implementation or dependencies.

Before freeze, `test_history_invoice_fixture.py` passed both tests (0.390s).
Actual native unittest checks: current 3 pass, A-only 3 pass, B-only 1 pass and
2 assertion failures (`100 != 101`, `-100 != -101`). These failures arise through
the real caller with the independently substituted proposal, not an oracle-only
simulation or missing dependency. All original bytes remain unchanged; no
bytecode or scratch remains. Four actual commit messages match the fixture.
The fixture generator and frozen payload compare equal. Author controls are not
included in model context; all scored obligations are in the ticket/requirements.

## Fixed execution

Two fresh serial sessions, GPT-6 Astra / medium, 240 seconds each, one repeat,
seed 20260915, baseline/skill arms. Persist original sessions for capture review.
Do not force helper adoption: native Git is valid. No retries to obtain a better
score, no edits to frozen criteria, and retain timeout/failure outcomes. Review
actual selected commands, outputs, final answers, source preservation and resource
manifests before interpreting cost. Missing decisive output remains unknown unless
the same original session's stored tool response supplies it; author reruns are
separate. Shared host/cache and n=1 prevent causal or general performance claims.

```sh
python3 -B benchmarks/run.py \
  --cases-file benchmarks/history-invoice-01-cases.json \
  --output benchmarks/local-runs/history-invoice-01 \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260915 \
  --timeout 240 --persist-session
```

Compare total input (cache included) plus output tokens and process wall time.
Do not call lower cost a valid improvement if required work/evidence is unequal.
Only if the helper is actually used can output-mode adoption be observed; even
then this two-arm screen cannot estimate the isolated compact-format effect.
No featured-chart promotion or public release from a single pair.
