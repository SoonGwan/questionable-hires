# Ticket store

This is an authored local audit fixture, not a deployed service.
`store.service.submit(directory, key, value)` must synchronously persist the JSON
content before acknowledging success. Reusing a key replaces its content with
the latest complete value. The directory already exists; keys are trusted simple
identifiers and payloads are JSON-compatible. Path hardening, concurrency and
crash-atomic replacement are outside this ticket's contract.

The supported default codec is JSON; no STORE_CODEC override is required.
Run `python3 -B -m unittest -v tests.test_submit` from this project.
Tests allocate and remove their temporary directories under the project cwd.
