# Linux source-archive verification — 2026-09-15

Measured source: `73d27f5a7092fdd87f017002a62927aa6370951d`.
This is author-run compatibility verification, not model performance evidence.
No skill instructions, benchmark criteria or featured numbers changed.

## Environment and method

An unmodified `git archive` of the measured revision was mounted read-only and
copied into a disposable container's `/work`. Both `.git` and
`benchmarks/local-runs` were absent from that copy. The existing image was
`questionable-hires/browser-codex:0.153.4-pw1.63.0`, image ID
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`:
Linux arm64, Python 3.12.3, Node 24.20.0. Containers used `--network none` and
`--rm`; no downloads, host installations or account changes were made.
Existing PyYAML 6.0.3 files were mounted read-only at `/deps/yaml`, with
`PYTHONPATH=/deps`; Linux used the pure-Python fallback.

Each completed full run executed `scripts/validate.py`,
`scripts/sync_featured_benchmark.py --check`, and then
`python3 -B -m unittest discover -s tests -v`. Both preceding checks passed.

## Observations, including unsuccessful setup

| Setup | Result | Evidence |
| --- | --- | --- |
| Default image plus PyYAML | 655 discovered, 648 passed, 7 skipped; 37.592s; exit 0 | [Full log](results/linux-archive-655-01/suite-73d27f5.txt) |
| Existing pytest files staged without `py.py` | Import failed before tests: missing `py` shim | [Preflight](results/linux-archive-655-01/pytest-dependency-preflight.txt) |
| Shim restored, pytest on `PYTHONPATH` only | Three focused tests: two failures, one error; 0.077s; exit 1 | [Focused log](results/linux-archive-655-01/pytest-path-only-73d27f5.txt) |
| Same dependencies in container site-packages | 655 discovered, 651 passed, 4 skipped; 38.643s; exit 0 | [Full log](results/linux-archive-655-01/suite-pytest-73d27f5.txt) |

The path-only setup was insufficient: the audit child removes `PYTHONPATH`,
and the CLI isolation check uses `python -I`. Their isolation was not weakened.
Existing pytest 8.3.4, pluggy 1.6.0, iniconfig 2.1.0, packaging 26.3 and `py.py`
were instead copied from a read-only staging mount into the disposable
container's `/usr/local/lib/python3.12/dist-packages/`.
`python3 -I -c 'import pytest; print(pytest.__version__)'` confirmed 8.3.4
before the full run. This did not install packages on the host.

The four remaining skips were three comparisons requiring project-owned Git
history (not present in a source archive) and the Friday discovery check
requiring ripgrep on PATH. The initial seven also included three pytest tests;
those three actually passed in the site-packages full run.

A subsequent full run added the image's existing bundled ripgrep directory
`/opt/codex/packages/standalone/releases/0.153.4-aarch64-unknown-linux-musl/codex-path`
to container-only PATH. Its terminal result/log was not recovered after loss of
the observation handle; the disposable container was no longer running on
inspection. **Outcome unknown, not counted as passing and not rerun to replace
the missing observation.** Ripgrep was absent from default PATH, not necessarily
absent from the image. Thus this report does not claim all executable checks
passed in one fully provisioned run.

## Interpretation

The current Linux archive run passes the native Receipt checks that failed in
the earlier [619-test observation](LINUX-ARCHIVE-619-01.md). That historical
failure remains unchanged; this is a different source revision and test count.
Local Linux success is not a hosted GitHub Actions result: recent hosted jobs
were unavailable before step execution. It also does not establish model
adoption, token savings, or a broad 20–30% improvement across eight skills.

한국어: 현재 소스의 Linux 압축 배포본에서 655개 중 651개 통과·4개 생략을
확인했다. 생략은 Git 이력이 필요한 3개와 기본 PATH에 ripgrep이 없어 실행하지
못한 1개다. pytest 준비 과정의 실패와 마지막 추가 실행의 결과 미확인도 남긴다.
이 결과는 호환성 검증이며, 모델 성능 개선이나 호스팅 CI 통과를 뜻하지 않는다.
