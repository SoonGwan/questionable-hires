invoice.invoice_total is the only supported entrypoint. Amounts are finite
decimal strings in major units, including negatives and fractional cents. Return
integer cents by rounding half away from zero. amounts.amount_cents is private.
The integer-minor-unit batch importer is retired; no plugins, alternate callers
or supported external imports of amounts exist. Preserve this contract.
