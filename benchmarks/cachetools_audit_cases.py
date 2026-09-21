"""Authored audit over pinned, unmodified upstream cachetools source/tests."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'benchmarks/fixtures/cachetools-5.5.2'
TARGET = 'cachetools/__init__.py'
SELECTORS = ['tests.test_lru.LRUCacheTest.test_lru', 'tests.test_lru.LRUCacheTest.test_lru_getsizeof']
FAULTS = {
    'read-recency': ('        if key in self:  # __missing__ may not store item\n            self.__update(key)\n', ''),
    'overwrite-recency': ('        cache_setitem(self, key, value)\n        self.__update(key)\n',
                          '        existed = key in self\n        cache_setitem(self, key, value)\n        if not existed:\n            self.__update(key)\n'),
    'newest-eviction': ('key = next(iter(self.__order))', 'key = next(reversed(self.__order))'),
    'ignored-size': ('Cache.__init__(self, maxsize, getsizeof)', 'Cache.__init__(self, maxsize)'),
}
WITNESSES = {
    'read-recency': "c=LRUCache(2);c['a']=1;c['b']=2;c['a'];c['c']=3;assert 'a' in c and 'b' not in c",
    'overwrite-recency': "c=LRUCache(2);c['a']=1;c['b']=2;c['a']=9;c['c']=3;assert 'a' in c and 'b' not in c",
    'newest-eviction': "c=LRUCache(2);c['a']=1;c['b']=2;c['c']=3;assert 'a' not in c and 'b' in c",
    'ignored-size': "c=LRUCache(3,getsizeof=len);c['a']='aa';c['b']='bb';assert 'a' not in c and list(c.values())==['bb'] and c.currsize==2",
}


def source_files():
    manifest = json.loads((FIXTURE / 'SOURCE.json').read_text())
    files = {}
    for item in manifest['files']:
        content = (FIXTURE / item['local']).read_bytes()
        identity = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
        if identity != item['sha'] or len(content) != item['size']:
            raise ValueError('Upstream fixture drift: ' + item['local'])
        files[item['local']] = content.decode()
    files['SOURCE.json'] = (FIXTURE / 'SOURCE.json').read_text()
    return files


def revise(source, name):
    start, end = source.index('class LRUCache(Cache):'), source.index('class MRUCache(Cache):')
    section = source[start:end]
    old, new = FAULTS[name] if name != 'equivalent' else ('next(iter(self.__order))', 'next(iter(self.__order.keys()))')
    if section.count(old) != 1:
        raise ValueError('Expected one LRU-scoped mutation anchor')
    return source[:start] + section.replace(old, new) + source[end:]


def cases():
    files = source_files()
    files['AGENTS.md'] = (
        'Audit only. Preserve every original source/test/license/metadata file and mode. '
        'No dependencies, network, commits or production changes. Use disposable copies inside '
        'this project and remove only your own copies afterward. Native tests run from a copy root '
        'with python3 -B -m unittest <selector> -v. Tests import the local cachetools package; '
        'establish the actual copied import and assertion results. No permanent harness/report.\n')
    task = (
        'Audit the two existing native tests tests.test_lru.LRUCacheTest.test_lru and '
        'tests.test_lru.LRUCacheTest.test_lru_getsizeof against four independent LRUCache regressions: '
        '(1) reading an existing key does not refresh recency, (2) overwriting an existing key does '
        'not refresh recency while new insertions still enter the order, (3) eviction removes the '
        'most-recent instead of least-recent key, (4) the constructor ignores the supplied getsizeof. '
        'Keep each regression isolated; do not change other cache classes or test bodies. '
        'For each of the eight fault/test combinations, establish correct-code success and the '
        'faulty copied test outcome, identify a detecting assertion/failure path or surviving gap, and distinguish '
        'setup errors from behavioral detection. Show the eight results clearly, explain any '
        'unprotected behavior and suggest a focused assertion for it. You may reuse matching '
        'correct-code observations within this audit if you identify that reuse; fresh external '
        'state is not required. Tool choice and execution grouping are yours. Follow AGENTS.md.')
    return [dict(id='cachetools-lru-four-faults', skill='con-artist', files=files, task=task,
        criteria=[
            'Both unchanged selected tests have actual passing correct-code observations tied to the copied local implementation.',
            'All four isolated semantic faults alter only LRUCache as requested, with no syntax/import failure counted as detection.',
            'All eight fault/test outcomes are established by actual unchanged native tests and correctly interpreted; reused normal results are not independent executions.',
            'Surviving behavior has a concrete contract-distinguishing assertion proposal; do not claim the two tests prove all LRU behavior.',
            'Original bytes/modes preserved, scope respected, owned project-local scratch removed; no production fix or permanent artifact.'])]


def preflight():
    original = source_files()
    rows = []
    with tempfile.TemporaryDirectory(prefix='cachetools-author-') as temporary:
        for variant in ['correct', 'equivalent', *FAULTS]:
            copy = Path(temporary) / variant
            for name, text in original.items():
                path = copy / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(revise(text, variant) if name == TARGET and variant != 'correct' else text)
            def execute(argv):
                result = subprocess.run([sys.executable, '-B', *argv], cwd=copy, capture_output=True, text=True, timeout=5)
                return dict(exit_code=result.returncode, output=(result.stdout + result.stderr).replace(str(copy.resolve()), '<COPY>').replace(str(copy), '<COPY>'))
            selected = [execute(['-m', 'unittest', selector, '-v']) for selector in SELECTORS]
            # A behavioral KeyError inside the unchanged test is detection, not
            # import/setup failure merely because unittest labels it ERROR.
            assert all('Ran 1 test' in r['output'] and r['exit_code'] in (0, 1)
                       and not any(s in r['output'] for s in ('ImportError', 'ModuleNotFoundError', 'SyntaxError', '_FailedTest'))
                       for r in selected), selected
            if variant in ('correct', 'equivalent'):
                full = execute(['-m', 'unittest', 'tests.test_lru', '-v'])
                assert full['exit_code'] == 0 and 'Ran 15 tests' in full['output'], full
                witness = execute(['-c', 'from cachetools import LRUCache\n' + '\n'.join(WITNESSES.values())])
                assert witness['exit_code'] == 0, witness
            else:
                full = None
                witness = execute(['-c', 'from cachetools import LRUCache\n' + WITNESSES[variant]])
                assert witness['exit_code'] == 1 and 'AssertionError' in witness['output'], witness
            rows.append(dict(variant=variant, selected=selected, full_suite=full, behavioral_witness=witness,
                implementation_sha256=hashlib.sha256((copy / TARGET).read_bytes()).hexdigest()))
    return rows
