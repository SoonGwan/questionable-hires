# Flag handoff 01 — synchronous transfer, 2026-09-15

Resources `fe3faa8`. Two newly authored synchronous task variants move beyond
the repeatedly exposed async refresh pair: incorrect truthiness vs valid explicit
boolean parsing, same task/contract. These remain correlated synthetic examples,
not real-user deployment evidence or proof about all eight skills.

Frozen `hostage-flag-cases.json` SHA-256:
`aab8a877f828a4df84a425862d6fc676aba8d183b91760348b5bb2bbd23a7574`.
[Generator](hostage_flag_cases.py), [native preflight](hostage-flag-preflight.json).
Five author contract methods accept correct production and reject bad false-token
handling and absent ValueError with actual assertions, no setup errors. Two fixture
tests pass (0.078s). Scratch is project-local, removed, sources unchanged.

## Prospective execution

Four fresh sessions: baseline/explicit skill × two variants × one repeat,
serial Astra medium, seed 20260911, 240s/cell. No selected retries; retain every
scheduled cell, failures, gaps and unknown usage; stop scheduling on account
limits. No author workloads or resource/input edits during timing. The model
gets only the frozen six project files, task and its arm's installed resource,
not the oracle, fixture labels, prior conclusions or this protocol.

Both arms receive the same durable-evidence requirement because it is the task's
handoff contract. Do not require use of the skill recipe; equivalent native
reporting is valid. No deliberate terminal-output loss is injected: assess real
captures and retained artifacts, not a simulated CLI defect.

## Review before any performance claim

- Correct exact true/false spellings, surrounding whitespace/case, missing/None
  with both defaults, invalid/blank ValueError, mapping preservation and caller.
- Preserve valid production, existing tests, owner notes and prior evidence.
- Retain rerunnable tests using actual production. Native command, actual output
  and own exit must be retained per verification run and inspected before claims.
  Check artifact provenance against execution events, not self-reported JSON alone.
- Keep task scope. Async helper use is unnecessary here; inspect whether routing
  avoids irrelevant assets/references. Do not award points for arbitrary brevity.

After timing reconcile raw usage/resources and all retained files. Separate author
replays will run retained tests against actual final production, truthiness fault
and an equivalent valid implementation; frozen oracle checks final production.
Inspect actual assertion/cleanup paths. Replays cannot repair original evidence.
Publish all four cells and per-pair costs/work differences, including regressions.
No historical/featured chart change, general percentage claim or automatic
promotion from these two examples.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/hostage-flag-cases.json --output benchmarks/local-runs/hostage-flag-01 --arms baseline skill --repeats 1 --jobs 1 --seed 20260911 --timeout 240 --model gpt-6-astra --effort medium
```

## 한국어

환경변수 문자열 파싱과 테스트 기록 전달을 새 과제 2종으로 고정했다. 정상/오류
사전 검증은 끝났고, 기본/스킬 모두 같은 증거 보존 요구를 받는다. 스킬 예시를
반드시 쓰게 하지는 않는다. 새 4세션을 실행하며 정답 테스트는 모델 입력에서
제외한다. 작성 예제 2종 반복 1회이므로 전체 실사용 성과로 부르지 않는다.
