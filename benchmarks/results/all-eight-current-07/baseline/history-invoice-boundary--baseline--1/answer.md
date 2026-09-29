I’ll inspect the local history, invoice contract, and caller, then test the current implementation and each proposal independently through `invoice.invoice_total`.


**Recommend A; reject B.** The historical reasons differ, and only the rounding behavior remains necessary.

- **A — remove the integer early return:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced `if isinstance(value, int): return value` to accept batch-importer integers already expressed in minor units, avoiding multiplication by 100. That purpose is obsolete under the current contract.
- **B — replace quantization with `int(Decimal(value) * 100)`:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly that expression with `quantize(..., rounding=ROUND_HALF_UP)` to preserve half-cent rounding, including negative credits. This remains required: `int()` truncates toward zero.

Commit `9b050b628b971c45ff80073172d26f262341ada0` established the current boundary and retired the importer. [requirements.md](project/requirements.md#L1) specifies the sole supported entrypoint, finite decimal strings in major units, and rounding half away from zero; the helper is private with no supported alternate callers.

The current path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → [`amounts.amount_cents`](project/amounts.py#L4). Consequently, the integer branch is unreachable for supported calls, while fractional-cent rounding is still exercised.

Verified through `invoice.invoice_total` using independent in-memory substitutions with `python3 -B`:

| Input | Required cents | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 |
| `"-1.005"` | -101 | -101 | -101 | -100 |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three invoice tests passed for current and A-only; B-only failed both half-cent tests. B retained the integer early return throughout verification.

All project files were preserved; Git remained clean.
