# Scheduling windows

Input is a finite list of integer pairs (start, end), start < end. Return sorted, coalesced half-open windows, merging both overlaps and touching endpoints. Preserve the input. Empty input is valid. Other types and invalid intervals are out of scope.
Native suite: python3 -B -m unittest -v test_windows. Standard library only.
