# Optional deadline for a local probe

Use for an identified hang risk, including blocking synchronous operations or
cancellation suppression, that the existing runner's process deadline does not
contain. Bounded local computation does not need this additional wrapper.
Invoke the installed helper without reading its implementation unless
adaptation is needed:

```sh
python3 /path/to/exorcist/scripts/run_probe.py --timeout 10 -- python3 -B experiments/probe.py
```

Replace the command with the project's actual interpreter/runner. It executes
argument vectors without a shell, inheriting the current directory and environment;
it does not install dependencies, copy files, or make the probe read-only.
Trusted, authorized foreground commands only—not servers, external operations or
a security sandbox. It kills its process group on deadline and cleans up remaining
group members after normal completion. Processes that escape that group are not
contained. Requires Python 3.9+ and POSIX.

JSON retains the actual `exit_code`, `timed_out`, elapsed seconds and last 12,000
combined-output characters with a truncation flag. CLI status: 0 successful child,
1 unsuccessful child, 124 wrapper deadline, 2 invalid invocation. A child exiting
124 is still CLI 1; inspect JSON. Default deadline 10 seconds, maximum 300.
Timeout or truncated decisive output is missing evidence, not the suspected bug.
Keep task cleanup and useful assertions in the probe; this replaces process-level
deadline plumbing, not experiment design.
