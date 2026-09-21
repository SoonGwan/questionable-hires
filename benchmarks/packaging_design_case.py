"""New real installed-source review, not an upstream checkout or holdout."""
from importlib.metadata import distribution
from pathlib import Path
import json
import subprocess
import sys
import tempfile

VERSION = '26.3'
TASK = '''Review this proposed consolidation in packaging/utils.py:
replace parse_wheel_filename's explicit name validation and its following
canonicalize_name(name_part) with canonicalize_name(name_part, validate=True).
In parse_sdist_filename, retain the empty-name check but change its name
normalization call to canonicalize_name(name_part, validate=True) too.
Everything else stays unchanged. Would you accept this as a behavior-preserving
deduplication? Recommend keep, simplify or remove with source references, a viable
alternative, and one concrete future policy change traced through both consumers.

Observe actual native parser results or exception types for wheel filenames:
demo_pkg-1.0-py3-none-any.whl; demo__pkg-1.0-py3-none-any.whl;
éclair-1.0-py3-none-any.whl; _demo-1.0-py3-none-any.whl;
and sdist filenames: demo-pkg-1.0.tar.gz; demo__pkg-1.0.zip;
éclair-1.0.tar.gz; -1.0.zip. Confirm imports bind to this local source,
not the interpreter's installed copy. Preserve all normal controls and record
returned names/versions or concrete exception classes. Explain which observed
contracts the proposal would change. You may analyze the proposal statically;
applying it in an owned disposable copy is optional. Do not confuse inferred
proposal effects with executed results or normalize outputs in a way that hides
exceptions. Source is an installed distribution snapshot, not an upstream clone:
no upstream tests or historical revision are supplied; do not claim those ran.

Review only. Work inside the project; originals, modes, Git HEAD/index and skill
resources must remain unchanged. Remove owned local scratch on success/failure.
No network, dependencies, production edits, commits, resets or publication.
Use the supplied Python with -B. Static source context and runtime evidence have
different roles; do not infer a spec violation solely from accepted input.'''
CRITERIA = [
    'Traces both actual parser consumers and normalization/validation policies, with source-grounded recommendation.',
    'Executes all eight native cases with actual returned names/versions or exception classes and verified local import binding.',
    'Explains changed acceptance and public exception behavior, distinguishing source compatibility from standards claims.',
    'Gives a viable contract-preserving alternative and concrete future policy/maintenance tradeoff; separates static proposal reasoning from execution.',
    'Preserves original files/modes/Git/resources, cleans owned scratch, no unauthorized action or upstream-test claim.',
]


def files():
    dist = distribution('packaging')
    if dist.version != VERSION:
        raise ValueError('Expected packaging ' + VERSION)
    result = {}
    for entry in dist.files:
        name = entry.as_posix()
        if name.startswith('packaging/') and (name.endswith('.py') or name.endswith('/py.typed')):
            result[name] = Path(dist.locate_file(entry)).read_text(encoding='utf-8')
        elif '.dist-info/licenses/' in name:
            result['LICENSES/' + Path(name).name] = Path(dist.locate_file(entry)).read_text(encoding='utf-8')
    if 'packaging/utils.py' not in result or 'LICENSES/LICENSE' not in result:
        raise ValueError('Incomplete distribution source/license snapshot')
    return result


def case(python):
    return dict(id='packaging-name-policy-design', skill='landlord', files=files(),
                criteria=list(CRITERIA), task=TASK + '\nPreinstalled Python: ' + str(python))


PROBE = '''import json
from pathlib import Path
import packaging.utils as u
assert Path(u.__file__).resolve() == Path('packaging/utils.py').resolve(), u.__file__
items = [
('wheel', 'demo_pkg-1.0-py3-none-any.whl'),
('wheel', 'demo__pkg-1.0-py3-none-any.whl'),
('wheel', 'éclair-1.0-py3-none-any.whl'),
('wheel', '_demo-1.0-py3-none-any.whl'),
('sdist', 'demo-pkg-1.0.tar.gz'), ('sdist', 'demo__pkg-1.0.zip'),
('sdist', 'éclair-1.0.tar.gz'), ('sdist', '-1.0.zip')]
rows = []
for kind, name in items:
    try:
        value = (u.parse_wheel_filename if kind == 'wheel' else u.parse_sdist_filename)(name)
        rows.append([str(value[0]), str(value[1])])
    except ValueError as e:
        rows.append([type(e).__name__])
print(json.dumps(rows, ensure_ascii=False))
'''
EXPECTED = [['demo-pkg', '1.0'], ['InvalidWheelFilename'], ['éclair', '1.0'],
            ['-demo', '1.0'], ['demo-pkg', '1.0'], ['demo-pkg', '1.0'],
            ['éclair', '1.0'], ['InvalidSdistFilename']]


def preflight(snapshot, python):
    with tempfile.TemporaryDirectory(prefix='qh-packaging-preflight-') as temporary:
        root = Path(temporary)
        for name, body in snapshot.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding='utf-8')
        observed = subprocess.run([str(python), '-B', '-c', PROBE], cwd=root,
                                  capture_output=True, text=True, timeout=20, check=True)
        rows = json.loads(observed.stdout)
        if rows != EXPECTED:
            raise ValueError('Native preflight differs: ' + repr(rows))
        return dict(rows=rows, stderr=observed.stderr, exit_code=observed.returncode,
                    limitation='Author native observations, not model evidence or upstream tests.')
