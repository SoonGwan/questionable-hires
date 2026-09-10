# Exorcist transfer check — preregistration

Freeze this file and `exorcist-transfer-cases.json` in Git before model execution. No sessions in this experiment have run at plan creation.

Compare original Exorcist from `be9d038` and candidate from `e2eb92b`, plus no-skill baseline. Three new diagnostic tasks, three repetitions per condition: 27 sessions. These tasks were authored after the candidate text, without additional tuning to them. They are author-designed transfer checks, not blinded third-party evidence or real-repository tasks.

Use Astra medium, fresh process/project per cell, 240-second timeout, concurrency one. Alternate condition order by repetition: baseline/original/candidate, candidate/baseline/original, original/candidate/baseline. Each invocation runs all three cases once with a fixed seed equal to 20260911 plus repetition. Separate output directories identify condition and block. Preserve all failures, no cell reruns, stop the experiment on an explicit account limit.

Review each predefined criterion as pass/fail/unknown against command output and final artifacts. Correctness, explanation of safeguard, runtime uncertainty, and scope remain separate; strict success requires all criteria and no evidenced scope deviation or unresolved scope uncertainty. Review original and candidate with the same rubric; author review is unblinded. Do not use answer length as quality. Missing runtime case requires no artificial execution.

Primary question: does the candidate preserve causal accuracy and clean-case restraint while explaining the safeguard? Secondary observations: CLI input (including cached), output, elapsed time. Report per-task outcomes and raw values, not a general speed or reliability claim. A tie or regression remains visible. Existing search results are development evidence and excluded. Keep original 72-session results unchanged.

Prepare isolated snapshots without altering installed skills; verify entrypoint hashes against the pinned commits. Use the runner's `--cases-file` and `--skills-root` options. Export only after reviewing raw logs for private information. An implementation/environment failure is not evidence of a wrong diagnosis.
