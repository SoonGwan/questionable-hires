# Direct invocation works; overall efficiency does not

Frozen candidate/protocol 195a037, runner fd8d578. Unchanged exposed
search-diagnosis case, Astra medium, one fresh baseline/skill session each,
serial seed 20260911, 240-second limit. Baseline ran first. No retries or exclusions.
Raw original logs remain private in `local-runs/exorcist-direct-01/`.

| Arm | Input + output tokens | Process seconds | Completed shell commands |
| --- | ---: | ---: | ---: |
| baseline | 64,085 | 41.269 | 4 |
| skill | 87,552 | 57.394 | 6 |

Skill costs **36.6% more tokens and 39.1% more elapsed time**. Cached input is
already included in input tokens. This shared-host single pair is descriptive,
not causal measurement of the edit or evidence of generalization.

Both execute real Search and transport functions with a cache-free recording
request dependency, control both overlapping completion orders and reproduce
the stale overwrite. Both preserve search.py and transport.py byte-for-byte.
Baseline's final answer identifies response ordering, but does not explicitly
explain why no-cache cannot order responses or distinguish this reproduction
from every production incident. Skill supplies those qualifications and adds a
sequential normal control, explicit owned-task cleanup and a process deadline.
Work is therefore unequal; baseline has no process deadline in its retained probe.
Do not turn these additional safeguards into new mandatory task criteria.

Skill reads only its entrypoint, not the reference or helper implementation,
and invokes the installed runner successfully. This establishes direct-invocation
adoption in this sample, not a causal improvement over earlier independent runs.
The actual helper result is exit 0, no timeout, no output truncation. Skill saves
the full JSON to a new result file, then reads it back; baseline prints its compact
observations directly. Skill also splits repository discovery and reading the two
production files across more commands. These are concrete remaining work costs;
they do not prove all extra work was unnecessary or explain a fixed percentage.

Original captured commands stay inside each assigned project. All four installed
resource hashes match 195a037 and before/after manifests agree. Both original
production files in each retained project match the frozen case. No rejected
patches, malformed JSON or event errors. Skill's one empty command-output flag
is the successful command redirecting stdout to its result file; the subsequent
captured read contains that result. Grouped final shell statuses do not isolate
every subcommand; original-file preservation was independently checked by author
comparison, not inferred solely from the final shell exit. No author replay is
credited as model execution.

Nine runner tests, all 154 repository tests (17.321 seconds), repository validation
and skill validation pass. The entrypoint is shorter (499 to 391 whitespace words)
and direct use is observed, but whole-session performance remains worse in this
pair. Keep this as a candidate, not a performance release or a reason to repeat
the exposed case until a favorable sample appears.
