I’m using the receipt skill to compare the two encoder files in disposable local copies, run the five specified tests, and capture their results and import paths without changing the checkout.

The commit changes only JSON encoding options: it preserves Unicode characters, removes separator spaces, and rejects NaN/infinity. Both public constructors reach this encoder. I’ll keep the current package support, tests, conftest, and configuration identical, and use the empty-content test as the control.

Verified retrospectively: **parent encoder: 4 failed, 1 passed; commit encoder: 5 passed.**

- Before: `8e36f2bc685dfbe43cd7503bc1c422a6ed6e05a5`
- After: `9fd6f0ca6616d0310a3ee0b0c6ef509a97995797`
- Confirmed the former is the latter’s direct parent.

Only `httpx/_content.py` varied. The actual change adds `ensure_ascii=False`, `separators=(",", ":")`, and `allow_nan=False` to `json_dumps`.

### Native test results

All cases are from `tests/test_content.py`.

| Test | Before | After | Decisive evidence |
|---|---|---|---|
| `test_empty_content[asyncio]` | PASS | PASS | Control: both streams yield `b""`; headers contain Host and Content-Length `"0"`. |
| `test_json_content[asyncio]` | FAIL | PASS | Before: length `"19"` versus expected `"18"`; both captured streams contain `b'{"Hello": "world!"}'`. After: both equal `b'{"Hello":"world!"}'`, length `"18"`. |
| `test_ensure_ascii_false_with_french_characters` | FAIL | PASS | Before text contains literal `\u00e7`; `"ça va"` is absent. After, `"ça va"` is present. |
| `test_separators_for_compact_json` | FAIL | PASS | Before: `{"cl\u00e9": "valeur", "liste": [1, 2, 3]}`. After matches `{"clé":"valeur","liste":[1,2,3]}` exactly. |
| `test_allow_nan_false` | FAIL | PASS | Before: NaN **did not raise**; infinity assertion was consequently unreached. After: both raise `ValueError` matching `"Out of range float values are not JSON compliant"`. |

**Test process exits:** before **1**, after **0**. Neither run timed out or truncated output.

### Execution and provenance

Used `<PREINSTALLED_PYTHON> -B`, with native `pytest.main`, `-vv -p no:cacheprovider --showlocals`, and exactly the five requested cases per version. Original assertions, conftest, configuration, and current package support were frozen identically.

After native collection, each test process verified that `httpx`, `httpx._content`, `httpx._models`, conftest, and the test module resolved inside its corresponding `.receipt-oomdzi6_/before` or `/after` copy.

Source inspection confirmed public `Request` → `encode_request` and `Response` → `encode_response` both reach `encode_json`. No requests were sent.

Disposable copies were removed; no report or harness remains. The tree guard confirmed unchanged original bytes/modes, including Git metadata and skill resources. This compares encoders under the same installed runtime—not complete historical dependency environments.
