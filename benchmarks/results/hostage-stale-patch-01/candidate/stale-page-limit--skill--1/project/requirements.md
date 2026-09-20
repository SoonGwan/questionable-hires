page_limit accepts a normal dict with a missing limit, None, or a
nonnegative integer. Missing/None mean default 100; explicit zero means zero;
positive integers are returned unchanged. Preserve all input entries/references.
No requirements for bools, negative numbers or other invalid inputs. Use Python
3.9+ stdlib and the existing native unittest suite, without modifying it.
