# Citation workflow adopted, whole-session savings absent

Frozen protocol/resources `e373da0`, Landlord entrypoint `5f67c6e`. Unchanged
check-scope task; fresh baseline then skill, one each, serial Astra medium,
seed 20260911, 240-second timeout. No retries, exclusions or concurrent candidate
changes. Local originals: `local-runs/landlord-citation-01/`.

| Arm | Input + output tokens | Wall seconds | Completed shell calls |
| --- | ---: | ---: | ---: |
| Baseline | 65,137 | 32.502 | 5 |
| Skill | 84,952 | 35.652 | 5 |

Skill uses 30.42% more tokens and 9.69% more time. Baseline input/output is
64,418/719, skill 84,137/815; cached input 58,112/77,056 is already included.
Reasoning output is not added again. Single shared-host exposed samples do not
establish causal effects or general efficiency.

Skill reads the entrypoint in its initial discovery call, performs a second
file listing/status call, then reads all six project files once with line numbers.
It does not reread source solely for citations. Baseline reads project files,
then rereads four files with line numbers in a call also checking status.
The intended first-read behavior occurs, but total calls do not decrease: skill
has separate discovery instead. Do not infer that the extra discovery alone
caused the token difference or that retained locations save whole-session cost.

Both run the documented two-test local contract group and a separate in-memory
direct-Backend probe, with actual successful exits and captured outputs. Both
show creation yields None, duplicate raises Duplicate, original value survives
and OSError propagates. Baseline additionally checks exception object identity;
skill checks its type. Both recommend retaining semantic translation, describe
compatible inlining as moving the policy into service.save, and explain driver
coupling rather than treating fewer classes as lower maintenance cost. Skill
adds a concrete future duplicate-exception change. Neither fabricates staging
evidence or claims staging verification.

All six original files in each retained project match fixture bytes; change
diffs are empty. Both installed skill resources match the frozen Git SHA-256
and before/after manifests. No capture diagnostic flags, rejected patches,
timeouts or event errors; actual check output was inspected, not merely the
absence of flags. No author replay is credited as model execution.

This preserves the earlier adverse reports. The candidate shows workflow
adoption but not the requested efficiency. Do not rerun this pair solely to
improve the score or append another general instruction to avoid extra calls.
Further work needs a distinct mechanism or task-transfer hypothesis.
