"""Expose the optional callback asset's actual contract before loading its guide."""

OLD = '''Only when additional
  Python request-control support is needed, read the [native-test interface](references/native-tests.md)
  and [copiable transport](assets/controlled_fetch.py) together.'''
NEW = '''For missing `async fetch(key)` response control, read the
  [native-test interface](references/native-tests.md) and
  [copiable transport](assets/controlled_fetch.py) together. The asset observes entry
  and settles each returned value/error; it does not implement callback-side effects.
  If those effects need a custom fixture anyway, prefer minimal native support
  unless adapting the asset removes needed setup.'''


def entry(source):
    if NEW in source and OLD not in source:
        return source
    if source.count(OLD) != 1 or NEW in source:
        raise ValueError('Expected the frozen Mother optional-support route')
    return source.replace(OLD, NEW, 1)
