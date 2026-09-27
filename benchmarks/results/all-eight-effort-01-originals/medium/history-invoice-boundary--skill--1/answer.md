I’ll use the necromancer skill to trace both behaviors to their introducing changes, check the current invoice contract and caller, and test each proposal independently without changing files.


The integer branch was introduced for the retired batch importer; the current invoice caller always passes a `Decimal`. Rounding was introduced separately to preserve half-cent behavior, which the current contract still requires. I’ll now check all three versions through `invoice_total`.


**A: approve removal. B: reject as proposed.** These conclusions treat the proposals independently.

The current supported path is [`invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → [`amount_cents`](project/amounts.py#L4). The [contract](project/requirements.md#L1) requires finite decimal strings in major units, rounded to integer cents half away from zero. It explicitly excludes other supported callers and retires the integer importer.

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced exactly the `isinstance(value, int)` branch, leaving rounding unchanged. Its historical purpose was to accept batch-importer integers already expressed in cents without multiplying them by 100. That purpose is obsolete under the current contract: commit `9b050b628b971c45ff80073172d26f262341ada0` added the retirement contract and changed the invoice caller to pass a `Decimal`. The branch is unreachable through the supported entrypoint. Smallest change: remove only that branch.

- **B — replace quantization with `int(Decimal(value) * 100)`.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced that exact truncating expression with `quantize(..., rounding=ROUND_HALF_UP)` and added the rounding import. Its historical purpose was to preserve half-cent rounding, including negative credits. That behavior remains required today. Quantization’s particular mechanism could be replaced by equivalent rounding, but this proposal truncates toward zero and breaks the contract. Retain the existing return.

Verified using `python3 -B`, substituting each proposal separately in memory and calling `invoice.invoice_total`:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

The three existing tests also passed on current code; the probe exited 0. Project files were unchanged, and Git status retained only the pre-existing untracked `.agents/` directory.
