I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test both proposals independently in memory.



**A: approve removal. B: reject replacement.** These are independent recommendations.

The current contract in [requirements.md](project/requirements.md#L1) supports only `invoice.invoice_total`, with finite decimal strings in major units and half-away-from-zero rounding. The current path is [invoice_total](project/invoice.py#L5) → string validation → `Decimal(amount)` → [amount_cents](project/amounts.py#L4).

- **A — remove the integer early return.** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` introduced exactly the `isinstance(value, int)` branch and unchanged integer return. Its stated purpose was accepting batch-importer integers already expressed in minor units; the patch prevents multiplying those cents by 100. That historical compatibility is no longer required: commit `9b050b628b971c45ff80073172d26f262341ada0` added the string-only boundary, Decimal conversion, and explicit contract retiring the importer and excluding other supported callers. The branch is unreachable through the supported path. Removing only that branch is appropriate.
- **B — replace the quantized return, keeping the early return.** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced precisely `int(Decimal(value) * 100)` with quantization using `ROUND_HALF_UP`, introducing half-cent rounding for invoices and credits. That behavior remains required. The proposed replacement truncates toward zero and reproduces the original rounding defect. Keep the quantized return.

Verified through `invoice.invoice_total` using independent in-memory substitutions:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

The existing three tests passed for current and A-only; B-only failed both half-cent tests. Each substitution matched exactly one AST statement, and compilation preserved the module’s future settings. All Python ran with `python3 -B`.

No files were changed or created. Git status remained unchanged, including the pre-existing untracked `.agents/` directory.
