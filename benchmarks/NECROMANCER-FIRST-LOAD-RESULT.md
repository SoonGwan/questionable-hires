# Native-history regression after entrypoint compression

Snapshot/protocol c9e0aa2, entrypoint 8454059, runner fd8d578. Unchanged exposed
history-active case, fresh Astra medium baseline then skill, one repeat, serial
seed 20260911, 240-second limit. No retries, exclusions or candidate edits.
Private original evidence: `local-runs/necromancer-first-load-01/`.

| Arm | Input + output tokens | Process seconds | Shell commands |
| --- | ---: | ---: | ---: |
| baseline | 62,723 | 32.243 | 3 |
| skill | 67,723 | 33.286 | 3 |

Skill uses **8.0% more tokens / 3.2% more time**. Cached input is already included.
This is an exposed regression with unequal evidence, not causal measurement of
compression or a held-out/general performance claim.

Both preserve the fallback and original files, execute the actual live caller and
show name-only and falsy-display-name behavior. Skill additionally checks an
ordinary v2 payload, attributes the fallback with blame, inspects the introducing
commit's actual patch and cites d5fc972. It distinguishes historical intent from
the live supported caller. Baseline gives a valid current-behavior recommendation
but does not inspect/cite Git history, so it does not satisfy that frozen criterion;
the neutral task itself only asks for evidence, not explicitly for history.

Skill uses native Git without reading the collector reference or implementation.
It collects a tiny two-line blame and two-entry log; the broad numeric blame range
does not imply narrowly selecting only the changed line, but no large-file history
is present here. This establishes the ordinary-path behavior only, not collector
adoption, large rewrites or incomplete-history transfer.

All four original file copies match the frozen case; four installed resources
match frozen Git hashes and before/after manifests. No captured scope expansion,
rejected patches, malformed JSON, empty-output flags, timeouts or event errors.
Original command outputs contain the live results and actual historical patch.
No author replay is credited. Repository validation passes; prior helper tests
validate unchanged mechanics, not session performance.

No additional skill wording change is supported by this correct narrow regression.
The candidate remains unproven against the overall efficiency objective. Retain
the result without repeating the exposed case to seek a favorable sample.
