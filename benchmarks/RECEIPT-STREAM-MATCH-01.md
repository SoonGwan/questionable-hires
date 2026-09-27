# Receipt streaming comparison01 — isolated, 2026-09-28

Parent `71cdc0ab`; ordinary Receipt source and both measured resource hashes are
recorded in [source identities](results/receipt-stream-match-01/source-hashes.json).
[Candidate transform](receipt_stream_match_candidate.py). No model call or normal
skill change. This is a memory experiment, **not whole-task efficiency adoption**.

The existing selected-file preservation check allocates a second complete file
buffer before comparing it with captured original bytes. The prototype shares the
same descriptor-opening checks and compares exact bytes in at most64KiB chunks,
plus one byte for growth detection. It retains the later, separate whole-tree
inventory and the final mode check. No snapshot, source read or checksum is reused
across mutable observations; no test or required comparison is removed.

This differs from the rejected [guard I/O prototype](RECEIPT-GUARD-IO-01.md), which
merged two observations and missed an actual late mutation. The unchanged late
mutation regression still rejects the changed watched file with this prototype,
after one real before failure and one real after pass. The changed source is not
restored. Smaller buffer allocation does not justify removing that second read.

## Native results

[Three candidate controls](results/receipt-stream-match-01/archive-candidate-tests.txt)
pass in an isolated Git-free archive: exact equality, growth, truncation, last-byte
and chunk-boundary changes, empty input, bounded read counts, and opened-inode,
symlink and FIFO replacement rejection. The unchanged existing
[9 tree-guard tests](results/receipt-stream-match-01/archive-guard-tests.txt) also
pass there, including the late-mutation counterexample and actual native outcomes.
These 12 methods validate the scoped prototype, not all Receipt functionality or
model performance. The new controls also passed in the checkout.

[Author profile and all samples](results/receipt-stream-match-01/profile.json),
[profile source](results/receipt-stream-match-01/profile.py). Each condition uses
20 warmed untraced timings with alternating version order and three separate
Python-allocation measurements. Original expected bytes exist before tracing;
these are additional allocations for the final selected-file comparison only.
Neither process RSS, Git work, copying, tests, the full comparison nor model work
is timed here. Shared host and warmed file cache limit interpretation.

| Selected input / condition | Original median ms | Candidate median ms | Original peak allocation | Candidate peak allocation |
| --- | ---: | ---: | ---: | ---: |
|64KiB / equal|0.026|0.027|71,746|72,217|
|64KiB / last byte differs|0.021|0.021|71,746|72,193|
|64KiB / one extra byte|0.020|0.023|71,746|72,193|
|8MiB / equal|0.993|0.930|8,394,882|137,858|
|8MiB / last byte differs|1.066|0.949|8,394,882|137,858|
|8MiB / one extra byte|0.866|0.910|8,394,882|137,858|

All expected acceptance/rejection outcomes match and file bytes remain unchanged.
Large-file temporary allocation decreases; small-file allocation slightly grows.
Timing is mixed, with absolute differences below1ms. No whole-agent token/time
claim follows, and an expensive model rerun is not justified by these timings.

Keep the prototype isolated. It may be relevant to an observed large-file memory
constraint, but that is not the demonstrated cause of current model-token cost.
Before integration it still needs the remaining Receipt compatibility controls
and a concrete consumer benefit. Do not repeat this profile to fish for a uniformly
favorable time result. Installed skills, hosted downloads, README cost claims and
featured benchmark remain unchanged.

한국어: 원본 보존 검사의 두 번 읽기를 유지하면서 마지막 바이트 비교만 블록화한
시제품이다. Git 없는 복사본의12개 검사와 기존 늦은 변경 반례를 통과했다.
8MiB 파일의 해당 단계 추가 메모리는 약8.39MB에서0.14MB로 줄지만 작은 파일은
조금 늘고 시간도 혼재하며 차이는1ms 미만이다. 전체 작업·모델 토큰 절감의 근거가
아니므로 기본 스킬에 반영하거나 같은 실험을 유리한 값이 나올 때까지 반복하지 않는다.

Author reporting correction: an intermediate progress message said18 tests using a historical guard count. The original logs show3 new plus9 existing methods,12 total; no18-test run is claimed.
