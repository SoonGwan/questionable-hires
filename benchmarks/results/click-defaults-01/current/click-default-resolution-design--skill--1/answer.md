I’ll use the landlord skill to trace the default-resolution policy, run the existing tests and CliRunner probes, and assess the proposal without changing repository files.

The code distinguishes a missing map entry from an explicit `None`, while the public lookup returns `None` for both. Existing tests require that distinction and preserve subclass overrides. I’ll now check runtime values, sources, and whether the proposed fallback path would call a `None`-returning factory twice.

**Keep both presence checks.** The proposal would change default resolution: explicit map `None` would fall back to the parameter default, and a factory returning `None` would run twice and receive the wrong parameter source.

The helper pays for a real policy distinction: absent entries and stored `UNSET` mean “continue”; explicit `None` means “use this map value.” Public `lookup_default()` returns `None` for both absence and explicit `None`, so its return value alone cannot decide presence. See [the presence policy and public lookup](project/src/click/core.py#L766).

**Executed against the unchanged checkout:** all **46 tests** in `tests/test_defaults.py` passed. I used the supplied interpreter with `-B`, `PYTHONPATH=src`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and `-p no:cacheprovider`, retaining project settings. Runtime assertions confirmed both `click` and `click.core` imported this repository’s `src/click`.

CliRunner observations used a string `--name`, `default='fallback'`, and explicit `envvar='LANDLORD_REVIEW_NAME'`. Environment values were isolated per invocation.

| Inputs | Callback value | Parameter source | Factory calls |
|---|---|---|---:|
| CLI + environment + map string | `'cli'` | `COMMANDLINE` | 0 |
| Environment + map string | `'env'` | `ENVIRONMENT` | 0 |
| Map string | `'mapped'` | `DEFAULT_MAP` | 0 |
| Map `None` | `None` | `DEFAULT_MAP` | 0 |
| Map empty string | `''` | `DEFAULT_MAP` | 0 |
| Map zero | `'0'` | `DEFAULT_MAP` | 0 |
| Missing map entry | `'fallback'` | `DEFAULT` | 0 |
| No map | `'fallback'` | `DEFAULT` | 0 |
| Stored `UNSET` | `'fallback'` | `DEFAULT` | 0 |
| Map factory returning `None` | `None` | `DEFAULT_MAP` | 1 |
| CLI + environment + map factory | `'cli'` | `COMMANDLINE` | 0 |
| Environment + map factory | `'env'` | `ENVIRONMENT` | 0 |

The help control displayed `[default: (dynamic)]` with **zero factory calls**; it did not invoke the callback.

**Static inference about the proposal—not execution of modified code:**

- Explicit map `None` would fail the simplified `consume_value` condition, then fail the simplified `get_default` condition, yielding `'fallback' / DEFAULT`.
- A factory returning `None` would first run in `consume_value`. Resolution would then enter `get_default`, retrieve the callable with `call=False`, and invoke it again. Result: `None / DEFAULT`, **two calls**.
- The other table controls would retain their outcomes.

These follow directly from [the two resolution paths](project/src/click/core.py#L2496). Existing [source assertions for explicit `None`](project/tests/test_defaults.py#L238) and [map overrides of callable flag defaults](project/tests/test_defaults.py#L476) would therefore regress.

This policy also serves actual callers beyond parsing: [command invocation](project/src/click/core.py#L894), [help rendering](project/src/click/core.py#L3448), and [prompt defaults](project/src/click/core.py#L3514).

For a concrete future maintenance scenario, consider adding a JSON configuration loader where `"name": null` clears a configured default, while an omitted key preserves `'fallback'`. Today the loader can pass that distinction directly through `default_map`. With this proposal, maintainers would need special handling in the loader or restore presence-aware resolution; wrapping null in a factory would still mislabel its source and execute twice. Repairing parsing alone would leave help and direct invocation inconsistent.

The nearest viable alternative is to retain the shared predicate and explain these two checks with comments. If consolidation becomes necessary, a private adapter returning `(found, value)` could combine lookup and presence handling. It must still dispatch through public `lookup_default`, preserve `call=False`, and honor [the tested subclass override contract](project/tests/test_defaults.py#L422). That additional machinery is not justified here.

Repository content, file modes, HEAD/index, and skill resources remained unchanged. Owned scratch was removed; no permanent tests or report were created.
