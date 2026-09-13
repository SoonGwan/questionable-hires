# Multi-decision history screen 01 — in progress

Resource/launch `667eb10`; [frozen protocol](NECROMANCER-REGIONS-01-PROTOCOL.md).
Skill cell remains pending; no comparison result yet.

## Baseline

Completed: **106,845 recorded tokens / 66.450 seconds**, six shell calls.
Correctly retains code fallback and negative rejection, permits removing the
private display-name fallback while keeping public caller normalization. Cites
the three actual introducing commits and later normalization. Reads actual
requirements, consumer and history; no unsupported public-API inference.

Original native suite passes 4/4 with individual results captured. In-memory
variants replace the actual consumer binding without editing files. Existing
suite results are summarized: original 4/4, no-code 1/4, no-display 4/4, no-negative
3/4. Additional 27-case Cartesian coverage per variant tests missing/empty/full
code and display name against negative/zero/positive amounts, with input-mutation
assertions. Native matrix results: 27/27, 12/27, 27/27, 18/27 respectively. Selected
actual/expected failures are printed; inner unittest traces are intentionally
captured into StringIO and not printed. This is not full per-variant native output.

Final recommendation/counts agree with the captured commands and outcomes. Extra
full history/stat output and repeated discovery are present. Git status/diff is
clean, final inventory unchanged; source/resource/raw reconciliation follows after
timing. No capture diagnostic or observed scope violation.
