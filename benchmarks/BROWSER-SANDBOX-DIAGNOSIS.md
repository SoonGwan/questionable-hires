# Browser launch diagnosis: enforcement boundary plausible, cause unproven

Read-only follow-up to [browser model 01](BROWSER-MODEL-01-REVIEW.md).
The original model commands used `codex exec --sandbox workspace-write` with
user configuration and rules ignored. Both retained browser logs show SIGABRT
and kill EPERM, but no captured rule-level denial identifying a forbidden path,
Mach service or system operation. A targeted search of the retained skill TAP
log did not reveal such a diagnostic. That absence does not rule out enforcement.

The [official sandbox documentation](https://learn.chatgpt.com/docs/sandboxing),
retrieved 2026-09-12 KST, states that spawned commands inherit sandbox boundaries
and macOS uses Seatbelt. This makes an enforcement difference between successful
author preflight and failed model launches plausible, not a proven root cause.

Local `codex exec --help` confirms workspace-write selection. Local
`codex sandbox --help` exposes direct command execution, `--log-denials`, and
`--sandbox-state-json`. This installed CLI does **not** have a `macos` subcommand:
the attempted `codex sandbox macos --help` treated `macos` as the executable and
returned exit 71 (missing executable). No browser or configuration change followed.

Do not substitute an unrestricted launch, a host browser endpoint, additional
socket permission or a new profile and label it the same experiment. A useful
next diagnostic requires the original effective sandbox state, or a demonstrably
equivalent policy, and a bounded minimal launch with denial logging. The original
event export does not currently supply that state. Reading unrelated credentials
or broad application logs is not needed for this investigation.

No new model usage, browser retry, permission change or host setting modification
was performed in this follow-up. Browser model QA remains incomplete. Skill
iteration and other in-scope release work can continue independently.
