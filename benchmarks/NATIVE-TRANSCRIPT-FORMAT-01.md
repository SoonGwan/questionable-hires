# Native transcript output prototype01 — rejected, 2026-09-27

Prototype against repository `8200cfc0`. This is an authored output-format
experiment, not a new measured skill resource or model run. Original data remains
native-split02 candidate **`6c099d68`**, with its
[scoped review and limits](NATIVE-SPLIT-02-REVIEW.md) unchanged.

The concrete hypothesis was that a direct `--transcript` CLI mode could avoid
custom JSON-output rendering code and native text escaping. The optional mode
kept compact JSON as default, retained metadata, native outputs, truncation and
reuse fields, and forwarded the same observed/incomplete CLI status. It moved
native text into length-labeled sections so marker-like output could not replace
or silently truncate a check during reconstruction. It did not skip checks.

The retained [prototype patch](results/native-transcript-format-01/rejected-prototype.patch)
contains the implementation and meaningful controls: exact roundtrip/nonmutation
for Unicode, NUL, embedded section markers and reused observations; actual
module-mode native pass/fault assertion and incomplete binding-precheck execution,
with source/scratch preservation. Four focused output tests pass. The first
broader module-style invocation discovers23 tests but fails3 imports because
sibling test modules are not on its path; it is not a passing validation.
Corrected `PYTHONPATH=tests` invocation of the existing validation interpreter
runs30 tests, zero failures/skips,8.106s:

```sh
PYTHONPATH=tests /path/to/validation/python -B -m unittest \
  test_audit_output test_audit_module_invocation test_audit_probe_cache \
  test_audit_native_batch_guide -q
```

The command redacts the actual local interpreter path with a placeholder; the
executed existing environment uses Python3.11.6, not a new installation. No current archive, install or model performance claim
follows from a rejected implementation's checks.

[Representation comparison](results/native-transcript-format-01/comparison.json)
uses identical retained single-audit records and the three retained batch audits.
The batch envelope is reconstructed from its original printed records and final
status/limitation; this is not a new original CLI capture. Source hashes and the
prototype patch hash are retained. Both comparisons append one trailing newline.

| Authored formatting of retained observations | Compact JSON characters | Transcript characters | Change |
| --- | ---: | ---: | ---: |
| Single |13,790 |14,055 |+265 |
| Multiple |21,642 |22,447 |+805 |

UTF-8 byte counts equal character counts for these selected ASCII records. Section
metadata/boundaries outweigh removed escaping. Characters are not model tokens;
this does not prove higher token costs, nor measure saved custom code, model
adoption, latency or whole-task work. It does fail the proposed representation-size
benefit on these exposed records. Do not spend a fresh model comparison merely to
turn this unfavorable preliminary result into an efficiency claim.

**Decision: reject the prototype.** Restore exactly the three owned modified
skill/test files. No new CLI option, dependency, formatter API or permanent test
is adopted. The patch is retained as a rejected historical artifact. Existing
lossless compact JSON, shared-observation pointers and optional saved-report
inspection remain available. All-eight quality/token/time goals remain unmet;
this eliminates one unsupported optimization path without weakening evidence.

한국어: 네이티브 원문을 직접 읽는 선택형 출력 시제품을 만들고30개 검사를
통과했지만, 기존 compact JSON보다 단일265자·배치805자가 더 커졌다. 문자 수는
모델 토큰이 아니며 실제 모델 비용을 측정한 결과가 아니다. 시제품은 채택하지
않고 원래 스킬·테스트 파일로 되돌렸다. 전체8개 역할의 목표는 계속 미달이다.
