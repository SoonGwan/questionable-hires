# Bounded regression follow-up

One fresh skill execution at `4c327a9` on the unchanged authored upload case,
under ignored `local-runs/hostage-transfer-02`. No new baseline or repeated
matrix was run. This is development evidence following an observed defect,
not independent held-out confirmation.

The session completed with 89,371 total tokens (87,398 input including cache,
1,973 output) in 73.129 seconds. Previous skill: 105,630 tokens / 67.677 seconds.
Earlier baseline: 98,573 tokens / 49.588 seconds. Token reduction alone is not
an overall efficiency win: this sample is slower than both earlier samples.
Shared-host/cache conditions and single runs preclude causal claims.

The production fix is unchanged. Existing test methods were compared by AST
and preserved; requirements and branding were byte-for-byte preserved.
Recorded discovery stayed within the project. The generated unittest suite
reuses the original client through a blocking test subclass and adds bounded
overlap and cancellation/retry checks, with controlled task cleanup.

Independent isolated replay verified copied imports and all four tests passed.
Removing only the duplicate guard made the overlap test raise its local
`asyncio.TimeoutError`; the suite completed in 1.039 seconds, exit 1, without
the audit's three-second process timeout. The preceding skill result hung
until that process timeout. This verifies that particular generated regression
now terminates on that particular fault, not that every possible async fault
is bounded or that the skill universally outperforms baseline.

Reproduce against either retained project with the exact-match recipe:

```sh
python3 skills/con-artist/scripts/audit.py --spec benchmarks/hostage-duplicate-audit.json --source benchmarks/local-runs/hostage-transfer-02/upload-existing-tests--skill--1/project --timeout 3
```

No additional skill rule was added after this result. The next useful step is
broader workload evidence or a structural cost reduction, not repeated draws
of this same case until a favorable time appears.
