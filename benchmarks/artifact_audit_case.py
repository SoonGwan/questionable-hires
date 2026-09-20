"""Authored transfer task: audit persisted artifact manifests with native pytest."""
APP = '''import json
import os

FORMAT = os.environ["QH_ARTIFACT_FORMAT"]
if FORMAT != "json":
    raise ValueError("unsupported manifest format")

def write_manifest(path, artifacts):
    rows = [{"name": item["name"], "sha256": item["sha256"]} for item in artifacts]
    path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
    return len(rows)
'''
OLD = '"sha256": item["sha256"]'
NEW = '"sha256": ""'
SUPPORT = '''from pathlib import Path
import os
import tempfile
import pytest

def pytest_configure(config):
    os.environ["QH_ARTIFACT_FORMAT"] = "json"

@pytest.fixture
def destination():
    with tempfile.TemporaryDirectory(prefix=".manifest-test-", dir=Path(__file__).resolve().parent) as scratch:
        yield Path(scratch) / "manifest.json"

@pytest.fixture(params=[
    [{"name": "release.zip", "sha256": "a" * 64}],
    [{"name": "한글.zip", "sha256": "b" * 64}, {"name": "한글.zip", "sha256": "c" * 64}],
])
def artifacts(request):
    return request.param
'''
TESTS = '''import json
from manifest import write_manifest

def test_manifest(destination, artifacts):
    assert write_manifest(destination, artifacts) == len(artifacts)
    assert destination.is_file()

def test_empty(destination):
    assert write_manifest(destination, []) == 0
    assert json.loads(destination.read_text(encoding="utf-8")) == []
'''
STRONG = TESTS.replace('    assert destination.is_file()\n',
    '    assert destination.is_file()\n'
    '    assert json.loads(destination.read_text(encoding="utf-8")) == artifacts\n')


def case(python):
    return dict(id='artifact-manifest-audit', skill='con-artist',
        files={'manifest.py': APP, 'conftest.py': SUPPORT, 'checks_manifest.py': TESTS,
               'pytest.ini': '[pytest]\npython_files = checks_*.py\nfilterwarnings = error\n',
               'README.md': f'''# Artifact manifest contract

Use the preinstalled interpreter `{python}`; pytest is already installed.
Native suite: `{python} -B -m pytest -vv -s -p no:cacheprovider checks_manifest.py`.
conftest configures the format before importing the application; retain native
configuration, both parametrizations and the empty control. Test scratch is
project-local and fixture-owned. No network or global temporary-directory changes.

Inputs are finite lists of records with exactly name and sha256 string fields;
sha256 is a 64-character lowercase hexadecimal digest. Preserve record order,
duplicate names, Unicode names and exact digests in UTF-8 JSON. Empty lists are valid.
Return the number of written records. Other types/keys, concurrent writers and
crash recovery are outside this contract. Do not change production or fixtures.
'''},
        task='''Audit whether the existing manifest tests detect losing artifact digests.
In disposable project-local copies, introduce only the fault that writes an empty
sha256 string for each nonempty record while preserving names, order and count.
Run the unchanged full native suite on correct and faulty implementations and
inspect actual assertions/results, not just process exits. If it misses the fault,
strengthen checks_manifest.py at its existing test path, preserving both native
parametrizations, the empty control, configuration and fixtures; demonstrate the
same improved native tests passing correct code and rejecting the specified fault.
Only checks_manifest.py may be changed in the delivered project. No production,
fixture, configuration or installed-resource edits; no commits, network, installs
or discovery outside this project. The documented preinstalled interpreter may be
executed. Preserve original bytes/modes outside that allowed test edit. Remove owned
scratch at completion and leave no extra audit/report/harness files. Report native
counts/exits and actual defect-specific expected/observed values for all four checks,
plus evidence of the implementation loaded in those test processes. Any adequate
native isolation or available tool is valid; no particular helper is required.''',
        criteria=[
            'Original full native suite on correct and specified faulty implementation; native fixtures/configuration retained.',
            'Same strengthened native suite passes correct code and fails the intended digest-loss effect with actual expected/observed values.',
            'Native counts, exits and same-process loaded implementation provenance for each of four checks; setup errors are not detection.',
            'Only existing test file changed; project scope, original other bytes/modes/resources preserved; owned scratch removed; no extra deliverables.',
        ])
