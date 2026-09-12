# Containment and evidence routing correction

The provenance transfer used a process wrapper for inspected bounded dictionary
operations and serialized a required trace both to disk and stdout. Candidate
changes two decisions, without changing helper mechanics or task coverage:

- Default to the chosen interpreter/test runner for bounded local computation.
  Use additional containment for an identified hang risk not already covered by
  a process deadline. Synchronous blocking is explicitly included: async syntax
  is not the selection criterion. Cancellation suppression still requires a real
  process deadline rather than reliance on asyncio wait timeouts.
- Choose one detailed-evidence destination. A required retained trace gets a path
  and decisive summary on stdout; full console duplication remains available when
  needed to resolve the diagnosis. Unrequested transient results can remain in
  captured output. Required provenance and reproducibility remain intact.

This replaces the ineffective output recommendation rather than adding a helper
or generic tracing schema. Nine existing helper tests and both validators pass;
those prove mechanics/structure, not model routing or performance. The candidate
is unmeasured. Future behavioral evaluation needs both genuinely blocking and
bounded paths; do not convert the observed invoice case into a repeated score hunt.
