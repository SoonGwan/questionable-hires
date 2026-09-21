Registry accepts a dict mapping string keys to mutable dict records.
get(key) must return the exact record object supplied for that key, not an equal
copy. Caller edits through a returned record must be visible through later gets
and through the original input dict. Different keys retain their own records.
A missing key raises KeyError. Other input types are outside this contract.
