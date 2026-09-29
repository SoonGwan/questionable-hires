"""Isolated optional delayed-serialization asset, reusing an existing fixture."""
from pathlib import Path

OLD = '''Only when additional
  Python request-control support is needed, read the [native-test interface](references/native-tests.md)
  and [copiable transport](assets/controlled_fetch.py) together.'''
NEW = '''For missing Python test support, choose the relevant interface:
  [controlled writes](assets/controlled_writes.py) observes the actual callback
  argument and deep-copies it only after acknowledgment, with owned task cleanup;
  response-control tests use the [native-test interface](references/native-tests.md)
  and [copiable transport](assets/controlled_fetch.py). Copy support only when it
  removes needed setup and project edits permit it.'''


def entry(source):
    if NEW in source and OLD not in source:
        return source
    if source.count(OLD) != 1 or NEW in source:
        raise ValueError('Expected the ordinary Mother support route')
    return source.replace(OLD, NEW, 1)


def install_candidate(skill):
    skill = Path(skill)
    path = skill / 'SKILL.md'
    path.write_text(entry(path.read_text()))
    asset = Path(__file__).with_name('candidates') / 'mother-writes01/controlled_writes.py'
    (skill / 'assets/controlled_writes.py').write_bytes(asset.read_bytes())
