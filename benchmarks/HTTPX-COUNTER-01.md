# Counter audit: native routing adopted, efficiency regressed

Two fresh Astra medium sessions at snapshot `150fa4f` followed the
[protocol](HTTPX-COUNTER-PROTOCOL.md): baseline then skill, one repeat, serial,
no retries/exclusions. Complete independent HTTPX copies use upstream
`26d48e0634e6ee9cdc0533996db289ce4b430177`. Raw ignored evidence:
`local-runs/httpx-counter-01`; each cell records its exact prompt and metadata.
Direct run_cell invocation did not generate a separate run.json.

| Arm | Total tokens (input including cache + output) | Seconds |
| --- | ---: | ---: |
| Baseline | 102,472 | 53.948 |
| Con Artist | 136,550 | 60.077 |

Skill costs **33.3% more tokens / 11.4% more time**. One sample, different
verification depth and an experimental setup failure prevent causal attribution.
Do not present native routing adoption as performance acceptance.

## Original evidence

Both independently select the same reachable fault: replace synchronous
`Response.iter_raw`'s counter accumulation with assignment of the current chunk's
length. Both run the real existing pytest assertions, verify a passing original,
and identify the counter assertion failing on the second chunk: `6 == 6 - 7`
instead of a cumulative total of 13. Neither mistakes a setup error for sensitivity
or adds unnecessary stronger tests after this fault is detected.

Baseline makes a project-local disposable directory containing package, tests and
configuration, checks the imported package path, then runs five relevant tests
on correct and mutated code. Correct: five pass. Mutant: one fails, four pass.
The copy is mutated between runs rather than recreated; no effect of prior test
side effects is demonstrated. It leaves the copy, two logs and mutation diff,
and uses subprocesses without explicit local timeouts. Four shell commands.

Skill reads neither helper reference nor helper source. It runs two relevant
tests on current code, then extracts the actual method and replaces only the
counter expression in memory, verifies the local class binding and uses pytest
on the same two tests. Its first extracted-function compilation fails on Python
3.9 union annotations: the original module's future-annotations setting was not
preserved. No tests execute in that attempt. A subsequent corrected experiment
adds the setting, executes the real tests and restores the method afterward.
Correct: two pass. Mutant: one fails, one passes. Six shell commands. All attempted
work remains in cost; no cell retry or excluded result.

The author encountered the same compilation-context issue during preflight and
recorded it before model execution. That assessment section was not supplied to
either arm. This supports a concrete risk of extracted-function experiments,
not a claim that an optional helper or file-copy approach always performs better.

## Environment and integrity

The dedicated temporary venv gained only upstream-pinned `chardet==5.2.0`, with
--no-deps, before either session; the earlier collection failure and author
correction remain in the protocol. Both arms share this prepared environment.
Older reports retain their original missing-dependency limitations. No model
installs dependencies or performs network work.

All 125 original tracked files in each retained project match source bytes. The
skill's five installed resources match frozen Git blobs and before/after
inventories. Both complete with exit zero, no timeout, patch rejection or capture
diagnostic flags. Inspected commands remain within project scope. Baseline's new
diagnostic copy/logs are retained, not confused with changed original files.
Skill leaves no diagnostic files. The runtime failures and successes are present
in original logs, not substituted author replays. Final equality cannot establish
all transient actions; clear flags do not prove full capture.

Retain as adverse transfer evidence. The routing candidate successfully avoided
helper-reading overhead but created a compilation-context repair and still cost
more with fewer tests. Native isolation alone does not solve the efficiency
problem. The next change must account for the semantic context of extracted code,
without forcing one isolation strategy or repeatedly scoring this exposed task.
The broad eight-skill objective remains unmet.
