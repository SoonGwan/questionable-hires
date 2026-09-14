# Installer audit transfer preflight — 2026-09-15 KST

This moves beyond the repeatedly exposed HTTPX ASGI task to the repository's real
standalone installer. Source and existing tests are pinned at
`07166bfcca6432f3954b6e1fb88e555acfe11d2a`. It is an author-selected controlled
audit of real code, not a newly reported user bug, independent holdout or model
performance result. No live model session has been scheduled for this transfer.

`preflight_installer_audit.py` copies 11 pinned files: installer, full installation
test module, license and the actual Necromancer/Receipt resource payloads used by
the selected tests. These payloads are installation data, not instructions for an
evaluating model. All four existing test bodies are unchanged. Only the test
`setUp` temporary-directory creation gains `dir=installer.ROOT` so test scratch
is explicitly inside the copied project. No global temp-variable changes.

Selected existing tests cover ordinary complete installation, rollback after copy
failure, cancellation cleanup preserving the original exception/user marker, and
continuing other cleanup when one removal fails. Remaining methods in the full
module are not run; this is not the complete installation suite.

| Implementation | Native result | Decisive observation |
| --- | --- | --- |
| Original | 4 pass | All selected contracts hold |
| Empty rollback loop | 3 fail / 1 pass | Copy/cancellation leave directories; cleanup attempts are missing |
| Catch Exception instead of BaseException | 1 fail / 3 pass | Cancellation leaves both newly installed directories |

Normal complete installation passes in both faulty variants. Cancellation is caught
by the existing test; the mutant failure is the subsequent filesystem assertion,
not a process interruption. The empty-loop cleanup-attempt failure is a mock-spy
assertion, while its other two failures inspect actual directory contents. Copy
and removal failures are controlled through the test's existing mocks; no real
disk exhaustion or filesystem permission failure is claimed. No syntax or setup
error is credited as a behavioral failure.

[Native retained output and adapted-input hashes](installer-audit-preflight.json)
record exit 0/1/1 and selected counts. Times are 0.017/0.016/0.017 seconds;
they are tiny local test durations, not developer or model speedups. Source files
inside each disposable project are unchanged by its tests; test scratch and outer
copies are removed. Author faults never modify the checkout or installed skills.
Home paths are redacted, including partial prefixes in unittest's abbreviated
assertion representations; outcomes/expected values are otherwise unchanged.

```sh
python3 -B benchmarks/preflight_installer_audit.py \
  --output /existing/directory/new-installer-preflight.json
```

Before model execution, freeze a task exposing selected tests, isolation/scope and
required evidence equally to fresh baseline/skill conditions. Keep author fault
recipes and expected results outside model inputs. Do not omit these conditions
to manufacture a shorter task, and do not reuse the prior ASGI scores as controls.

한국어: 실제 설치기와 기존 테스트를 고정해 다른 작업의 사전 대조를 만들었다.
테스트 본문은 그대로 두고 임시 디렉터리만 복사 프로젝트 내부로 지정했다.
정상은 4개 통과, 정리를 제거하면 3개 실패, 취소 처리를 제거하면 1개 실패했다.
실제 잔여 디렉터리를 검사하는 실패이며 정상 설치는 결함 대조에서도 통과한다.
복사 실패는 기존 테스트의 모의 오류 주입이지 실제 디스크 고갈은 아니다.
모델 비교·전체 스킬 성능 검증은 아직 시작하지 않았고 그래프는 변경하지 않았다.
