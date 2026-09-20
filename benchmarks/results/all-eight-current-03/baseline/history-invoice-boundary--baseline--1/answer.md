I’ll inspect the local history, invoice contract, and call path, then check each proposal independently through `invoice.invoice_total` without changing files.

**Recommend A; reject B.** Each was checked independently.

**A — remove the integer early return.** Commit `ee9689a` (“Accept integer minor units from the batch importer”) added `if isinstance(value, int): return value`, preserving already-denominated cents instead of multiplying them by 100. That historical need is now obsolete: commit `9b050b6` retired the importer and established the current contract. [requirements.md](project/requirements.md#L1) makes `invoice_total` the only supported entrypoint and excludes alternate callers. Removing this branch is safe under that contract.

**B — replace quantization with `int(Decimal(value) * 100)`, retaining the early return.** Commit `1d38dfc` (“Preserve half-cent invoice rounding, including credits”) specifically replaced that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)`. This remains necessary: the current contract includes negative amounts and fractional cents and requires rounding half away from zero. B reintroduces truncation toward zero.

The current call path is [`invoice.invoice_total`](project/invoice.py#L5) → reject non-string input → `Decimal(amount)` → `amounts.amount_cents`. Thus the helper receives a `Decimal`, making its integer branch unreachable through the supported caller while leaving rounding essential.

Verified through `invoice.invoice_total`, using Python `-B` and independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | **100** |
| `"-1.005"` | -101 | -101 | -101 | **-100** |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests pass for current and A-only; B-only fails both half-cent tests. All project files were preserved; Git status remains clean.
