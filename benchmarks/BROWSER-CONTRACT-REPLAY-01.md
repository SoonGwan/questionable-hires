# Retained browser QA: correction compatibility

This is **author replay**, not new model performance evidence. It checks the
unchanged native browser harness from the skill session documented in
[browser deduplication](MOTHER-BROWSER-DEDUPE-01.md), resource revision `948431c`.
It does not relabel that historical session with the current skill revision.

The local Colima runtime was available. No image download, credential mount,
personal profile or external site was used. The existing image was
`questionable-hires/browser-codex:0.153.4-pw1.63.0`, ID
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Each replay container used network=none and its own project copy. The unchanged
harness additionally blocks page HTTP(S), uses fresh browser contexts, real
keyboard input and rendered DOM/input/focus observations.

## Results

| Author source variant | Normal success/failure/retry | Late success | Late failure | Late success after clear |
| --- | --- | --- | --- | --- |
| Original | Pass | Fail | Fail | Fail |
| Guard both success and failure | Pass | Pass | Pass | Pass |
| Guard success only | Pass | Pass | Fail | Pass |
| Guard failure only | Pass | Fail | Pass | Fail |

The generation guard is an author-only source correction in disposable copies.
It retains the existing input/response/error behavior and rejects stale completion
in the relevant branch. Removing only one branch guard exposes the corresponding
rendered defect. No assertion or expected state in the retained harness changes.
This verifies that these checks accept a valid correction and distinguish partial
fixes, not merely reproduce the original faulty UI. It does not cover arbitrary
navigation, real backends, accessibility, all browsers or all valid corrections.

[Full observations](browser-contract-replay-01.json) include every checkpoint's
expected/observed state, trusted-input request records, outcomes and cleanup.
Each variant has four nonempty cases, no infrastructure-error case and closed
contexts/browser. The replay script also confirms its uniquely named container
is absent after cleanup. Retained source, harness, dependencies and prior evidence
are fingerprinted before/after and remain unchanged.

The initial author run produced the same four outcome vectors. After adding an
explicit container-absence check, a second author run confirmed them; the initial
report remains local at `local-runs/browser-contract-replay-01-initial.json`.
Neither run is counted as another model sample or used to claim token savings.

## Inspecting and reproducing

[replay_browser_contract.py](replay_browser_contract.py) runs the four variants
with an unchanged retained `qa/catalog.mjs`. The exact
[harness](browser/retained-contract/qa/catalog.mjs),
[page](browser/retained-contract/index.html) and
[original requirements](browser/retained-contract/README.md) are included for
inspection. Harness SHA-256 is
`81b8e5ea02b7d79f5c3d4f1bf446b7ebb681d91a96d1abb2a44e5e862259cee5`;
page SHA-256 is
`f7ee42c67defd033970c11af7aaacbb7930f6b020296993d6d878db32d488419`.
Both included files match the retained model artifacts byte-for-byte.

For replay, supply a project containing those files plus the already-installed
playwright-core 1.63.0 dependency (with its license) under node_modules, and the
existing image above. Dependencies are not embedded in these source excerpts.
Use a project-local scratch parent shared with Colima, not a macOS system-temp
path that the VM may see as empty. The script neither installs dependencies nor
starts the runtime. Each container has a 45-second process deadline, an outer
60-second wait and bounded container removal/inspection.

```sh
python3 -B benchmarks/replay_browser_contract.py \
  --project /path/to/prepared-project \
  --scratch-parent benchmarks/local-runs \
  --output /path/to/new-author-report.json
```

Repository links/metadata and diff whitespace checks passed. No private
home/temp paths or credential markers appeared in the report. Featured charts
and both README languages retain their measured provenance. The broad eight-skill
real-development usefulness and efficiency goal is still not established.
