# Hiring plan

Build one useful skill, establish the evaluation pattern, then expand the team.

## Current status

All eight skill instructions and UI entries are implemented. Local installation, plugin manifest validation, catalog checks, and 11 deterministic installer/fixture tests pass. The items below describe the remaining behavioral evaluation and distribution work, not a claim that all milestones are complete.

GitHub Actions is configured, but the initial run could not start because GitHub reported failed account payments or an insufficient spending limit. Account billing must be resolved for hosted CI; local checks remain available.

- [x] Eight focused skill implementations.
- [x] Non-overwriting local installer and failure recovery tests.
- [x] Validated Codex plugin manifest.
- [x] Installation guide and Astra design notes.
- [x] Executable baseline fixtures for five engineering failures.
- [ ] Complete neutral evaluation fixtures, including historical, multi-file, and clean cases.
- [ ] Execute and record behavioral evaluations for every hire.
- [ ] Run controlled Astra baseline comparisons before making performance claims.
- [ ] Verify marketplace installation end to end.
- [ ] Obtain a passing hosted CI run after the account billing issue is resolved.

## 0. Open the office

- [x] Establish the project name and voice.
- [x] Document the planned team and contribution criteria.
- [ ] Finish the first skill before adding installation instructions or plugin packaging.

## 1. Hire Necromancer

Input: a suspicious code path and a question about changing it.

Output: its current purpose, historical evidence when available, conditions that must survive a change, and an actionable recommendation with uncertainty made explicit.

Initial evaluation cases:

- A timing workaround whose original race still exists.
- A compatibility branch whose supported consumer still needs it.
- A workaround whose original cause has already been removed.
- Missing or shallow history: report uncertainty without inventing intent.

Separate observed behavior from inferred intent. Stop when the recommendation has enough evidence; don't excavate the entire repository. Investigation alone must not silently become implementation.

## 2. Establish an honest evaluation loop

Run the same realistic task from the same starting state with and without the skill, using the same Astra configuration and tools. Record the model, settings, fixture revision, commands, results, and limitations. Repeat enough to expose variability before making comparative claims.

Assess whether the recommendation is correct, its citations support it, relevant compatibility constraints survive, and the agent stays within scope. Track time and tokens when the environment exposes them. A shorter response alone is not a quality gain.

Keep evaluation fixtures local and reproducible. Don't publish private project code, logs, or history as benchmark material.

## 3. Package the first working hire

Add a validated Codex plugin manifest and documented installation path after the first skill passes realistic evaluation. Keep packaging separate from model behavior claims.

## 4. Grow the team

Proposed order, adjustable after actual use:

1. Receipt — proof that a bug fix changes behavior.
2. Mother-in-law — realistic interaction failures.
3. Exorcist — discriminating debugging experiments.
4. Landlord — maintenance cost of new structure.
5. Hostage Negotiator — scope control.
6. Con Artist — test sensitivity to broken behavior.
7. Friday — deployment reversibility and compatibility.

Each hire needs a distinct job. Merge overlapping concepts if usage shows they don't deserve separate skills.
