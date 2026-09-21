I’ll use the landlord skill to trace the default-resolution policy and callers, then run the existing tests and CliRunner probes with the supplied interpreter. This will remain a read-only review, with no permanent artifacts.

The presence check distinguishes an explicit `None` from a missing entry while keeping `UNSET` hidden from public lookup callers. Both runtime resolution and help/prompt defaults use that distinction. I’ll now check the requested values and whether a factory returning `None` is invoked once.

**Keep both checks.** The proposal changes default resolution: explicit map `None` would become `'fallback'`, and a factory returning `None` would run twice and receive the wrong parameter source.

Executed against the unchanged checkout: **46 tests passed** in `tests/test_defaults.py`. I used the supplied interpreter with `-B`, `PYTHONPATH=src`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and `-p no:cacheprovider`, retaining project settings. Runtime assertions confirmed `click.__file__` and `click.core.__file__` resolve to this repository’s `src/click` files.

The native CliRunner probe used `--name`, `type=str`, `default='fallback'`, and explicit `envvar='LANDLORD_REVIEW_NAME'`. Environment absence was controlled through CliRunner isolation. All invocations exited successfully.

| Inputs | Observed value | Parameter source | Factory calls |
|---|---|---|---:|
| CLI `'cli'`, environment `'env'`, map `'mapped'` | `'cli'` | COMMANDLINE | 0 |
| Environment `'env'`, map `'mapped'` | `'env'` | ENVIRONMENT | 0 |
| Map `'mapped'` | `'mapped'` | DEFAULT_MAP | 0 |
| Map `None` | `None` | DEFAULT_MAP | 0 |
| Map `''` | `''` | DEFAULT_MAP | 0 |
| Map `0` | `'0'` | DEFAULT_MAP | 0 |
| Missing map entry | `'fallback'` | DEFAULT | 0 |
| No map / empty map | `'fallback'` | DEFAULT | 0 |
| Stored `click._utils.UNSET` | `'fallback'` | DEFAULT | 0 |
| Map factory returning `None` | `None` | DEFAULT_MAP | 1 |
| CLI, environment, map factory | `'cli'` | COMMANDLINE | 0 |
| Environment, map factory | `'env'` | ENVIRONMENT | 0 |

The following consequences are **static inference**, not executions of modified code:

- **Stored `None`:** the proposed `consume_value` skips it; the proposed `get_default` then substitutes the parameter default. Result: `'fallback'`, `DEFAULT`.
- **Factory returning `None`:** `consume_value` calls and rejects its result. `get_default(call=False)` retrieves the callable, which is subsequently invoked again. Result: `None`, `DEFAULT`, **two calls**. A stateful factory could also change the resulting value.
- The other table entries retain their behavior: `is not None` accepts empty strings and zero; CLI/environment still short-circuit map resolution.

These paths are visible in [get_default and consume_value](project/src/click/core.py#L2473).

The abstraction has concrete consumers. [Context._default_map_has](project/src/click/core.py#L766) centralizes “present, including `None`, but excluding stored `UNSET`.” Public `lookup_default` deliberately returns `None` for absence, so its return value alone cannot encode presence. Existing tests explicitly require [map `None` and correct sources](project/tests/test_defaults.py#L238), [hidden absence and preserved falsy values](project/tests/test_defaults.py#L170), and [stored `UNSET` falling through](project/tests/test_defaults.py#L551).

The policy also reaches [Context.invoke](project/src/click/core.py#L894), [help rendering](project/src/click/core.py#L3448), and [prompt defaults](project/src/click/core.py#L3514). Removing the `get_default` check would make these callers substitute a fallback for explicit map `None`. Source attribution also participates in option arbitration; it is more than diagnostic text.

A concrete future maintenance change illustrates the cost: suppose a configuration loader must represent “inherit the parameter default” with stored `UNSET`, while retaining `None` as an explicit override. With the current structure, the absence policy belongs in `_default_map_has`; both resolution paths share it, and public lookup continues hiding the sentinel. Replacing presence with non-`None` forces that distinction back into callers or requires a richer lookup API. Simple membership alone would also mishandle `UNSET`.

**Viable alternative:** retain the implementation and clarify the two guards with brief comments explaining the public lookup ambiguity. A richer presence/value result would require preserving public `lookup_default` overrides and `call=False` behavior—both have [existing compatibility tests](project/tests/test_defaults.py#L422)—and adds migration cost without a demonstrated need here.

Repository file contents and modes matched the pre-execution snapshot, including Git metadata and skill resources. HEAD/index remained unchanged; owned temporary scratch was removed. No permanent tests or report were created.
