# Audit import hash01 — local allocation correction, 2026-09-27

Candidate **`ff0fbd2a`**, parent `43f5235a`.
[Exact author profile](results/audit-import-hash-01/profile.json),
[native log identities](results/audit-import-hash-01/logs.json).
Con Artist's copied-import verification previously hashed location.read_bytes(),
allocating the complete source again. It now hashes the same complete file in64KiB
chunks. Same path validation, SHA256, printed evidence, setup failures, native
runner/result observation and original/whole-project integrity checks. No cache
reuse across mutable reads, combined guards or changed skill entry instructions.

A new actual fresh-process regression imports the fixture before tracing, as
native unittest startup does, then executes the helper's real SETUP/verify_setup.
It checks the complete native import record against independently computed source
bytes, actual module value, small/chunk-boundary/4MB sources and Unicode tail.
[Before](results/audit-import-hash-01/before.log.gz) fails the large-source memory
assertion:4,005,694 is not below300,000. No import/setup error. The corrected
[checkout130](results/audit-import-hash-01/checkout.log.gz) and
[Git-free130](results/audit-import-hash-01/git-free.log.gz) tests pass,zero skips.
Archives use validated relative regular entries and the exact candidate files;
no repository history/model calls/dependency updates are needed for these tests.

On a separate4,000,013-byte ASCII module, author traced hash-verification peak is
**4,005,691→137,442bytes (−96.57%)**. Original/candidate printed records are exactly
identical. Exact source/setup hashes link the initially in-memory prototype to the
committed implementation. Input creation and module import are outside tracing;
this is intermediate allocation, not total RSS, full import cost or a total cap.
All source bytes are still hashed; filesystem reads remain non-atomic, as before.

Ten within-process untraced repetitions per variant,grouped original then candidate,
have medians0.001783→0.001744s (difference<0.04ms). This ordering/cache/one-fixture
measurement cannot prove repeatable speedup. No model-token/time comparison or
all-eight benefit follows from local memory savings. Previous adverse model costs
remain at their actually measured resources.

[Actual cached local CLI installation](results/audit-import-hash-01/installed.json)
checks all8 skills/51files byte/mode parity,9 Python entrypoints and25 command exits.
Installed Receipt retains native1/0; Con Artist0/0/0/1 and wrong-binding incomplete7;
Exorcist failure17/timeout124/cleanup and installed callback assets pass. These
exercises cover current installed code on the local host, not remote/platform
release or behavior on every instruction. Source and installed inventories remain
unchanged; owned copies are removed. No global settings/install or site deployment.
The [fd8b590d full-suite checkpoint](RELEASE-VALIDATION-FD8B590D.md) remains historical
and does not cover this later script change.

Native logs are explicitly path-redacted gzip reading derivatives; original and
reading-copy hashes are recorded separately. Originals remain local. The failing
assertion, native summaries and all profile samples are preserved. This is authored
functionality/allocation evidence, not independent model validation or goal completion.

한국어: audit-import-hash01(2026-09-27,후보`ff0fbd2a`)은 복사된 모듈의 import
해시를 파일 전체 임시 복사 대신64KiB씩 읽어 계산한다. 해시·출력·실제 테스트
판정·원본 변경 감지는 유지한다. 추가 할당 회귀 검사는 기존 코드에서 실제
assertion으로 실패하고, 체크아웃·Git 없는 복사본130개 검사는 모두 통과했다.
4MB 작성자 사례의 검증 중 할당4.01MB→0.137MB(96.57% 감소),격리 CLI 설치
8개 스킬51개 파일·25개 명령도 확인했다. 시간 차이는0.04ms 미만이고 전체
메모리·모델 토큰·시간 개선이나 전체8개 역할 목표 완료의 근거가 아니다.
