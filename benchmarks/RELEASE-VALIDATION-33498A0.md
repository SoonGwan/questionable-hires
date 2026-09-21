# Offline compatibility checkpoint — 2026-09-21

Source: `33498a045617e41f89ae21ec5c7d1de36089ff50`. This is local
release-compatibility evidence, not a model-performance experiment or hosted CI.

| Environment | Python | Discovered | Passed | Skipped | Failed |
| --- | --- | ---: | ---: | ---: | ---: |
| macOS Git checkout | 3.11.16 | 1,079 | 1,079 | 0 | 0 |
| macOS fresh source archive | 3.11.16 | 1,079 | 1,056 | 23 | 0 |
| Offline Linux arm64 source archive | 3.12.3 | 1,079 | 1,056 | 23 | 0 |

Each command was `python -B -m unittest discover -s tests`; Linux additionally
used `-v`. All three processes exited 0. macOS checkout/archive terminal
summaries reported 194.340s/181.685s; their execution overlapped. Linux reported
76.849s. These are test-run durations, **not comparative speed measurements**.
Complete macOS stdout was not retained as a repository artifact.

## Retained Linux evidence and setup

- [Complete suite log](results/release-validation-33498a0/linux-suite.txt)
- [Container identity, timestamps, exit status and log digest](results/release-validation-33498a0/linux-runtime.json)

The existing image `questionable-hires/browser-codex:0.153.4-pw1.63.0` ran with
`--network none`. Its immutable image ID is retained in the runtime record.
The source archive and existing pytest/PyYAML resources were mounted read-only
and copied into the disposable container's filesystem. No packages were
downloaded, host dependencies installed, or account settings changed.
The working copy had neither `.git` nor `benchmarks/local-runs` before testing.
Python 3.12.3, pytest 8.3.4, PyYAML 6.0.3, Node 24.20.0 and ripgrep 15.2.0
were available. Repository validation and featured-document synchronization
checks also passed before the Linux suite.

All 23 Linux skips explicitly require project-owned historical resources;
synthetic scheduling and archived-fixture controls still execute. They are not
23 passing historical comparisons. The macOS archive summary also reports 23
skips, but its non-verbose output does not independently retain their names.
Expected negative-control diagnostics inside the log are not suite failures.
An evidence pattern scan found no matches; this is not a security certification.

## Decision and remaining limits

The [archive correction](ANCESTRY-ARCHIVE-01.md) now has a complete-suite check
on both platforms, not just the affected scheduling tests. Keep the correction.
No skill instructions, frozen model observations or featured chart values
changed. This does not establish automatic skill activation, remote installation,
independent usefulness, a 20–30% efficiency gain, or successful hosted checks.
The previously documented hosted billing restriction is a separate issue; this
offline run neither rechecks nor resolves it.

한국어: macOS 작업본 전체 1,079개가 통과했고, Git 이력이 없는 배포 압축본은
macOS와 Linux에서 각각 1,056개 통과·23개 건너뜀으로 끝났다. Linux에서 건너뛴
항목은 프로젝트의 과거 Git 자료가 필요한 비교다. 배포본 호환성 확인이며,
스킬 성능 향상이나 원격 CI 성공을 뜻하지 않는다. 그래프 수치는 변경하지 않았다.
