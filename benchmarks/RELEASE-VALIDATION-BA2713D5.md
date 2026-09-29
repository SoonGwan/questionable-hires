# Local validation — 2026-09-27, source `ba2713d5`

[Recorded summary](results/release-validation-ba2713d5/summary.json),
[installed behavior](results/release-validation-ba2713d5/installed-behavior.json).
This pinned source includes interpreter route01 and its scheduler, later evidence
analysis and bilingual landing copy. It is not a completed all-eight improvement
release. Model costs remain adverse/mixed at their original measured resources.

| Source form | Native suite | Exit | Local elapsed | Original log SHA256 |
| --- | --- | ---: | ---: | --- |
| Checkout |1,250 discovered,17 skipped,zero failures |0 |191.622s |`2ec58faa07e46dda73458d229e20520a06a8a5ccfa6a99672fec2e5ba625dce0` |
| Git-free source archive |1,250 discovered,47 skipped,zero failures |0 |175.118s |`142c41282ac5c3f56fbac1eb648d5b4a808d36a40227847e71423bcaabe81e77` |

Both execute python -B -m unittest discover -s tests -q on macOS26.5.2/arm64,
Python3.11.6 in the existing validation environment, without dependency downloads.
These elapsed values describe local checks, not a checkout/archive performance
comparison or model efficiency. Skips are not passes; no broader environment is
inferred. The archive has no .git and was extracted into an empty owned directory
after checking every entry is a relative regular file/directory without traversal.
Archive SHA256: `0fc53196f322cb62f974f48df7489abcb020512b99f3687528f724d6c07939a1`.
Original logs stay local; published metadata retains hashes without private paths.

Existing installation checker uses cached skills CLI1.5.18 in a disposable project,
never global registration. Eight skills/51 files match source bytes and modes,
nine Python entrypoints answer help, and25 actual command exits match expectations.
Installed Python/JavaScript callback assets execute; named-region success/missing
selection, native Receipt before1/after0, native Con Artist0/0/0/1 plus wrong-binding
incomplete7, and Exorcist child failure17/timeout124 with cleanup are verified.
Source and installed resources remain unchanged. This is local installer behavior,
not remote availability, anonymous access, independent model validation or the
meaning of every skill instruction. Full original installed observations are
retained as redacted derivatives; CLI/checker SHA identities appear in metadata.

Catalog/link and featured synchronization checks pass. No featured numbers or
charts change. Hosted CI, other Python/OS versions, public history and final
responsive/browser release checks remain distinct work. The all-eight quality,
lower whole-task tokens and faster completion objective remains unachieved.

한국어:고정 소스 ba2713d5의 macOS/Python3.11.6 전체 검사는 체크아웃1,250개·17개
건너뜀, 아카이브1,250개·47개 건너뜀으로 실패 없이 끝났다. 실제 로컬 CLI 설치는
8개 스킬51개 파일과 모드가 일치하고25개 명령의 종료·선택된 helper 동작을
확인했다. 건너뜀을 통과로 세거나 모델 성능·원격 설치·다른 플랫폼·최종 업데이트
완료로 확대하지 않는다.
