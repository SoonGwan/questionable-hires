# Decision-gate transfer to actual packaging cleanup

Use one real-source task, exported by `packaging_review_cases.py` from
questionable-hires `436e409`. Source and original tests are unchanged; README
setup is explicitly authored for evaluation. This is the project's own code,
previously exposed during packaging development, not an independent held-out
repository. The export contains a snapshot commit, not upstream ancestry.

The user asks whether the copying exception handler can be removed while
preserving behavior. Neither prompt nor README supplies the intended decision.
Criteria stay outside the evaluated workspace. Source skills are packaging data;
only the invoked installed skill may supply instructions.

Before model execution, freeze both exporter scripts and this protocol at one
commit and record the generated JSON digest. Export all Necromancer resources
from predecessor `8844685` and candidate `0143ef2`, preserving modes and recording
each file's SHA-256. Use fresh serial Astra medium sessions, one per condition,
240-second cell timeout, seed 20260911, no retries or exclusions. Schedule:
candidate, no-skill baseline, predecessor. Exactly three sessions on one task.
Use `run.py --cases-file <generated.json> --case packaging-cleanup-review
--jobs 1 --repeats 1 --model gpt-6-astra --effort medium --timeout 240
--seed 20260911`, with separate new outputs and frozen `--skills-root` for the
two `--arms skill` conditions; the baseline uses `--arms baseline`.

Compare supported recommendations, actual cleanup/removal evidence, successful
bundle behavior, existing-destination preservation and error semantics before
resource costs. A correct static guess alone does not meet the verification
request. Never infer historical intent from the synthetic snapshot commit. Missing
upstream history is a limitation, not a reason to fetch or claim a false origin.
Record additional probes, history lookups and different tested failure modes as
unequal work. Stop scheduling on an account limit or incomplete orchestration.

Author preflight ran the five original build tests successfully. It then removed
only the outer copying try/except using an AST transformation in a fresh process,
left its copying body and exclusive directory creation intact, and ran the same
tests. Three failure-type subtests fail because the partial destination remains;
the five-test run has exactly three failures and no errors. All supplied files
remain byte-identical. This is author fixture evidence, not model execution or a
model performance improvement.

This transfers from a dictionary fallback to filesystem failure cleanup, but
cannot prove broad efficiency or estimate the gate's benefit on rich history:
the review is one exposed project snapshot, one repeat, shared host/cache and
possibly unequal work. Retain all results, including a slower candidate. No
superiority graphic or release claim follows from this screen alone.
