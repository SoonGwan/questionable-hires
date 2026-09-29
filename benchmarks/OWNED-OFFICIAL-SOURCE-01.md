# Owned official source01 — matching bytes, different modes and HEAD

Dated checkpoint **2026-09-27**, first protocol`065760ad`, prospective direct
comparison`fcadd5a8`, parent`8408c8fd`.
[Protocol](OWNED-OFFICIAL-SOURCE-01-PROTOCOL.md),
[original first outcome](results/owned-official-source-01/first-result.json),
[original direct-comparison collector outcome](results/owned-official-source-01/result.json),
[recovered original native observation](results/owned-official-source-01/recovered-result.json).
Zero model turns and selected-case tests;8skills and featured measurements unchanged.

## Authoritative observed identity

Actual image Git at `/usr/bin/git` runs natively via guest binfmt, cwd `/testbed`,
command-scoped safe.directory and GIT_OPTIONAL_LOCKS=0, without global configuration.
HEAD is **6868056bccd4882f25aa14acc1d76b6eb57c397f**, different from selected base
**0be38a0c37c59c4b66ce908731da15b401655113** and environment-setup commit
**bf436ea0a49513bd4e49bb2d1645bd770e470d75**. Working/cached diff-quiet,
rev-parse and ls-files calls all return0 with empty stderr. All132 regular tracked
entries exactly match their **own indexed Git blob bytes and executable modes**;
no missing/unmerged/unsupported or blob/mode mismatch entries. First VM5.425s.
This alone establishes internal coherence, not selected-base identity.

The original selected-base archive SHA256
`f91bf0c1463f0e1349c0c2aa8c0d547412694d0bd87870e774a582410cb9e7fc`
was rechecked, without extraction. Its132 file names/modes/content hashes were
held only in a private readonly comparison table; no path list or body published.
[Archive identity](results/owned-official-source-01/base-archive-identity.json).
Direct native comparison in the unchanged image gives:

| Compared to selected-base archive | Count |
| --- | ---: |
| Missing or extra paths | 0 / 0 |
| File-content SHA256 differences | **0** |
| Git executable-mode differences | **129** |

Thus **all132 selected-base file contents match**; identity differences are
executable modes and HEAD. The mode-sensitive archive/image aggregate hashes
remain different (`393d6976…`/`26402ce4…`). Do not claim whole-tree mode/Git history
parity or label this a different implementation. Synthetic history and preparation
chmod are plausible explanations, **not established causes**; no history body was
read to assert them. No source reset/repair, layer reapplication or test patch used.

## Original criterion failures and collector recovery

First strict expected-HEAD gate fails, controller1/VM0, and remains failed.
Before the second native observation, the archive/mode comparison was frozen as
a separate prospective intervention. Second VM4.927s successfully records the
actual direct comparison; Pythondriver0 and guest stop. The author's collector
looked only for JSON starting with `checkpoint`; sorted JSON now starts with
`base_comparison`, so it omitted the native observation and exits1. That original
collector result/source/log is preserved, not silently replaced.

The [recovery](results/owned-official-source-01/recover.py) checks the exact original
raw-console digest and parses the original JSON semantically by checkpoint.
It writes a **separate derivative** with explicit collector_recovery_only,
original_result hash,0replayed native processes/models and recovered counts.
Both strict HEAD and mode gates remain failed; byte equality is a separately
observed scoped fact, not retroactive grading success. No third VM/retest/rescore.
Raw original console stays private; outputs contain scalar/opaque identities only.
The private comparison map itself is not exported;
[map identity](results/owned-official-source-01/private-input-identity.json).

## Boundaries and next official-case preparation

The [native probe](results/owned-official-source-01/fixture/probe.py) hashes
regular bytes/link targets with Git blob framing and mode checks. Path names,
source/test/gold/history bodies and labels are never printed. Actual Git commands
have15-second timeouts; VM180-second deadline, independent parent200-second
watchdog and owned process-group cleanup. Root/probe shares readonly, guest-only
proc/dev/tmp and binfmt;1CPU/1GiB,no NIC/block devices. Both VMs stop normally;
owned root volume is detached after collection.

Selected source **bytes** are now supported, with explicit mode/HEAD limits.
Untracked/generated files, environment prep, HTTP/TLS services, exact official
scripts/parsers/FAIL-PASS grading, ownership/capabilities and amd64 kernel parity
remain distinct gates. Solver source isolation must preserve these resource choices
and keep private evaluation data out. No model work/token/time comparison or all8
release claim follows from this source audit. Existing adverse cost results stand.

한국어: 공식 이미지의132개 파일 내용은 고정 원본 아카이브와 모두 같지만,
129개 실행 권한과 Git HEAD가 다르다. 내부 Git 일관성은 확인했고 소스 내용
불일치로 단정하지 않는다. 첫 HEAD 기준 실패·후속 권한 차이·출력 수집 오류를
보존했으며 원본 로그에서 결과만 복구했다. 공식 과제·모델 재실행은0회다.
