# Necromancer first-load candidate

Candidate 8454059 reduces the entrypoint from 513 to 371 whitespace-delimited
words. The optional collector's invocation/environment details already exist in
focused-history.md, so the entrypoint routes there only for repeated collection
instead of duplicating the recipe. No extra reference file, helper, framework or
required artifact is introduced. Collector, reference and UI metadata are unchanged.

The ordinary native Git path remains directly available: scoped blame, relevant
before/after inspection, pickaxe when attribution is unresolved, rename handling
and region selection for bulk changes. Removed-line context and excerpt limitations
remain explicit. Current necessity still requires a live contract or behavior;
public contracts aren't declared obsolete merely for lacking local callers.
Absent/shallow history stays unknown without fetching or contacting former authors.
Review/implementation boundaries, user changes and the character remain intact.

Eighteen actual history-helper tests and both validators pass. This proves existing
mechanics and structural validity, not candidate adoption or session savings.
Word reduction is not a model-token measurement. Conditional reference loading
may add a read in collector-heavy work; native-Git and collector paths need separate
behavioral checks before claiming improved efficiency. Earlier benchmarks measure
earlier entrypoints, not this candidate. Overall objective remains unmet.
