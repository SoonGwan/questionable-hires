# Requests environment diagnosis: runner compatibility is one cause

2026-09-21, parent`6eeafe4`. Follow-up to the
[internal-service preflight](SWE-LITE-PILOT-01-SERVICES.md), not a model run.
Uses only the original public Requests tests, without the gold or test patch.

## Reproduction in the base-only source image

With the internal HTTP service and `HTTPBIN_URL=http://httpbin/`, execute the
complete original `test_requests.py` under the image's pytest7.4.4. Native result:
**134passed /8failed**,22warnings,9.52s,exit1. This is a different test set from
the hidden scoring groups; do not merge their counts or treat it as a replacement.
[Original output and command](results/swe-lite-pilot-01-requests-diagnosis/qh-swelite-requests-native-services-01.txt)
show these distinct failure mechanisms:

- Redirect-off-host uses a hostname not resolved on this internal network.
- `test_conflicting_post_params` calls `pytest.raises` with source strings;
  pytest7 rejects them as noncallable, before the intended exception assertion.
- Mixed-case HTTPS, pyOpenSSL redirect, request history and stream-timeout checks
  require HTTPS service/hostname behavior absent from the HTTP-only setup.
- Connect/total-timeout checks target`10.255.255.1` but get immediate network
  unreachability, not the deliberately slow connection expected by those tests.

This evidence supports more than a blanket TLS explanation. Do not change test
expectations, use catch-all passing mocks, disable certificate verification or
skip failures to satisfy the benchmark.

## Narrow runner repair, actually tested

The [official pytest removal note](https://docs.pytest.org/en/7.2.x/deprecations.html#raises-warns-with-a-string-as-the-second-argument)
documents removal of the string form in5.0. In a fresh Requests-only container,
install pytest4.6.11 and an explicit compatible dependency set from local wheels:
pluggy0.13.1, atomicwrites1.4.1, py1.11.0, six1.17.0, attrs23.2.0,
more-itertools9.1.0, packaging24.2 and wcwidth0.2.13.
[Exact installed wheel hashes](results/swe-lite-pilot-01-requests-diagnosis/installed-wheel-hashes.json)
are retained. Atomicwrites' universal wheel was built locally from its1.4.1 source
distribution; other installed artifacts are downloaded wheels. An initial host
download also collected newer dependency versions, but explicit install pins did
not select those; they are not part of this validated environment.

All installation occurs inside a disposable, unmounted, network-disabled
container, not the user's Python environment or the separate pytest issue runtime.
The Requests source and tests are not rewritten. Docker's filesystem diff has no
`/testbed` entries afterward; this is an observed diff, not an atomic mutation audit.

[Actual compatibility run](results/swe-lite-pilot-01-requests-diagnosis/qh-swelite-requests-pytest-compat-01.txt):

- Unchanged `test_conflicting_post_params`:1passed,23warnings,2.10s,exit0.
- [Independent runner controls](results/swe-lite-pilot-01-requests-diagnosis/assertion-control.py):
  one true assertion passes, deliberate `7 == 9` fails with both values and
  `AssertionError`;1passed/1failed,0.11s,native exit1. The wrapper requires that
  expected failure code, so its final exit0 is not two passing tests.

This validates that narrow API repair on Python3.9.20, not the full Requests
suite, complete official grading or the source bug's resolution. The runtime
has not yet been promoted into either solver or gold scoring runs.

## Next environment work

Preserve the unchanged hostname/HTTPS and connection-timeout contracts in an
isolated service/network setup, then rerun all required scoring controls without
omission. Pin and verify the combined runtime before any baseline/skill sessions.
All diagnostic containers are terminal and the HTTP service was stopped again;
original images and the unrelated database container remain untouched.

한국어: 남은 실패는 HTTPS뿐 아니라 pytest의 옛 API 제거와 타임아웃용 네트워크
조건에도 있었다. Requests 전용 컨테이너의 실행기를 고정하니 원래 검사1개가
수정 없이 통과했고, 의도적인 실패도 제대로 검출했다. 전체 채점 환경은 아직
미완료이며 스킬 성능 수치나 그래프는 바꾸지 않는다.
