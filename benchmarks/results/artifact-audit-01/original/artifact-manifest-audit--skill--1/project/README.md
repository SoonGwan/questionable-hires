# Artifact manifest contract

Use the preinstalled interpreter `<HOME>/orca/workspaces/this-work/humpback/benchmarks/local-runs/receipt-provenance-venv/bin/python`; pytest is already installed.
Native suite: `<HOME>/orca/workspaces/this-work/humpback/benchmarks/local-runs/receipt-provenance-venv/bin/python -B -m pytest -vv -s -p no:cacheprovider checks_manifest.py`.
conftest configures the format before importing the application; retain native
configuration, both parametrizations and the empty control. Test scratch is
project-local and fixture-owned. No network or global temporary-directory changes.

Inputs are finite lists of records with exactly name and sha256 string fields;
sha256 is a 64-character lowercase hexadecimal digest. Preserve record order,
duplicate names, Unicode names and exact digests in UTF-8 JSON. Empty lists are valid.
Return the number of written records. Other types/keys, concurrent writers and
crash recovery are outside this contract. Do not change production or fixtures.
