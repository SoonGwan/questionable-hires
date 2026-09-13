# HTTPX audit interface checkpoint 02

Freeze candidate `89e4d61` and the unchanged `header-equality-audit` task on
HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`. The existing local checkout is
clean and its preinstalled Python 3.9.6 environment remains available. This
follow-up tests cumulative interface/provenance/integrity changes since the
[first pair](HTTPX-HEADER-EQUALITY-01-PROTOCOL.md), whose +65.33% token / −15.92%
time result remains preserved. It is not an unchanged-candidate score retry.

Same full checkout, task, pytest command and two normal controls. No oracle is
supplied to the model. Author preflight with the current helper again shows 27
existing tests passing on correct and faulty code (0.06s each); the exact
duplicate-multiplicity assertion passes correct code and fails set-equality code
with actual_equal True versus expected_equal False. Four checks have copied import
provenance, no timeouts/truncation, selected 65-file integrity and owned scratch
removal. This validates the local audit path, not model adoption. Runner repeats
native correct-code preflight before scheduling.

Two fresh serial Astra medium sessions, baseline and skill once, seed 20260912,
360-second cell limits, no retries or exclusions. Freeze resources before timing;
no author test workloads, fixture edits or resource changes while models run.
Stop new scheduling on account limits and preserve incomplete results. Re-poll
the live handle after observation timeouts instead of starting a replacement.

Review real assertions, normal controls, actual copied imports/caller bindings,
original preservation and cleanup before costs. Check whether the agent consumes
the documented interface/integrity result rather than rereading helper code or
writing duplicate verification. Adoption itself is not success or a percentage
gain. Report both complete costs and unequal work, including adverse results and
capture gaps. Input includes cache once; time is process wall time.

This is an exposed, author-selected audit on real upstream source, not an organic
maintainer request, independent holdout, causal study or all-eight acceptance.
Do not update featured charts from a selected favorable pair.

```sh
python3 -B benchmarks/run_httpx.py \
  --source /tmp/qh-httpx-preflight.3Slnqw/httpx \
  --python /tmp/qh-httpx-preflight.3Slnqw/venv/bin/python \
  --profile header-equality-audit --arms baseline skill --repeats 1 \
  --skill-revision 89e4d61 --output benchmarks/local-runs/httpx-header-equality-02
```
