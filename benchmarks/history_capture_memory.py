"""Native Git capture prototype: Python allocations, not model or RSS evidence."""
import argparse
import codecs
import gc
import hashlib
import importlib.util
import json
import mmap
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import tracemalloc

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('capture_reference', ROOT / 'skills/necromancer/scripts/trace.py')
helper = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(helper)


def spooled_git(repo, *args):
    """Prototype only: two temporary files; full decoded strings still retained."""
    command = ['git', '--no-pager', '--no-optional-locks', '--literal-pathspecs',
               '-c', 'core.fsmonitor=false', '-c', 'core.quotePath=false', *args]
    with tempfile.TemporaryFile(dir=repo) as stdout, tempfile.TemporaryFile(dir=repo) as stderr:
        result = subprocess.run(command, cwd=repo, stdout=stdout, stderr=stderr, timeout=20)
        def decoded(stream):
            if stream.tell() == 0:
                return ''
            with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
                return codecs.decode(mapped, 'utf-8')
        result.stdout, result.stderr = decoded(stdout), decoded(stderr)
        return result


def observation(call):
    try:
        result = call()
        return dict(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr)
    except UnicodeDecodeError as error:
        return dict(error='UnicodeDecodeError', encoding=error.encoding,
                    start=error.start, end=error.end, reason=error.reason)


def measure():
    result = dict(python=sys.version, git_version=subprocess.check_output(['git', '--version'], text=True).strip(),
                  source_revision=subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  helper_sha256=hashlib.sha256((ROOT/'skills/necromancer/scripts/trace.py').read_bytes()).hexdigest(),
                  prototype_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), cases={})
    with tempfile.TemporaryDirectory(prefix='history-capture-', dir=ROOT/'benchmarks') as temporary:
        repo = Path(temporary)
        def git(*args):
            subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false', *args],
                           cwd=repo, check=True, capture_output=True, timeout=30)
        git('init', '-q')
        git('config', 'user.name', 'Native fixture')
        git('config', 'user.email', 'fixture@example.invalid')
        (repo/'small.py').write_bytes('first = "한글"\r\nsecond = 2\r\n'.encode())
        (repo/'large.py').write_bytes(b'# historical row with padding 0123456789\n' * 400_000)
        (repo/'invalid.py').write_bytes(b'value = "\xff"\n')
        git('add', '.')
        git('commit', '-qm', 'Native historical source')
        initial = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
        (repo/'large.py').write_text('value = 1\n')
        git('add', 'large.py')
        git('commit', '-qm', 'Replace long historical source')
        show = ('show', '--no-ext-diff', '--no-textconv', '--no-color', '--format=commit %H%n%B', '--unified=3')
        cases = {'small_crlf_unicode': (*show, initial, '--', 'small.py'),
                 'large_removed_history': (*show, 'HEAD', '--', 'large.py'),
                 'invalid_utf8_history': (*show, initial, '--', 'invalid.py'),
                 'missing_revision': ('show', '--no-ext-diff', '--no-textconv', 'no-such-revision', '--', 'small.py')}
        for label, args in cases.items():
            functions = {'current': lambda: helper.git(repo, *args), 'spooled': lambda: spooled_git(repo, *args)}
            samples = {name: [] for name in functions}
            observations = {}
            for index in range(4):
                for name in (('current', 'spooled') if index % 2 == 0 else ('spooled', 'current')):
                    start = time.perf_counter()
                    value = observation(functions[name])
                    samples[name].append(time.perf_counter()-start)
                    if name in observations and observations[name] != value:
                        raise AssertionError('Native output changed across observations')
                    observations[name] = value
            if observations['current'] != observations['spooled']:
                raise AssertionError('Decoded evidence or error differs')
            observed = observations['current']
            peaks = {}
            for name in functions:
                gc.collect()
                tracemalloc.start()
                try:
                    observation(functions[name])
                    peaks[name] = tracemalloc.get_traced_memory()[1]
                finally:
                    tracemalloc.stop()
            result['cases'][label] = dict(equal=True, native_exit=observed.get('exit_code'), error=observed.get('error'),
                stdout_characters=len(observed.get('stdout','')), stderr_characters=len(observed.get('stderr','')),
                observation_sha256=hashlib.sha256(json.dumps(observed, ensure_ascii=False).encode()).hexdigest(),
                samples_seconds=samples, median_seconds={k:statistics.median(v) for k,v in samples.items()},
                peak_traced_bytes=peaks)
        result['owned_fixture_removed_after_return'] = True
    result['limitation'] = ('Author-owned native Git fixture; four alternating timing pairs plus one separately traced call per arm/case. '
        'Shared host/cache, no RSS/child/disk/model-token measure. Full decoded strings remain allocated. '
        'Prototype writes two temporary files and memory maps them; not a read-only-workspace-compatible drop-in. '
        'No timeout/concurrent-child or whole-collector equivalence validation; not adopted.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output exists; retain the previous observation')
    value = measure()
    with args.output.open('x') as stream:
        json.dump(value, stream, indent=2)
        stream.write('\n')
    for name, row in value['cases'].items():
        print(name, row['peak_traced_bytes'], row['median_seconds'], row['error'] or row['native_exit'])
