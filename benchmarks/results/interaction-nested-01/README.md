# Inspect nested interaction discovery

One exposed task, one session per arm. Skill uses 16.68% fewer tokens and 11.46%
less time. Coverage differs: baseline also tests overlapping query clearing;
skill also tests in-order overlap. This is not general superiority evidence.

| Evidence | Baseline | Skill |
| --- | --- | --- |
| Commands/output | [Read](nested-search-qa--baseline--1/commands.json) | [Read](nested-search-qa--skill--1/commands.json) |
| Actual tests | [Read](nested-search-qa--baseline--1/project/apps/catalog/qa/test_search.py) | [Read](nested-search-qa--skill--1/project/apps/catalog/qa/test_search.py) |
| Answer | [Read](nested-search-qa--baseline--1/answer.md) | [Read](nested-search-qa--skill--1/answer.md) |

See the [review](../../INTERACTION-NESTED-01-REVIEW.md) and
[protocol](../../INTERACTION-NESTED-01-PROTOCOL.md).

Exported with `benchmarks/export.py`. In addition to its path sanitization, six
baseline owner/group listing entries are replaced by `<USER>` and `<GROUP>` in
commands and events. Source hashes identify original artifacts, not edited public
files. Commands, usage, statuses and behavioral output are unchanged. No new model
run was performed. A privacy scanner cannot guarantee absence of private data.
