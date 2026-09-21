I’ll inspect the default-resolution paths and tests, then run the existing tests and a CliRunner probe with the supplied interpreter. I’ll keep the checkout unchanged and distinguish observed behavior from static inference about the proposal.

The helper preserves a distinction that `lookup_default()` alone cannot express: a present map value of `None` versus a missing entry. Existing tests explicitly cover that policy and stored `UNSET`. I’ll now check runtime values, parameter sources, and whether falling through would invoke a factory twice.

**Keep both guards and `_default_map_has`. The proposed simplification changes default resolution.** It conflates an explicit map value of `None` with an absent value.

Executed against this checkout:

- All **46 tests in `tests/test_defaults.py` passed**.
- Used the supplied interpreter with `-B`, `PYTHONPATH=src`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, and `-p no:cacheprovider`; retained `pyproject.toml` settings.
- Asserted that `click.__file__` and `click.core.__file__` resolve to this repository’s `src/click/__init__.py` and `src/click/core.py`.

The native CliRunner probe used `--name`, `type=str`, `default='fallback'`, and explicit `envvar='CLICK_REVIEW_NAME'`. Environment absence was controlled through CliRunner’s in-process isolation.

| Inputs | Observed value | Observed source | Factory calls |
|---|---|---|---:|
| CLI + environment + map | `'cli'` | `COMMANDLINE` | 0 |
| Environment + map | `'environment'` | `ENVIRONMENT` | 0 |
| Map `'mapped'` | `'mapped'` | `DEFAULT_MAP` | 0 |
| Map `None` | `None` | `DEFAULT_MAP` | 0 |
| Map `''` | `''` | `DEFAULT_MAP` | 0 |
| Map `0` | `'0'` | `DEFAULT_MAP` | 0 |
| Missing map entry | `'fallback'` | `DEFAULT` | 0 |
| No map | `'fallback'` | `DEFAULT` | 0 |
| Stored `click._utils.UNSET` | `'fallback'` | `DEFAULT` | 0 |
| Map factory returning `None` | `None` | `DEFAULT_MAP` | **1** |
| CLI + environment + map factory | `'cli'` | `COMMANDLINE` | **0** |
| Environment + map factory | `'environment'` | `ENVIRONMENT` | **0** |

The following consequences of the proposal are **static inference**, not execution of modified code:

- **Explicit `None`:** `consume_value` would reject the map result; `get_default` would then replace it with `'fallback'`. Both value and source change.
- **Factory returning `None`:** `consume_value` would call it once and fall through. `get_default(call=False)` retrieves the callable, which is subsequently invoked again. Result: `None`, source **`DEFAULT`**, and **two calls**. A stateful factory could also produce a different value on its second invocation.
- The other table rows retain their results. In particular, `is not None` still accepts empty strings and zero; CLI and environment retain precedence.

These distinctions are deliberate policy. [`_default_map_has`](project/src/click/core.py#L766) treats missing entries and stored `UNSET` as absent, while accepting explicit `None`. [`lookup_default`](project/src/click/core.py#L790) returns `None` for absence, so its return value alone cannot convey presence. Existing tests explicitly require [`None` to have source `DEFAULT_MAP`](project/tests/test_defaults.py#L239) and [`UNSET` to fall back](project/tests/test_defaults.py#L551).

The guards serve different callers:

- [`consume_value`](project/src/click/core.py#L2509) implements runtime precedence and assigns provenance, which [`handle_parse_result`](project/src/click/core.py#L2780) exposes before conversion and callbacks.
- [`get_default`](project/src/click/core.py#L2473) also serves [`Context.invoke`](project/src/click/core.py#L896), help rendering through [`Option.get_default`](project/src/click/core.py#L3246) and [`get_help_extra`](project/src/click/core.py#L3449), and prompting. Removing its guard independently changes those paths—for example, help with `show_default=True` could display the fallback when the map explicitly supplies `None`.

A concrete future maintenance change illustrates why the shared policy matters: suppose configuration loading introduces an `INHERIT` marker that should behave like an absent entry. With the current design, excluding that marker in `_default_map_has` updates all three consumers: `lookup_default` hides it, `get_default` permits fallback, and `consume_value` avoids assigning `DEFAULT_MAP`. Explicit `None` remains meaningful. Separate presence checks would require coordinated edits and risk inconsistent help, runtime values, and provenance.

A viable larger refactor is a **private presence-aware adapter returning `(present, value)`**, shared by both parameter methods. It should call the overridable `ctx.lookup_default(name, call=...)`, retain the current presence policy, and preserve callable evaluation timing. Keep the public lookup API unchanged: the existing [`CustomContext` regression test](project/tests/test_defaults.py#L422) requires overrides to work for both execution and help. Directly reading the map or exposing `UNSET` publicly would undermine that compatibility.

No source changes were made. Before/after content and mode snapshots, including Git metadata, matched; HEAD remained `6aabf099bfdd4c1e75fe8d0e0d4241372b988ab1`, and Git status stayed clean. Owned project-local scratch was removed. No skills, external services, or dependencies were used.
