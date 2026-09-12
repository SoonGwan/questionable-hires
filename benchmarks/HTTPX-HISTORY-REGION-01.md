# Region-first HTTPX review: promising single pair, not causal acceptance

Two fresh Astra medium sessions followed the [frozen protocol](HTTPX-HISTORY-REGION-PROTOCOL.md)
at repository snapshot `908c5e5`, skill then baseline, serial, one repeat, no
retries or exclusions. Both use independent full copies of HTTPX
`26d48e0634e6ee9cdc0533996db289ce4b430177`, including its shallow Git history.
Raw ignored evidence: `local-runs/httpx-history-region-01`. The protocol's task
section alone, not its author assessment, is supplied to both arms. `run_cell`
records the exact prompt and metadata in each cell; no separate run.json was
generated for this direct invocation.

| Arm | Input + output tokens, cache included | Seconds |
| --- | ---: | ---: |
| No skill | 167,956 | 98.700 |
| Necromancer | 104,842 | 70.738 |

Observed reductions are 37.6% tokens and 28.3% time. This is a new development
task, not independent confirmation, and the baseline's failed first reproduction
and broader successful check confound causal attribution. Do not extrapolate to
the eight-skill objective or replace the original adverse comparison chart.

## Actual outcome and surrounding context

Both correctly retain the early return. The actual public Response path filters
empty incoming strings, but a nonempty carriage-return chunk becomes empty
inside `LineDecoder.decode` when trailing CR is deferred. Removing only the guard
then raises IndexError at the subsequent last-character access. This requires
reading surrounding state transformation, not trusting the adjacent comment or
looking only at the return statement.

Both construct an in-memory AST variant removing the single guard, execute real
sync and async Response line iteration, retain the ordinary control, and reproduce
standalone CR and split-CRLF failures. Skill asserts 16 comparisons across four
inputs: ordinary, empty, CR-only, and split CRLF. Baseline asserts 20 across five
inputs, adding joined CRLF as a passing control. Baseline also instruments decoder
entry state to assert all actual incoming strings are nonempty and checks the
exception source line. Skill prints actual iter_text outputs instead. Both meet
the fixed request, but verification depth is not identical.

Both distinguish current necessity from unavailable historical reason. The
version snapshot is a shallow boundary, not proof of the introducing change;
neither fetches missing history or invents author intent. Both reproduce the
disclosed missing-chardet collection failure and label standalone checks separately
from the unavailable upstream suite. No dependency installation occurs.

## Investigation and failures

Skill begins with symbol searches and reads decoder/chunker and sync/async caller
regions, rather than whole files. It uses line-range blame. It still performs a
parent lookup and pickaxe after detecting the shallow boundary: focused reading
does not eliminate all redundant history work. Four completed shell commands.

Baseline reads wider regions spilling into unrelated cookie logic, guesses a
nonexistent test path, and reads full project configuration. It also starts with
a too-long blame range. Its first in-memory experiment has a SyntaxError and
does not execute; the corrected experiment succeeds. Nine completed shell
commands. All failed attempts remain in costs and evidence, with no cell rerun.
Do not explain savings solely through command count or the instruction change.
Neither arm invokes the optional history collector; no collector benefit follows.

## Integrity and capture

All 125 original tracked files in each retained project match the clean source
checkout byte-for-byte, and final diffs are empty. The skill's four installed
resource instances match the frozen Git blobs and before/after inventories.
Both sessions complete with exit zero, no timeout and no rejected patches.
Inspected commands remain inside project scope, with only in-memory mutations.

Skill capture diagnostics are clear. Baseline has one empty-output item combining
parent-object existence, diff and status checks; a subsequent nonempty cat-file
error confirms the parent object is absent. Do not assume the earlier empty
capture fully preserved stderr or every subcommand status. The decisive 20-check
runtime output is present, including the initial failed experiment separately.
No author replay is credited as model evidence. Clean final files cannot establish
all transient behavior, nor do diagnostic flags prove full capture.

Retain the region-first candidate with this positive but limited transfer result.
It preserved necessary surrounding context in this task and used less observed
cost, but one pair with unequal work and a baseline repair does not establish a
stable causal advantage. No new safety checklist or forced helper is warranted.
