# Original command-output candidates01 — 2026-09-28

Parent `c37fd510`. Author evidence tooling only: no model call, test replay of a
measured solver, performance rerun or ordinary skill change.

The [Hostage scope lean review](HOSTAGE-SCOPE-LEAN-01-REVIEW.md#original-capture-correction)
found an actual98-character CLI summary with no native test headers. A one-off
collector skipped it because its suffix-matching branch required more than100
characters. Manual inspection recovered the original seven headers from the same
stored tool response. This is an evidence-navigation failure, not a failed test
or a reason to rerun the model.

Extend the existing [session extractor](extract_rollout_tools.py), instead of
adding another per-experiment collector. The returned/local summary now includes
`command_output_candidates`, matching **unredacted, nonempty** CLI output against
stored structured command-result text with the same integer exit code. There is
no minimum text length. References identify the CLI event line, paired call/output
lines and their hashes, call ID, output block index, text hash and relation.
The CLI-events hash binds the index to its exact input. Output text remains in
the existing selected tool records; the index does not duplicate whole outputs.

Statuses distinguish one candidate, ambiguous candidates, empty CLI output and
unmatched output. Running results, exit mismatches and outputs with missing,
duplicate or out-of-order call associations cannot supply a candidate. A single
candidate is **not verified command identity or complete stdout**. Inspect its
paired call and any earlier chunks; never infer missing output from a final answer.
Equal output from several commands remains ambiguous. No output is automatically
selected, concatenated, substituted into historical events or scored as a pass.

The existing command still takes an explicitly selected rollout/events pair and
a new local output directory:

```sh
python3 -B benchmarks/extract_rollout_tools.py \
  --rollout /path/to/the/exact/session.jsonl \
  --events benchmarks/local-runs/example/cell/events.jsonl \
  --output benchmarks/local-runs/example/cell/original-session
```

It neither searches sessions nor launches commands. Existing matching-session
validation, selected tool records and extraction behavior remain. The full raw
rollout may contain private instructions; keep it local and review/redact selected
evidence separately before publication. Candidate references contain no private
initial messages, command inputs or output bodies.

## Native controls and original evidence

Ten extractor methods cover the existing explicit-session/private-message/chunk
controls plus short98-character summaries, ambiguous equal suffixes, empty output,
wrong/running/boolean exits, missing/duplicate call or output association, string
envelopes and source/CLI line identities. Source/event bytes stay unchanged.
These are collector controls, not additional model-quality results.
The same suite was also run from a fresh source archive without Git history:
[parent](results/command-output-candidates-01/before.txt) lacks the new index and
produces eight missing-field errors across the six new methods/subtests; the four
existing methods pass. [Changed extractor](results/command-output-candidates-01/after.txt)
passes all10. These missing-field errors are feature-availability checks, not
application assertion failures. [Commands, exits and exact source hashes](results/command-output-candidates-01/native-check.json)
identify this native comparison.

The [read-only original-session check](results/command-output-candidates-01/original-session-check.json)
indexes all four terminal Hostage sessions. For candidate b/item9 it identifies
the same reviewed output at stored line39. The paired call contains the required
native command exactly once, and its full output equals the already-retained
seven-header evidence. Original session and event hashes remain unchanged.
The report retains only candidate references and scoped review facts, not private
records. No model/native solver invocation was repeated, and frozen usage/events
and the rejected candidate's decision remain unchanged.

This removes the ad hoc length threshold from future evidence navigation. It
does not repair the upstream capture issue, guarantee recovery for every tool
format or establish lower whole-task tokens/time. The all-eight objective remains
unmet; do not reclassify this author-tool change as a shipped skill improvement.

한국어:98자짜리 테스트 요약을 짧다는 이유로 복구 후보에서 놓친 실제 사례를
기반으로 기존 세션 추출 도구에 출력 후보 색인을 추가했다. 길이 하한 없이 원본
문자열·종료값을 대조하며, 여러 후보·빈 출력·실행 중 결과는 성공 증거로 단정하지
않는다. 같은 세션의 원본 줄·호출·블록 해시를 남기고 기존 기록을 덮어쓰지 않는다.
기존4개 세션을 읽기만 해서 이미 검토된7개 테스트 이름과 동일한 원본을 찾았다.
모델이나 테스트를 재실행하지 않았으며 스킬 토큰·시간 개선으로 주장하지 않는다.
