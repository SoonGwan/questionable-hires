# Retain one native check when terminal capture is unreliable

Prefer an existing native report tied to the current command and inputs. Use this
fallback only when output has been lost or capture is known to be unreliable,
and project-local evidence files are permitted. It does not recover past output.
Do not rerun side-effectful work to obtain a nicer transcript.

Run from the intended project directory, in a POSIX shell with `mktemp`. This
example uses unittest; replace the argv after `set --` with the project's actual
native command. It runs that command once, without a pipe or replacement runner:

```sh
(
  evidence_dir=$(mktemp -d ./.test-evidence.XXXXXX) || exit 1
  set -- python3 -B -m unittest discover -v
  printf '%s\n' "$@" > "$evidence_dir/argv.txt" || exit 1
  if "$@" > "$evidence_dir/output.txt" 2>&1; then
    check_exit=0
  else
    check_exit=$?
  fi
  printf '%s\n' "$check_exit" > "$evidence_dir/exit.txt" || exit 1
  printf 'Evidence: %s\n' "$evidence_dir"
  cat "$evidence_dir/output.txt"
  exit "$check_exit"
)
```

If displayed output is lost, read this run's `argv.txt`, `output.txt` and
`exit.txt` instead of repeating the test. Check native identities/count, outcomes
and exit together: zero tests, skipped tests or command-not-found are not passes.
An absent exit file means completion is unverified; observe a live process if
available. Keep the execution tool's timeout and existing task cleanup; this
recipe supplies neither a process deadline nor cancellation of child processes.

The fresh directory avoids overwriting previous evidence. It is not a tamper-proof
attestation or input snapshot. Associate it with the actual invocation and code
revision; changed inputs require fresh evidence, not relabeling an old log. Do not
commit logs automatically: they may contain secrets or machine paths. Respect the
project's retention/cleanup rules and identify retained files in the handoff.
No project writes allowed? Use a permitted existing reporting path or state the
verification limit; do not broaden scope merely to store a report.
