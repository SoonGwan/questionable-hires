# Local candidate validation — 2026-09-27, source `6c099d68`

This validates the native-single route candidate, not the later benchmark runner
files or model efficiency. Same macOS host, Python3.11.6 in the local validation
environment; no new dependency downloads for these checks.

| Source form | Test result | Native elapsed | Original local log SHA-256 |
| --- | --- | ---: | --- |
| Git checkout |1,239 discovered,17 skipped,zero failures,exit0 |193.832s |`279d1ec47201ac7099d9609fe7694fdfe18687120d7f4c8d5f65acd6fbb7004e` |
| Pinned Git source archive |1,227 discovered,51 skipped,zero failures,exit0 |169.258s |`3e488fef38fb8d1d7400eea812db965d1642a5ec494826aba09a2e4a6490ab00` |

Both used `python -B -m unittest discover -s tests -q`. Original logs remain
local; SHA identities retain provenance without publishing unreviewed path-shaped
output. Counts include skips, not all passes. Archive has no Git history; skips
and different discovered counts are not silently counted as current coverage.
The native single recipe's dedicated4 and native-module17 checks pass without
skips. Complete discovered-suite results do not prove every external environment.
The two local runs partly overlap; their times are not a performance comparison.

Archive bytes SHA-256:
`e9fb34ce05b71422cb5f66cae64c97fb3dd1ce68f00397a20b35d9559433091c`.
Extraction checked relative paths and only regular-file/directory entries, into
a dedicated empty temporary directory. No repository files were overwritten.

Actual local installer copy/check completes:8 skills,51 installable files, exact
pinned `6c099d68` bytes and modes, no extra installed files. Catalog README is
not an installable skill resource. This is the project's local installer, not a
fresh remote CLI install, active user registration or model-selection evidence.
Installed-script/behavior checks at this resource remain separate unfinished work.

Catalog, documented links, Skill Creator metadata, whitespace and featured
synchronization checks pass. No featured cell or chart changed. No hosted CI,
Linux/Python matrix, anonymous remote installation or whole-task efficiency
claim is made. [Measured adverse screen](ASSERTION-CONTRACT-01-REVIEW.md) remains
at `33530f98`; the new native-split02 model comparison is still underway.

한국어: 해당 후보의 로컬 체크아웃·소스 아카이브 검사는 실패 없이 끝났지만
각17·51개는 건너뛰었다. 8개 스킬51개 파일의 실제 로컬 설치 일치도 확인했다.
다른 OS/런타임·원격 설치·모델 성능 개선까지 검증됐다는 뜻은 아니다.
