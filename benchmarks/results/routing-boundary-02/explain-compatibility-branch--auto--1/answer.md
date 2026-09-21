I’ll read `display.py` and check how the compatibility branch handles missing and empty names.

In [display.py](project/display.py), the results are:

| Input | Return value |
|---|---|
| `{}` | `'Anonymous'` |
| `{'name': ''}` | `''` (empty string) |
| `{'name': 'Ada'}` | `'Ada'` |

The compatibility branch checks whether the `'name'` key is **missing**. An empty name still has that key, so it bypasses the branch and returns the empty string unchanged.
