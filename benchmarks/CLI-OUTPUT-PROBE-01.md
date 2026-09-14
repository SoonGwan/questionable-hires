# CLI output localization probe — 2026-09-15 KST

This is a collector diagnostic, not a developer task or skill benchmark. Previous
[capture persistence](CAPTURE-PERSISTENCE-01.md) localized missing prefixes before
export, but did not distinguish model-visible tool output from CLI event output.
The installed standalone executable is `codex-cli 0.153.4`; no local CLI source
is supplied. No CLI installation, credentials or persistent settings are changed.

One baseline session uses the existing runner: Astra medium, serial, 240 seconds,
seed 20260915, ephemeral. Three exact commands produce tiny, bulk and line-flushed
outputs. Each contains unpredictable per-invocation BEGIN/END nonces and writes
an exclusive project-local witness before printing: nonces, rows, byte count and
SHA-256. Tiny has 8 rows; bulk/chunked each have 512 identical-size numbered rows.
Witnesses are deliberately not secret; the model is told not to read source or
witnesses. Review actual commands for alternate access before using nonce agreement
to infer visibility. Exact output is reconstructible from witness and emitter.

No retries/favorable draws. Retain all native errors, model deviations, original
CLI output and final answer. Compare per-command aggregate bytes against witnesses;
check started/updated events for recoverable fragments. A correct unpredictable
BEGIN nonce reported by a compliant model, absent from all CLI command output,
would support a gap between model-visible response and exported command events.
If both lack it, that does not isolate which upstream component removed it.
Successful controls do not resolve intermittent historical gaps.

```sh
python3 -B benchmarks/capture_probe_cases.py --output benchmarks/cli-output-probe-01-cases.json
python3 -B benchmarks/run.py --cases-file benchmarks/cli-output-probe-01-cases.json \
  --arms baseline --repeats 1 --jobs 1 --seed 20260915 --timeout 240 \
  --model gpt-6-astra --effort medium --output benchmarks/local-runs/cli-output-probe-01
```

OpenAI Docs [non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
documents JSONL events; it does not guarantee every byte of model-visible tool
output is present in a completed command event. No performance/quality gain,
historical transcript repair or chart update follows from this diagnostic.

한국어: 스킬 성능이 아닌 출력 수집 경로 진단이다. 작은 출력·큰 일괄 출력·큰
줄별 출력을 각각 1회 실행한다. 실행마다 새 표식과 별도 대조 파일을 만들고,
모델이 읽었다고 답한 표식과 CLI 원본을 비교한다. 대조 파일을 읽거나 명령을
바꾸면 그 영향을 공개한다. 설정 변경·재시도·기존 수치 수정은 하지 않는다.
