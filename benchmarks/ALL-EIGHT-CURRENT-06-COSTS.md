# Integration06 cost checkpoint — 2026-09-27

Measured skill resource **`1d0e92ac`**, execution **`35342e9c`**. [Frozen protocol](ALL-EIGHT-CURRENT-06-PROTOCOL.md).
All 16 scheduled fresh serial sessions completed without timeout, account limit or replacement.
[All attempts](results/all-eight-current-06/comparison.json), [per-response arithmetic](results/all-eight-current-06/input-cost-analysis.json),
and [actual model/resource audit](results/all-eight-current-06/capture-and-resource-audit.json) retain their measured identities.
Original response counters reconcile with final CLI usage in every cell. Cached input is counted once; reasoning is not added again.

**Cost arithmetic is reviewed; original outcome/scope/preservation review remains pending.**
A completed CLI turn is not a passing task. These are reused exposed development
controls, n=1 per arm, fixed alternating order, shared host/cache and unequal extra work.
The host execution retains normal rules; it does not resolve the separate guest MCP authorization boundary.

| Task | Baseline tokens | Current tokens | Baseline seconds | Current seconds |
| --- | ---: | ---: | ---: | ---: |
| history-invoice-boundary | 84,828 | 84,678 | 81.134 | 64.176 |
| ledger-delivery-b | 68,363 | 96,105 | 79.219 | 47.167 |
| store-check-scope | 60,738 | 77,520 | 35.947 | 37.762 |
| editor-snapshot-present | 62,297 | 83,026 | 53.479 | 54.128 |
| runner-environment-timing | 76,104 | 63,945 | 52.593 | 63.193 |
| refresh-owner-a | 82,888 | 122,523 | 104.484 | 105.771 |
| sqlite-commit-audit | 81,573 | 86,364 | 76.975 | 72.767 |
| view-contract | 64,534 | 65,697 | 87.338 | 69.099 |
| Sum | 581,325 | 679,858 | 571.169 | 514.063 |

Summed tokens **+16.95%**, summed CLI elapsed **−10.00%**. Two pairs use fewer
tokens; four are faster; only the history pair decreases both (tokens by just150).
That single observation is not a reliable general improvement. All-eight cost and
quality objectives remain unmet. Historical integration05 is not a contemporaneous
third arm, and these values do not measure subsequently modified resources.

Receipt originally requested optional argument observation. Path-valued setup
assertions made that observation incomplete despite retained native test failures;
the model reran the comparison with observation disabled. Both attempts and costs
remain included. The [path candidate](RECEIPT-PATH-OBSERVATION-01.md) has separate
native controls; it is not included in this model measurement or adopted as a
demonstrated token optimization. Interpreter failures and all other recovery remain charged.

The [original exports](results/all-eight-current-06/run.json) retain public task
artifacts and CLI tool events; private initial contexts/session files are not published.
Known private-path/credential-pattern scans passed, not a universal privacy guarantee.
Capture diagnostics are review candidates, not proof of completeness. No featured
benchmark, historical plot or hosted metric is relabeled by this checkpoint.

한국어: 현재 리소스1d0e92ac의16회 원본을 대조한 합계는 토큰581,325→679,858
(+16.95%), 실행 시간571.169→514.063초(−10.00%)다. 토큰 감소2개, 시간 감소4개,
동시 감소1개이며 그 토큰 차이는150뿐이다. 원본 품질·범위·보존 검토는 진행 전이므로
전체 통과나 일반 효율 개선으로 주장하지 않는다. Path 기록 실패 후 재실행을 포함한
모든 비용을 보존한다. 후보 네이티브 검사는 별도이며 랜딩의 과거 수치를 덮어쓰지 않는다.
