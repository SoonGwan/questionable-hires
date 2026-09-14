# Hostage read/review candidate 03 — 2026-09-15

Parent `e659f0e`; follows [refresh 02](HOSTAGE-REFRESH-02-REVIEW.md), where original
native evidence improved but sum tokens increased 58.57%. This document describes
a candidate, not another measured performance result.

## Changes supported by traces

- Known-file reads and status first; discover only missing paths, including hidden
  instruction files so an incomplete inventory does not trigger another pass.
- Executable `sed` examples read complete Python/JavaScript asset usage blocks.
  Trust review, adaptation and unclear behavior still justify implementation reads.
- Native tests remain dedicated commands. Combine remaining non-test integrity,
  diff and status checks, keeping needed exits. Do not reprint a generated suite
  solely to check its existence; inspect new code not visible in edit output.

No helper implementation, concurrency contract, assertion obligation, permission
boundary or missing-evidence recovery rule changed. This is not a universal ban
on discovery, code review or longer reads. Existing project support remains first.

## Local verification, not model savings

The entry changes from 4,130 to 4,146 bytes (+16); no entry-size reduction claim.
Actual excerpt commands return Python usage 2,382 of 5,388 bytes and JavaScript
usage 2,918 of 7,835 bytes. Python's AST confirms the complete module docstring
and no implementation; JavaScript output matches the complete opening comment.
Files are unchanged. These are byte counts, not model tokens or elapsed savings.

[Executable instruction check](../tests/test_hostage_usage_reads.py) extracts and
executes the shipped commands against actual assets, checking complete usage and
unchanged source. Existing 21 Python/JavaScript helper tests pass (0.651s), including
real owners, intentional faults, cleanup and standalone copies. Skill structure
validation passes. The executable instruction check passes (1 test / 0.007s),
and all 12 bundle tests pass (3.326s). Model uptake, extra-call reduction and whole-task savings
require prospective measurement; no chart is updated by these local checks.

## 한국어

실측에서 드러난 반복 탐색·도우미 전체 읽기·최종 점검 왕복을 줄이는 후보다.
사용법 전체를 읽는 명령을 제공하며 신뢰 검토나 수정이 필요하면 구현도 읽는다.
테스트는 별도 명령으로 유지하고 나머지 점검만 묶는다. 안내 자체는 16바이트
늘었으며, 읽을 수 있는 본문 감소를 모델 토큰 절감으로 주장하지 않는다.
기존 도우미 동작 테스트 21개와 구조 검사는 통과했고 실제 모델 개선은 미검증이다.
