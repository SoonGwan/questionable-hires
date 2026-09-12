# Two additional HTTPX audit tasks

Four fresh cells on the already frozen HEAD and exception tasks, Astra medium, serial, one sample per arm/task, no retries or excluded cells. Skill resources are pinned to `8c56744`; the later executable-mode fix is **not** included in these model runs. Preflight passed 36 tests. Original tracked files were preserved in all four cells according to byte comparisons and matching source revision; none timed out or recorded a rejected patch.

| Task | Baseline tokens / seconds | Skill + helper tokens / seconds |
| --- | --- | --- |
| HEAD body suppression | 157,754 / 103.030 | 141,839 / 57.847 |
| Default exception propagation | 105,042 / 60.023 | 116,279 / 44.661 |

Tokens include input (cached input once) plus output. HEAD used about 10.1% fewer tokens and 43.9% less time. Exception propagation used about 10.7% **more** tokens and 25.6% less time. Do not turn this into an all-metrics win. The seed scheduled both skill cells first, then baseline, so temporal/cache confounding remains. Author replay checks also overlapped later model execution on the shared host; wall times are descriptive, not controlled timing measurements.

## Evidence and differences

Both HEAD runs remove the same HEAD guard and show all 24 existing tests surviving. Both verify empty HEAD content, status and content-length under asyncio/trio against correct and faulty code. The baseline's proposed test additionally parametrizes GET as a control (four checks versus the skill's two); existing tests already include GET behavior, but the extra proposed control is still additional evidence and must be disclosed.

Both exception runs change only the constructor default from true to false. Existing tests pass 24/24 on correct code and fail four propagation checks on the mutant, with `DID NOT RAISE RuntimeError` before/after response completion under both async backends. Both correctly stop without demanding a stronger test for this fault.

The author inspected commands and results, extracted both actual skill JSON recipes and independently replayed them through the frozen helper. The HEAD outcomes were correct-tests 0, correct-probe 0, mutant-tests 0, mutant-probe 1 at the expected leaked-body assertion. Exception outcomes were correct-tests 0 and mutant-tests 1 at the expected propagation assertions. Baseline outcomes were inspected from retained artifacts, not independently replayed here.

The skill HEAD trace includes `ls -a ..`, an out-of-project parent-directory listing. This does not establish an outside write, but prevents labeling that run a strict project-only-scope success. Keep its behavioral result and metrics; do not silently exclude it or claim perfect constraint compliance. Final snapshots cannot prove absence of every transient action.

Both baselines wrote reusable audit scripts/reports and initially asserted an exact spelling of `sys.executable`; their assertions failed and were corrected. The helper avoids rewriting that interpreter-handling logic. This is an observed orchestration difference, not a complete causal attribution for timing or tokens.

Complete local evidence remains in `local-runs/httpx-tool-transfer-01`, including frozen resources, manifest, original logs, traces, final project copies and metadata. Preserve HTTPX's license if exporting source artifacts.

## Implementation correction made during the run

A separate local regression test showed that helper copies discarded executable permission bits, breaking a test that launches a selected shell fixture even on correct code. The test failed before the fix and passed afterward. Commit `99dbf23` preserves ordinary file permission bits while creating each copy; the original fixture stays unchanged. This is a concrete compatibility fix, not a performance claim or a change to the frozen comparison. The helper's 13 local tests now cover this path alongside its earlier failure/isolation checks.
