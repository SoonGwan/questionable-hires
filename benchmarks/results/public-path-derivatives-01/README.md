# Reviewed path derivatives01 — not original evidence

2026-09-22; source revision `f4e3ca8`. These eight files are explicitly labeled
path-redacted derivatives of the files listed in [manifest.json](manifest.json).
They are for reading, not replay inputs, executable commands or replacements for
the original hash-bound benchmark records. No benchmark is rerun or rescored.

Generation uses the existing `benchmarks/export.py:redact_paths` on each complete
UTF-8 source. The manifest records the exporter hash and each original/derivative
SHA-256 and size. Original bytes were checked against the named Git revision
before generation and against the working files afterward. Original files and
reachable history were not edited. JSON/JSONL parsing, object keys/order, list
lengths and all non-string scalar values are unchanged; redaction is idempotent.
Original hashes inside records remain original identities, not derivative hashes.
Placeholders are not executable paths or proof that two account roots match.

## Included scope

Five authored replay/preflight JSON files contain the previously identified26
owner-home lines. Three app-server artifacts contain account-directory UUIDs.
The known owner prefix and `/codex-accounts/<UUID>/` pattern are absent from
these derivatives. The exporter also replaces matching temporary path shapes.
The exact source paths are preserved as the derivative subdirectory layout.

The existing broad scanner still flags12 lines in the three app-server files.
Every flagged occurrence begins with the literal `/home` suffix immediately
after `/codex-accounts/<ACCOUNT>` in an already-redacted path. These are **not**
new unredacted home roots. This classification was checked for every match;
the scanner itself was not weakened and its nonzero result is retained here.
No credential/header matches were reported for this derivative directory.

## Remaining boundary

Creating these copies does **not** remove owner paths or identifiers from the
original files, current tree or Git history. A public clone would still include
those originals/history if repository visibility changed now. The wider284-line
history review, other artifact categories and owner disposition remain open.
This directory is not clearance for public release or a secrets-free certificate.
Do not repoint frozen fixtures/runners at these files or overwrite their originals.

한국어: 작성자 경로가 있던 자료5개와 계정 폴더 식별자가 있던 자료3개의 별도
비식별화 사본이다. 원본·수치·Git 이력은 수정하지 않았다. 검사에 남은12줄은
이미 가린 계정 경로 뒤의 `/home` 문자열임을 전부 확인했다. 기존 저장소를
공개하면 원본과 이력은 여전히 노출되므로 공개 승인이나 정리 완료가 아니다.
