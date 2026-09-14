# Store audit: valid work, no evidence of collector adoption

Frozen launch `889af32`; [protocol](../../CONDITIONAL-STORE-01-PROTOCOL.md).
Con Artist original `1d80f49` versus candidate `de65613`, both explicit skill
invocations. GPT-6 Astra / medium, original then candidate, one fresh persisted
session each, 240-second cap. This is a new authored synthetic developer task,
not a real upstream incident or independent project holdout.

| Condition | Total input + output tokens | Seconds | Shell / outer calls |
| --- | ---: | ---: | ---: |
| Original | 126,700 | 94.406 | 7 / 5 |
| Candidate | 125,053 | 86.877 | 7 / 5 |

Candidate records **−1.30% tokens / −7.98% time**, with cached input included once.
Both complete all required audit and test-improvement work. **Neither reads the
changed collector guide nor executes the collector** (or the audit helper).
Both directly read the small supplied files and build native disposable-copy
orchestration. The skill entry is identical, so this pair does not exercise the
changed capability and cannot support a causal improvement claim. No no-skill
baseline, featured promotion or broad efficiency conclusion.

## Actual work and outcomes

Both trace `submit` → `FileStore.save` → default JSON `encode` → `write_bytes`.
Both select the same meaningful payload-loss fault: persist `b"{}"` instead of
the encoded content, preserving file creation and acknowledgment. Instrumented
copies retain actual module paths/bindings and effective codec observations.
The author preflight used JSON null; the models independently choose another
valid content-loss fault under the frozen acceptance criteria.

Both run:

| Tests and implementation | Native outcome |
| --- | --- |
| Original tests, correct copy | 2 pass / exit 0 |
| Original tests, faulty copy | 2 pass / exit 0: fault survives |
| Improved tests, correct copy | 2 pass / exit 0 |
| Improved tests, faulty copy | 2 assertion failures / exit 1 |
| Improved tests, original project (extra final check) | 2 pass / exit 0 |

Each improved test decodes actual UTF-8 JSON and compares the entire semantic
value, while retaining acknowledgment assertions. Faulty outcomes show `{}` versus
the expected title/count dictionaries, not import, binding or syntax errors.
Original additionally gives the first replacement payload an `obsolete` field;
exact equality then also checks its removal. Candidate retains the original
payloads. This extra work and ordinary run variation limit cost comparisons.

Both preserve all original production/README/package-marker files and installed
skill resources; only `tests/test_submit.py` changes. Reviewed commands create
scratch under project cwd and explicitly remove the owned copies. Final actual
workspace inventories contain no extra non-Git/non-skill files. No network,
installs, environment edits, timeouts or account limits. Final identity does not
prove absence of every transient write; commands and original outputs provide
the additional scope evidence.

## Capture review

[comparison.json](comparison.json), manifests, commands, final tests/diffs,
answers and selected stored tool records are retained. Fourteen shell commands
map to fourteen parsed stored output/exit pairs. Ten match exactly after path
normalization. In **both** conditions, CLI `item_5` and `item_7` retain only a
suffix, losing the correct-copy phase and its label; original stored responses
contain both complete native phases. The pairs are unambiguous suffix matches:

| Condition / CLI item | CLI characters | Stored characters | Native summaries CLI / stored |
| --- | ---: | ---: | ---: |
| Original / item_5 | 1,374 | 2,933 | 1 / 2 |
| Original / item_7 | 2,417 | 4,012 | 1 / 2 |
| Candidate / item_5 | 1,380 | 2,895 | 1 / 2 |
| Candidate / item_7 | 2,323 | 3,838 | 1 / 2 |

Counts above use path-normalized text. The complete required four phases plus
extra final check are in original stored records, not inferred from the final
answer or recreated by author replay. No missing/unmatched outer output IDs,
duplicate call IDs or unparseable output JSON. Full rollouts stay local because
they contain private instructions; exported line hashes identify raw originals.

## Next decision

Keep the separately verified conditional-selector correctness fix, but leave its
model benefit unmeasured. Do not force helper usage or add collector instructions
to small audits merely to make a benchmark exercise it. Further performance work
needs a task where required orchestration/context volume creates a real cost that
the helper can remove, not another repeat of this already-solved small case.
Shared host/cache, fixed order, n=1 and authored development exposure remain.

한국어: 양쪽 모두 실제 저장 내용 누락을 기존 테스트가 놓친다는 점을 확인하고,
두 테스트를 올바르게 보강했다. 정상 코드에서 통과하고 결함 코드에서 실제 값이
남는 단언 실패가 발생했으며 원본 보존·임시 복사본 정리도 충족했다. 수정본은
토큰 1.30%, 시간 7.98% 적게 썼지만 양쪽 모두 변경된 수집기를 사용하지 않아
수정 효과로 주장할 수 없다. CLI 앞부분 누락은 원본 세션의 완전한 응답과 대조해
확인했고 근거를 보존했다. 작은 감사에 도구 사용을 강제하거나 이 결과를 대표
그래프에 올리지 않는다.
