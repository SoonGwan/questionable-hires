# Friday recipe keys01 — 2026-09-28

Parent **`e77372b4`**. The CLI used ordinary `json.loads`, silently retaining only
last values for repeated object keys. A later `phases`, `checks`, SQL field or
reader name could discard declared work before validation. A failing reader
followed by a same-named successful reader could report a complete successful
sequence. Native query errors also leave sequence completion true; completion
alone has never established compatibility.

The parser now rejects repeated decoded keys at every object depth before matrix
input preparation or SQLite connection. File and stdin paths return exit2 and
incomplete JSON. The bounded key-only diagnostic excludes field values. Escaped
equivalent names count as duplicates. Repeated phase-name values, identical SQL
under distinct check names, duplicate result labels and BLOB rows remain valid.
The dict API cannot recover keys already overwritten by a caller's parser.

This reuses the existing duplicate-key approach in Con Artist and Receipt for
Friday's separate CLI boundary. Existing Friday compact-output, API-result-reuse,
core-guide and sequence experiments were reviewed before this change; this is no
new optimization hypothesis and uses no model calls or repeated cost experiment.

[The same eight tests](../tests/test_friday_recipe_keys.py) yielded
[14 failing subcases before](results/friday-recipe-keys01/before.txt), then
[all eight methods passing](results/friday-recipe-keys01/after.txt), zero skips.
They execute the actual CLI with native SQLite, check source bytes/modes unchanged,
and retain a valid-input control. One in-process CLI test wraps matrix/connect to
verify neither is reached after rejection; that structural observation is separate
from subprocess outcomes. Before failures stop subsequent assertions in those cases.
[Git-free focused validation](results/friday-recipe-keys01/gitfree.txt):58 methods
across recipe-key, matrix and row-assertion tests pass. Required frozen fixture data
was copied explicitly, without repository history. Existing model-output formatter
controls exercise historical data; they are not fresh model evidence.

Both README capability rows and the two Friday references describe the boundary.
No entry, featured pointer, chart, integration07 number or whole-task savings claim
changes. Rejecting ambiguous input prevents lost work; it is not token savings.

한국어: Friday CLI가 JSON 중복 키로 앞의 검사나 마이그레이션을 버리던 문제를
수정했다. 실행 전 중복을 거부하되 정상 중복 값·결과 열·BLOB은 유지한다.
수정 전14개 하위 사례 실패, 수정 후8개 메서드 및 Git 없는 사본58개 검사가
통과했다. 한영 설명을 동기화했으며 모델 비용 절감으로 주장하지 않는다.
