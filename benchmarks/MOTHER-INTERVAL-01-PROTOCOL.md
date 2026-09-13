# Interval versus final-only QA checkpoint 01

The route comparison at `672e22f` exposed a real regression blind spot: generated
skill tests reported but did not assert older-completed/newer-pending display.
Unchanged-test author replay passed a transient display fault that baseline tests
rejected. Preserve that result; do not call the instruction change a proven fix.

Candidate changes the shared decision rule: a stated “retain while loading” /
“until latest completes” condition covers relevant intermediate completions within
the interval. Printed observations are not retained regression assertions. A
final-ownership-only contract still leaves unspecified intermediate display free,
so valid corrections must not be rejected for a permitted intermediate path.
Existing helper/asset code and delivery routes remain unchanged.

Freeze two unchanged exposed authored cases from bundle-contract-v2:
`search-protected` (retention requested) and `search-order` (final latest ownership,
explicitly permits retaining prior display while pending). All decoded source,
task and criteria objects are preserved, with no new model-visible hints or
retroactive obligations. Native preflight verifies original/guard behavior and
actual intended assertion failures, including the permissive normal-display path.

File: `mother-interval-cases.json`, SHA-256
`7984c2416962285e54c2c1139cecd01421620106cf7f901024c7ca709e62b131`.
Prelaunch: 43 targeted tests passed in 7.769s (exact case reuse, native bundle
preflights, controlled requests, probe behavior and installed helper execution).
Skill metadata, catalog/document links, featured-language synchronization and
whitespace checks pass. Not a new full-suite or hosted-CI result.

Four fresh serial Astra medium sessions, baseline/skill once per task, seed
20260914, 240-second limits. No resource/task edits or author tests during timing.
Preserve every scheduled attempt, timeout, missing output and scope deviation.
No retries/exclusions for desired results; stop scheduling on account limits.

Review actual component binding, required deliverable and normal/adverse native
assertions. After timing, replay unchanged tests without installed skills:
protected original versus the previously disclosed transient-retention fault;
unprotected original versus a valid guarded correction. These author checks test
both missing required assertions and invented constraints; they do not replace
native model evidence or establish performance. Preserve failed acceptance too.

Report all input+output (cached once), wall time, extra work and capture limits.
Two exposed authored tasks at n=1 are not independent confirmation, broad developer
transfer, all-eight success or a guaranteed percentage improvement. No automatic
featured-chart changes. Document adopted/ignored rules separately from savings.

```sh
python3 -B benchmarks/run.py --cases-file benchmarks/mother-interval-cases.json \
  --arms baseline skill --repeats 1 --jobs 1 --seed 20260914 --timeout 240 \
  --model gpt-6-astra --effort medium \
  --output benchmarks/local-runs/mother-interval-01
```
