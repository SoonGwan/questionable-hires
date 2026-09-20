# Allocation service

`reserve` returns a new stock mapping. Duplicate SKU lines accumulate;
invalid or insufficient orders raise ValueError without mutating input.
Stock maps SKU strings to nonnegative integer counts. Lines are a finite list
of (SKU string, integer quantity) pairs; nonpositive quantities and unknown SKUs
are invalid. Empty orders are valid. Other input types are outside this contract.
Native suite: `python3 -B -m unittest -v test_allocation`. Standard library only.
