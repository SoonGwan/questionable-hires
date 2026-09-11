# Inspect the Landlord compression comparison

This is an adverse previous-versus-candidate comparison, **not baseline versus
skill**. See the [report](../../LANDLORD-COMPACT-01.md) and
[frozen protocol](../../LANDLORD-COMPACT-PROTOCOL.md).

| Evidence | Previous | Compact candidate |
| --- | --- | --- |
| Actual commands and captured outputs | [commands](previous/store-check-scope--skill--1/commands.json) | [commands](candidate/store-check-scope--skill--1/commands.json) |
| Model answer with linked source | [answer](previous/store-check-scope--skill--1/answer.md) | [answer](candidate/store-check-scope--skill--1/answer.md) |
| Usage, elapsed time and resource inventories | [metadata](previous/store-check-scope--skill--1/metadata.json) | [metadata](candidate/store-check-scope--skill--1/metadata.json) |
| Full exported events | [events](previous/store-check-scope--skill--1/events.jsonl) | [events](candidate/store-check-scope--skill--1/events.jsonl) |

The exporter preserves event order, command outputs and usage while redacting
local paths. Answers rewrite local source links for this directory. Source file
hashes identify the private inputs to export; those hashes are not independently
verifiable without the original private files. No missing output was reconstructed.
The synthetic final projects are included; they match the original fixture.

All exported commands, answers, manifests, stderr and project content were reviewed;
the pattern scanner reports no findings. A scanner is not a secrets-proof guarantee.
No live account configuration or original private stdout is shipped.

Check the shipped artifacts offline, including from a source archive:

```sh
python3 -B -m unittest discover -s tests -p test_landlord_public_evidence.py -v
python3 -B benchmarks/scan_evidence.py benchmarks/results/landlord-compact-01
```

The audit cross-checks captured usage, command records, resource inventories,
fixture digest and final file bytes. It does not infer correctness from process
completion; the behavioral judgment and limits are in the linked report.
