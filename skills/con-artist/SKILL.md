---
name: con-artist
description: Audit whether tests detect broken behavior by tracing assertions and running narrow controlled mutations in an isolated workspace; use for test-quality reviews, not routine test execution.
---

# Con Artist

> Your mock is very impressed with itself.

## Check what the test actually buys

Start with the user-selected tests or changed behavior. Run the baseline and trace each important assertion through the actual implementation and mocks. Identify the contract supposedly protected.

Choose a plausible fault that violates that contract: omit a write, reverse a comparison, ignore a rejected response, or return stale data. An arbitrary syntax error doesn't test behavioral sensitivity. Check whether the mutation changes behavior on reachable inputs; equivalent or unreachable mutations don't prove a weak test.

Run controlled mutations only in a disposable copy or isolated worktree, never over existing user changes. Change one behavior at a time and run the relevant tests. Record the baseline, mutation, and result. A surviving mutation can indicate missing assertions, missing input coverage, or a wrong claim about the test; investigate before concluding.

If isolation or execution isn't available, report a static concern and proposed experiment, not a demonstrated survivor. Keep a failing baseline separate from mutation results.

## Deliver and stop

Show the meaningful fault a test failed to catch, the executed command and result, and the smallest stronger assertion or scenario. Improve the test when requested. Confirm it passes on correct code and fails for the targeted fault; never ship the deliberate fault.

Stop after the scoped coverage claims have been assessed and any requested improvement verified. Don't chase a global mutation score or demand every mock be removed.

## Working agreement

Follow the user's requested outcome and repository conventions. User instructions take precedence over this skill's preferences. Resolve routine choices from available context and keep working within authorized scope. Investigation is not permission to implement or publish. Preserve existing user changes.

Use the user's language. Keep the character to an optional short line; never insult people or substitute a joke for evidence. Report observed facts separately from inferences and unavailable checks. If a skill instruction actually prevents progress, cite that instruction and explain the concrete conflict.

