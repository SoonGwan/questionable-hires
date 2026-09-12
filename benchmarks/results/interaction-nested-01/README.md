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

## Replay without model usage

From this directory, enter either exported project's `apps/catalog` directory:

```sh
cd nested-search-qa--skill--1/project/apps/catalog
python3 -B ../../tools/check.py --timeout 3 -- python3 -B -m unittest discover -s qa -p 'test_*.py' -v
```

Use the corresponding baseline directory for the other arm. Requires Python 3.9+
and POSIX, with no dependency installation or Git history. Expected CLI status
is **1**, because these QA tests expose an unfixed defect. Skill output has one
failure; baseline has two. A timeout or import error is not the expected result.
The runner's JSON distinguishes those outcomes and includes normal-test success.

The repository regression copies each exported project into its own temporary
directory and executes that command using the test interpreter. Both reproduced
their expected assertion failures and normal success on the local host, without
changing any copied files. This is author replay, not new model evidence or a
replacement for original traces; replay elapsed time is not benchmark latency.
