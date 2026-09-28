# 0.2.0 candidate validation — 2026-09-29

This is local release preparation and authenticated draft-asset delivery, **not a
new model benchmark or a published release**. [PR #2](https://github.com/SoonGwan/questionable-hires/pull/2)
is draft. Plugin metadata is `0.2.0`; main has not been merged and no version tag
has been published. [Release conditions](../docs/RELEASE-READINESS.md) remain unmet.

## Failures retained and fixes

1. Source `ec8df78b`: 1,542 discovered tests, one error. A historical Friday
   candidate test read the evolving live guide. Fix `e033f928` pins the exact
   `75f6b4f` guide as an explicit fixture and checks SHA-256
   `71a4e46504485f486bf8fd08e8ac3f024e06fc44a39c520e963552ac3104ac84`.
   The two focused tests pass in checkout and a Git-free copy on Python3.9/3.11.
2. Source `cc5102ac`: checkout 1,542 pass, zero skips. The separate full Git source
   archive discovers1,542, with one failure and30 history-dependent skips:
   generated `skills.tar.gz` differs because Git archive modes are0664/0775 while
   checkout modes are0644/0755. All55 payload bytes are identical.
3. New regression: five standalone tests, one failure before the packaging fix.
   Fix `a002981c` normalizes distribution modes to0644/0755 using the owner execute
   bit. The five standalone tests pass on Python3.9.6 and3.11.6. Checkout download
   bytes remain unchanged; this does not modify installed skill behavior.

Original log hashes and path-redacted compressed readings are retained in
[suite records](results/release-020-candidate-20260929/suite-records.json).
Failures and skipped historical comparisons are not counted as passes.

## Final verification

Tested source **`a002981ce46583d7359f183ffa170e483232b1c3`**, Python3.11.6
and Node24.16.0:

| Environment | Discovered | Passed | Skipped | Failures/errors | Native seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Git checkout | 1,543 | 1,543 | 0 | 0 | 246.394 |
| Fresh Git-free source archive | 1,543 | 1,513 | 30 | 0 | 229.855 |

Both exit0. Runs shared the host concurrently; these durations are validation
records, not a performance comparison. Thirty archive checks explicitly require
repository history. Later changes are documentation and evidence only.

한국어: 검증 소스 `a002981c`에서 체크아웃1,543개 통과, 소스 압축본1,513개
통과·이력 의존30개 생략이며 실패는 없습니다. 두 실행은 같은 호스트에서 동시에
진행했으므로 실행 시간을 성능 비교로 사용하지 않습니다.

Catalog/UI/plugin/current-document-link checks pass. Featured synchronization
reports already current and `--check` succeeds; both READMEs retain integration07
and the frozen Mother confirmation. All151 generated preview files match.
The separate dated Markdown scan covered3,631 tracked files/15,635 relative links
before the final documentation additions. Seven missing links occur in retained
model answers or partial historical source snapshots; these originals were not
rewritten. See [scan](results/release-020-candidate-20260929/markdown-links.json).

The existing credential/auth-header pattern scan reviewed5,104 newly reachable
blobs through `ec8df78b`, with zero findings. This is a bounded pattern check,
not a guarantee that all possible secrets are absent. Subsequent changes contain
reviewed documentation, test fixtures, package permissions and validation evidence.

## Actual artifacts and installation

The standalone archive is109,104 bytes, with55 payload files plus `CONTENTS.json`:
8 skills/52 skill resources, installer, license and bilingual install guide.
SHA-256: `ecb7f50419d1d46c3a491c414da728b2eab281caee0141672c98cc779c2fdaee`.
Two builds at `cc5102ac` match; rebuilding with fixed packager `a002981c` also
matches. Extracted bytes/hashes/modes match the manifest. Actual isolated offline
installation matches on Python3.9/3.11; all10 Python entrypoints pass `--help`
smoke checks in each. The full suite separately tests installed helper behavior.
These smoke checks alone are not exhaustive behavior validation.

The plugin ZIP is141,353 bytes, version0.2.0, built at `cc5102ac`; all52 resources
match. Its SHA-256 is
`820e3717a29433f092efdb6214de8eecd625f1b117526535f31ac9c95d45d83d`.
ZIP reproducibility was not claimed. See [artifact review](results/release-020-candidate-20260929/artifact-review.json)
and [source identities](results/release-020-candidate-20260929/RELEASE.json).

The authenticated GitHub draft contains both packages, `SHA256SUMS` and
`RELEASE.json`. Each was downloaded back from the release-asset API and compared
byte-for-byte with its local original; all four match. Cross-host redirects strip
Authorization. [Upload metadata](results/release-020-candidate-20260929/release-assets.json)
and [download checks](results/release-020-candidate-20260929/release-download-check.json)
record exact sizes and hashes. Draft assets require authorized access; this is
not an anonymous public-release installation check.

No hosted site deployment or new browser QA occurred in this checkpoint. The
previous hosted source remains `281c3cf0`; its standalone bytes match this
candidate, but that does not make the entire hosted revision current.
No personal installation, workflow setting or billing setting changed.

한국어: 2026-09-29의 로컬 후보·초안 전달 검증입니다. 과거 Friday 테스트 입력
오류와 소스 압축본 권한 때문에 다운로드가 달라지는 오류를 재현하고 수정했습니다.
실패·생략 결과는 원본 해시와 함께 보존합니다. 스킬8개·리소스52개 설치와 각
Python 버전의10개 `--help` 확인을 완료했고 GitHub 초안의4개 파일도 재다운로드
후 원본과 일치했습니다. 원격 CI·새 모델 성능·새 공개 사이트 배포·정식 출시를
뜻하지 않습니다. integration07의 토큰+1.67%·시간−9.63%·동시 감소2/8은 변함없으며
사용자가 요청한 전체 품질·토큰·시간 목표와 독립 검증 환경 문제는 남아 있습니다.
