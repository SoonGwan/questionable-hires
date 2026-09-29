# Python regions file01 — installed delivery check, 2026-09-27

Parent `8b1d8163`; [functional change](PYTHON-REGIONS-FILE-01.md).
[Actual installation/CLI evidence](results/python-regions-file-01-install/result.json),
[standalone archive member hashes/modes](results/python-regions-file-01-install/archive-contents.json).
Separate owned checkout and standalone-package consumers each install all8 skills
and52 actual resource files using the real installer. No existing personal/global
installation is changed; the archive has no project Git metadata.

In both consumers the actual installed Python excerpt script runs with `-I -B`,
accepts `--path source.py` and ignores intentionally invalid stdin. It extracts
C.f with original indentation, source hash and future-feature context. Top-level
source raises RuntimeError if executed, so a successful static selection verifies
that it was not run. Missing function returns incomplete with exit1; normal
selection returns complete with exit0. Actual installer `--check` passes afterward.
Installed helper bytes match current source; every installed resource hash/mode
and input file bytes/mode remain unchanged through both executions.

Standalone packaging is the real deterministic packager, with archive SHA and
all member identities retained. Setup/package/check/helper processes have30s
parent bounds. Installation is entirely under owned temporary consumer roots;
artifacts are preserved there. This is local delivery evidence, not a hosted
release check, actual model helper selection, measured tokens/time or all8 task
quality. Frozen adverse comparisons remain accessible; the overarching goal is
unmet. No public deployment or performance claim was made.

한국어: 체크아웃·독립 압축 패키지에서 실제 설치한 8개 스킬·52개 리소스를
확인했다. 설치본의 파일 입력 발췌는 정상0·없는 함수1을 반환하고 코드 실행 없이
원본과 설치 리소스를 보존했다. 실제 설치 검사가 통과했지만 로컬 배포 확인이며
모델 비용·전체8개 품질·호스팅 릴리스 검증은 아니다.
