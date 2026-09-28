# Friday JSON numbers01 — 2026-09-28

Parent `371b4b1e`. Actual SQLite can return positive/negative infinity for valid
queries such as `SELECT 1e999`. The helper previously emitted bare Infinity tokens
while returning CLI0/complete=true. JavaScript JSON.parse rejected that output
with SyntaxError, so completed native evidence could not be consumed as JSON.

`format_result` and the CLI now encode non-finite floats as explicit objects:
`{"float_special":"Infinity"}`, `{"float_special":"-Infinity"}` and, for a caller-
supplied NaN, `{"float_special":"NaN"}`. This does not claim SQLite returns NaN.
Serialization enforces strict JSON, preserving finite numbers, text/nulls,
duplicate column labels, existing BLOB tags and failed-reader records. The native
matrix result remains unchanged, including tuple rows and float values used by
assert_rows. It does not rerun SQL, replace infinity with null or infer compatibility.
Consumers that need special numeric values must interpret the documented tags.

[Five new tests](../tests/test_friday_json_numbers.py) record4 strict-JSON errors
before and5 passing methods after, with the ordinary-value control passing both.
The [actual Node consumer comparison](results/friday-json-numbers01/consumer.json)
uses the same SQL/consumer: native CLI0 in both, JSON consumer1/SyntaxError before,
consumer0 with both tags and preserved finite/BLOB cells afterward. The parent
helper is taken from the exact source revision; source/output hashes are retained.

Existing matrix42, row-assertion8 and recipe-key8 controls pass. The Git-free copy
initially omits two existing fixtures and yields2 FileNotFoundErrors; preserve that
incomplete-copy attempt. A separate complete copy supplies the two frozen fixtures
and passes all63 methods without Git/history access or skips. The historical
model-output fixture checks serialization only, not fresh model behavior.
Original logs are in [the evidence directory](results/friday-json-numbers01/).

Both Friday references and English/Korean helper capability descriptions explain
the wire format. Root README onboarding and dated historical snapshots are not
expanded or rewritten. Featured data and all existing model cost claims are unchanged.
This is a native correctness fix; zero model calls, no token/time-saving claim.

The execution-route review preceding this fix also distinguishes the guest MCP
rejection from the separate ordinary integration runner. Integration07's launcher
retains execpolicy rules and does not call the guest tool. Local CLI0.157.1 reports
ChatGPT authentication; that alone is not a fresh model-execution success. No model,
approval-mode change or blocked guest retry occurred. Official documentation defines
[approval policy and per-server MCP tool modes](https://learn.chatgpt.com/docs/config-file/config-reference)
separately; the prior guest rejection is not evidence that every model route is
unavailable. It remains documented in SOLVER-EXECUTION-ENVIRONMENT-REQUEST-01.md.

한국어: Friday가 무한대를 포함한 SQL 결과를 성공으로 출력해도 JavaScript가
JSON으로 읽지 못하던 문제를 수정했다. 비유한 float는 명시적인 태그로 전달하고
네이티브 값·일반 숫자·문자열·BLOB·실패 근거는 보존한다. 수정 전4개 오류에서
새5개 검사가 통과했고 실제 JS 파서도 실패→통과했다. 누락 fixture가 있던 최초
복사 검사2개 오류도 보존하며 완전한 Git 없는 사본에서는63개가 통과했다.
모델 호출0회이며 전체8개 토큰·시간 개선으로 주장하지 않는다.

## Installed and packaged delivery

Source `c9b30fc6` is installed after all prior Friday bytes/modes match parent
`371b4b1e`, with the previous directory backed up outside skill discovery.
[All eight installed skills match](results/friday-json-numbers01/installation.json);
[the same five installed-source tests](results/friday-json-numbers01/installed.txt),
[four package tests](results/friday-json-numbers01/package.txt) and
[27 landing/server tests](results/friday-json-numbers01/landing.txt) pass.
The 151-file build check passes; only archive/checksum change in landing output.
[All52 packaged resource bytes/modes match source](results/friday-json-numbers01/download.json).
These checks are installation/packaging evidence, not new model measurements.

## Public delivery

Hosted revision `b528b7853b786e2a63bf1695edbb498b986de64d` is verified on
[한국어](https://hires.no-money-do-you-have-money.com/ko/) and
[English](https://hires.no-money-do-you-have-money.com/en/).
[Eight HTTPS observations](results/friday-json-numbers01/public.json) match the
release's health identity, both locale pages, JavaScript/styles/content and exact
archive/checksum. All52 public packaged resources match source bytes/modes.
Download108,336bytes, SHA256
`540c5f035f4c35f008163cfcf16895872157827c6265520fd4aa99eb8e26a338`.
Canonical/indexable metadata and frozen integration07 figures remain unchanged.
No new browser interaction or model-cost result is claimed; GitHub was not pushed.

한국어: 공개 배포b528b785의 HTTPS8개 경로와 다운로드52개 리소스 일치를 확인했다.
설치본과 공개 다운로드에 수정이 반영됐으며 실험 수치나 전체 목표 달성으로
바꾸지 않는다. GitHub 저장소에는 푸시하지 않았다.
