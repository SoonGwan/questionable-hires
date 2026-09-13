render is the sole supported entrypoint. summary.summarize is private.
Input name is nonempty; display_name and code may be missing or empty. Missing or
empty code must render as 'unknown'; missing or empty display_name uses name.
amount is an integer and negative values must raise ValueError. Upstream does not
reject negatives. There are no other consumers, plugins or supported direct calls.
Use python3 -B -m unittest -v. Review only: preserve all original files.
