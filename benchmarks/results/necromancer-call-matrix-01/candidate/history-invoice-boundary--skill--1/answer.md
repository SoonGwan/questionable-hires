I’ll use the necromancer skill to trace each behavior’s introducing change, check the current invoice contract and caller, and test the proposals separately in memory. I’ll preserve all project files.


The integer guard was added to preserve amounts already expressed in cents. The current invoice boundary always passes a `Decimal`, and the contract explicitly retires integer callers. Rounding has a separate origin: its introducing patch replaced truncation to handle half-cent invoices and credits. I’ll now verify all three versions through `invoice_total`.


**Recommend A; reject B.** The proposals were tested independently.

The current path is [`invoice.invoice_total`](project/invoice.py#L5) → string validation → `Decimal(amount)` → `amount_cents`. The [supported contract](project/requirements.md#L1) requires integer cents rounded half away from zero and explicitly excludes alternate callers and external imports.

**A — remove the integer early return**

- **Historical reason:** Commit `ee9689a28e043cc57317c118786ce7f5b1f213b4` added precisely `if isinstance(value, int): return value`. This preserved already-in-cents integers instead of multiplying them by 100; the commit identifies the batch importer as the motivation.
- **Current necessity:** None under the supported contract. Commit `9b050b628b971c45ff80073172d26f262341ada0` changed the invoice caller to validate strings and pass a `Decimal`, and documented retirement of the integer importer. The integer branch is unreachable through the supported entrypoint.
- **Recommendation:** Approve removing just the guard.

**B — replace quantization with `int(Decimal(value) * 100)`**

- **Historical reason:** Commit `1d38dfc0c1a1255c8f9a5f8dd8aaab9c58a58d34` replaced exactly that truncating expression with `quantize(..., rounding=ROUND_HALF_UP)` and added its import. The change preserved half-cent rounding, including negative credits.
- **Current necessity:** Half-away-from-zero rounding remains required. B truncates toward zero and breaks both half-cent cases. Keeping the integer guard does not help because the caller supplies a `Decimal`.
- **Recommendation:** Reject this replacement; retain the required rounding behavior.

Observed through `invoice.invoice_total`:

| Input | Required | Current | A-only | B-only |
|---|---:|---:|---:|---:|
| `"1.005"` | 101 | 101 | 101 | 100 ❌ |
| `"-1.005"` | -101 | -101 | -101 | -100 ❌ |
| `"2.34"` | 234 | 234 | 234 | 234 |

Verification used `python3 -B` with independent in-memory substitutions. All three existing tests passed for current and A-only; B-only failed both rounding tests. The verification harness exited 0 after confirming these expected outcomes.

No project files changed; Git status remained unchanged, including the pre-existing untracked `.agents/` directory.
