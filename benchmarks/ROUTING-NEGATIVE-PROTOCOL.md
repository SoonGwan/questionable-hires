# Current-bundle unrelated-request routing screen

Freeze all eight skills at `bead33d`. Two new narrow comprehension/summarization
requests in `routing-negative-cases.json`, one auto-arm session each, serial Astra
medium, seed 20260911, 240-second limits. No retries/exclusions. Auto installs all
eight skills and does not explicitly invoke one. The required `skill` case fields
are runner metadata only, not desired selections or instructions to the model.

Purpose: inspect needless activation and task expansion outside the hires' stated
jobs. Neither request requires a specialized skill. Correct answers alone do not
establish correct routing. Inspect actual skill file reads, other instruction
sources, commands and original outputs, plus final answers and file preservation.
File access is observable evidence, not a guarantee about hidden selection or
host-provided context. Record any discovered personal-skill disablement limits.

Report both results and all input+output tokens and time. No no-skill arm, causal
overhead claim, false-positive population estimate or all-eight acceptance from
two cases. This does not replace the positive-task performance gate. If an
unrelated skill activates, use that concrete trace before changing its description;
do not disable automatic selection merely to pass this screen.
