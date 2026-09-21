"""Supplementary author observation: no new model run, no fixture rewrite."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

PROBE = '''import asyncio
import json
from pathlib import Path
import shared
assert Path(shared.__file__).resolve() == Path('shared.py').resolve()

async def main():
    calls, observed = [], []
    late = None
    async def join():
        observed.append(loader._inflight['key'].done())
        return await loader.load('key')
    async def fetch(key):
        nonlocal late
        value = {'request': len(calls) + 1}
        calls.append(value)
        if len(calls) == 1:
            # Ready callback order: this new caller is queued before the fetch's
            # done callbacks, but executes after the fetch has returned.
            late = asyncio.create_task(join())
        return value
    loader = shared.Loader(fetch)
    first = await loader.load('key')
    second = await late
    print(json.dumps(dict(calls=len(calls), first=first, second=second,
        original_fetch_already_done=observed, same_object=first is second)), flush=True)
    assert observed == [True], 'Probe did not establish completed-fetch window'
    assert len(calls) == 2 and first is not second, 'Completed fetch result reused by a new caller'
asyncio.run(main())
'''


def observe(source, python=sys.executable):
    with tempfile.TemporaryDirectory(prefix='qh-completed-fetch-') as folder:
        root = Path(folder)
        (root / 'shared.py').write_bytes(Path(source).read_bytes())
        result = subprocess.run([str(python), '-B', '-c', PROBE], cwd=root,
                                capture_output=True, text=True, timeout=5)
        return dict(exit_code=result.returncode, output=result.stdout,
                    stderr=result.stderr, limitation='Post-run author probe, not original model evidence.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    print(json.dumps(observe(parser.parse_args().source), indent=2))
