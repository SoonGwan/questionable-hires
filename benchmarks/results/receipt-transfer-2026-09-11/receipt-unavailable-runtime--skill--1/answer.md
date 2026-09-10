I’ll use the receipt skill to inspect the patch and run the relevant regression check, without changing project files or adding dependencies. I’ll distinguish observed results from anything the environment prevents me from verifying.

The fix is **not behaviorally verified**.

- At revision `654a404`, `ledger.amount()` passes `rounding='half_even'`. `requirements.md` describes the patch as changing `half_up` to `half_even`; no prior revision or working-tree diff is available.
- Ran `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_ledger` — **exit 1**, because `company_ledger_runtime` is missing. The assertion `amount('1.005') == '1.00'` never executed. This is an import failure, not reproduction of the rounding defect.
- **Before evidence:** unavailable. **After evidence:** blocked by the missing actual runtime package.

No project files were changed, dependencies installed or fabricated, or external services used.
