# Avoid unnecessary input-list reconstruction

The HTTPX routing trace manually listed test support files after extra discovery,
where earlier successful recipes selected the package and tests directories.
To assess whether copy size justified that work, the current helper's `snapshot`
was run read-only on pinned HTTPX `26d48e0634e6ee9cdc0533996db289ce4b430177`:

| Selection | Files | Bytes |
| --- | ---: | ---: |
| `httpx`, `tests`, `pyproject.toml` | 65 | 782,562 |
| `httpx`, test package init/conftest/concurrency/test_asgi, `pyproject.toml` | 29 | 304,778 |

Both are well below the helper's 20 MB limit. Earlier model-run evidence already
shows both recipes execute the same exception test file successfully on correct
code and detect the same four mutant failures. No model or test-suite rerun was
needed for this size observation. This is not a controlled speed comparison,
nor proof that the added discovery caused all token differences.

The usage reference now prefers small permitted package/test directories over
manually reconstructing imports solely to save copy bytes. Narrow selection
remains appropriate for large trees, scope limits, sensitive data or unsupported
contents. This does not authorize copying arbitrary repositories/environments.
No automatic scope expansion or dependency inference was implemented.

The instruction aims to trade cheap local copying for fewer agent decisions
without losing supporting fixtures. Its effect on agent behavior and total
cost is unmeasured. Keep this as a candidate, not a performance claim; validate
it on the next relevant changed workload rather than another immediate repeat
of the same HTTPX exception task.
