# Browser model evaluation: isolation preflight

At source `596a1ff`, the existing repository evaluator can copy a standalone clean
Git project into a separate workspace. Its snapshot retains ignored dependency
files too. Installed Playwright is approximately 13 MB; copying it per cell is
feasible, but exporting it would unnecessarily distribute dependencies. Do not
silently omit dependency identities or describe an external import as in-project.

Local preflight copied only `playwright-core` and `search-order.html` into a fresh
temporary project. A Node module launched installed Chrome, blocked HTTP(S) page
requests, opened the copied file, filled the actual query input and completed a
controlled response. It observed `local result` and one browser-trusted `local`
submission, then closed the context and browser. The command exited 0; its outer
author process had a 30-second deadline. No Git, author assertion runner, package
installation or model session was needed. The owned temporary copy was removed.

This establishes dependency resolution and local browser operation from a copied
project. It does not prove the Codex workspace-write sandbox permits the same
launch, model adoption, cleanup under forced timeout, or a performance advantage.

## Evaluation requirements before launch

- Freeze a small baseline/skill comparison and an identical local dependency
  snapshot with hashes. Keep dependencies local, preserve their licenses, and
  separate their inventory from public application evidence.
- Supply raw interaction requirements and controlled response facilities, not
  `input-check.mjs` or its expected outcomes. The model must choose and implement
  the browser checks rather than run an author-written oracle.
- Verify actual fresh-session browser launch and retain failures, including
  sandbox restrictions. Do not relax host permissions automatically.
- Review trusted inputs, rendered observations, actual assertion output, normal
  controls, original-file preservation, cleanup and complete session usage.
  A working author preflight is not a substitute for any of these observations.

No browser model performance claim is supported yet. Earlier author-side browser
checks and Python model comparisons remain separate evidence.
