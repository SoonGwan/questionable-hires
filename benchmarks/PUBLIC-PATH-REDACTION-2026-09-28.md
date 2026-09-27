# Public export path correction — 2026-09-28

A pre-publication scan of4,237 added/modified files (38,501,048 bytes) relative
to fetched origin/main identifies the owner's absolute home path in10 exported
records: three landing-test failure logs, one legacy-pytest control failure log,
and six solver launch records. These were actual findings, not test/model failures.
The scan also checks known account-ID/credential patterns; absence of those
patterns is not comprehensive secret detection or publication approval.

Use the existing export redactor on those10 current files. Original bytes are
retained under ignored `local-runs/public-path-redaction-20260928/`; the
[manifest](results/public-path-redaction-20260928/manifest.json) records original
and current-public SHA-256 values and byte counts. JSON still parses. The first
whitespace check flags one trailing space on the redacted pytest rootdir line;
that space is removed in the public copy and disclosed in the manifest. Only path
representations change; failures, timings, exits, decisions and measured source
identities are not rewritten. Prior attempts remain adverse where applicable.

Existing local Git commits also retain the preceding exports. This is a current
tree correction, **not a Git-history purge**. No remote push occurs in this check;
publishing an entire history is a separate decision from verifying the current
export tree. The unchanged hosted site is not described as a new release.

한국어: 공개 예정 기록10개에 남아 있던 실제 로컬 경로를 기존 redactor로
정리했다. 원본은 비공개 실행 폴더에 보존하고 원본·공개본 해시를 함께 기록한다.
수치·실패·소스 식별자는 바꾸지 않으며, 이전 로컬 Git 이력을 지웠다는 의미도
아니다. 이 검사에서 원격 push나 새 호스팅 배포는 하지 않았다.
