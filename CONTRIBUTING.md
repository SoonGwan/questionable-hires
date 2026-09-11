# We're unfortunately hiring

A good hire has a memorable flaw and a useful engineering instinct.

## Send a job description

Explain the recurring development problem, when the skill should activate, the concrete artifact or decision it produces, and when it should stop. Include one realistic example where its behavior improves the outcome.

The personality belongs in the name, introduction, and occasional short line. Technical findings need evidence, not roleplay.

## Build the smallest useful skill

Place each implemented skill in `skills/<name>/SKILL.md`, with `name` and `description` in YAML frontmatter. Use lowercase hyphenated names. Add scripts or references only when the workflow needs them.

Keep instructions focused on decisions the skill changes. Respect the user's task and repository conventions. Define completion clearly so an investigation doesn't turn into an endless audit. Don't add universal testing requirements, blanket permission questions, or unrelated cleanup.

Investigative requests produce findings. Implementation requests can produce changes and proportionate verification. A character is never authorization to delete, deploy, or publish.

## Bring evidence

Evaluate realistic behavior, including a case where the skill should find nothing and a case where evidence is incomplete. Record limitations. Don't turn a hypothetical demo into a reported result or publish improvement percentages without reproducible comparisons.

Before proposing a new hire, check whether an existing one already handles the same decision.

## Run the checks that match your change

Development dependencies are listed in `requirements-dev.txt`. Install them in
your development environment if needed. These local checks do **not** invoke a
model, install skills into your host, or publish a package:

```sh
python3 scripts/validate.py
python3 -B -m unittest discover -s tests -v
git diff --check
```

For a short packaging feedback loop, run the relevant groups first:

```sh
python3 -B -m unittest discover -s tests -p test_install.py -v
python3 -B -m unittest discover -s tests -p test_build.py -v
python3 -B -m unittest discover -s tests -p test_distribution_cli.py -v
```

Those tests create temporary local trees. They check copy fidelity, ownership of
cleanup targets, errors/cancellation, source-link rejection and command-line
behavior. They do not prove host discovery, remote marketplace installation or
model performance. The full suite also exercises helpers and evaluator mechanics.
Run it before submitting executable changes; for prose-only edits, catalog/link
validation and a focused manual review are normally sufficient.

The repository validator also checks basic consistency of the maintained bug and
new-hire issue forms: required text, body structure, unique input IDs, labels and
boolean validation flags. This is not a full GitHub schema validator or a hosted
form-rendering test.

The real packaging regression uses its checked-in source snapshot, so it also
runs without historical Git objects. A separate generator-equality test skips
explicitly when the pinned commit is unavailable (for example in a shallow
checkout). That skip means provenance was not rechecked, not that the regression
was skipped; use a checkout containing the pinned commit to verify both.
Snapshot and history-collector mechanics tests create disposable Git repositories
instead of relying on this checkout's commit history. Git must still be installed.
The full suite also runs from a source archive, with only the pinned historical
provenance comparison skipped when those original Git objects are unavailable.

## Behavioral evaluation is separate

Commands in `benchmarks/run.py` launch authenticated model sessions and consume
usage. Start with one to three relevant tasks; keep iterative screens below ten
tasks. Freeze the task, candidate resources, baseline, model settings and repeat
count before running. Do not edit the candidate mid-run or retry merely to obtain
better numbers. An exposed development task is not held-out evidence.

Report correctness and scope alongside input + output tokens and elapsed time.
Cached input is already included in input: do not add it twice or discard it.
Keep failures, unequal verification, timeouts and missing output visible. Separate
author-written tests/replays from actions performed by the evaluated model.
See [evaluation instructions](benchmarks/README.md),
[current candidate evidence](benchmarks/CURRENT-CANDIDATE-STATUS.md) and
[release gates](docs/RELEASE-READINESS.md).

Do not commit `benchmarks/local-runs/` wholesale. Review selected artifacts for
private data before sharing; redacted paths alone do not establish that a log is
safe. Follow [security reporting](SECURITY.md) for sensitive findings.
