"""Fresh authored ZIP audit tasks; native controls, not model performance."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
WRITER = '''import io
import stat
import zipfile


def pack(records):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as archive:
        for name, payload, permissions in records:
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | permissions) << 16
            archive.writestr(info, payload)
    return buffer.getvalue()
'''
ENDPOINT = '''from releasekit.writer import pack as _pack


def create_package(records):
    return _pack(records)
'''
TESTS = '''import io
import unittest
import zipfile
from releasekit import create_package as build


class PackageTests(unittest.TestCase):
    def test_entries_and_crc(self):
        records = [('bin/launch', b'\\x00\\xfflaunch', 0o755),
                   ('etc/settings', b'', 0o640)]
        with zipfile.ZipFile(io.BytesIO(build(records))) as archive:
            self.assertEqual(archive.namelist(), ['bin/launch', 'etc/settings'])
            self.assertIsNone(archive.testzip())

    def test_empty_package(self):
        with zipfile.ZipFile(io.BytesIO(build([]))) as archive:
            self.assertEqual(archive.namelist(), [])
            self.assertIsNone(archive.testzip())
'''
CONTRACT = '''Python3.9+ standard library only. Run python3 -B -m unittest -v test_package.
create_package accepts an ordered list of distinct relative POSIX file names,
bytes payloads (including binary and empty bytes), and integer permission bits
between 0 and 0o777. Inputs are already validated; path validation and extraction
are not in scope. It returns ZIP bytes with exactly that entry order, exact bytes,
Unix creator system3 and each supplied Unix permission value. An empty list returns
a valid empty archive. Do not modify the caller's list or tuples. Inputs are regular
files only; directory/symlink entries and filesystem extraction are not supported.
For this audit, all supplied source/test/requirements files are immutable. Isolated
project-local copies and temporary added tests are allowed; remove owned scratch
before finishing. No external resources, installation, delegation or publication.
'''
FAULTS = {
    'permissions': dict(target='releasekit/writer.py',
                        old='            info.external_attr = (stat.S_IFREG | permissions) << 16\n', new=''),
    'payload': dict(target='releasekit/writer.py', old='            archive.writestr(info, payload)\n',
                    new="            archive.writestr(info, b'')\n"),
}
STRONG = '''import io
import stat
import unittest
import zipfile
from releasekit import create_package as build


class PersistenceTests(unittest.TestCase):
    def test_complete_archive_records(self):
        records = [('bin/launch', b'\\x00\\xfflaunch', 0o755),
                   ('etc/settings', b'', 0o640)]
        original = list(records)
        produced = build(records)
        self.assertEqual(records, original)
        with zipfile.ZipFile(io.BytesIO(produced)) as archive:
            observed = [(i.filename, archive.read(i), stat.S_IMODE(i.external_attr >> 16),
                         i.create_system) for i in archive.infolist()]
        self.assertEqual(observed, [('bin/launch', b'\\x00\\xfflaunch', 0o755, 3),
                                    ('etc/settings', b'', 0o640, 3)])
'''


def cases():
    shared = '''Inspect the actual tests, public package entrypoint and writer. Audit
whether the native tests detect the specified reachable fault(s), in isolation.
Execute existing native tests on correct code and each faulty version; keep each
fault independent, not combined. Verify the actual test's build binding and the
endpoint's _pack binding in the same process as the checks. If an existing test
survives, execute the same stronger native assertion against correct code and that
fault: reopen the bytes returned by the real create_package, compare complete
ordered (filename, payload bytes, permission bits, Unix creator system) records
for the existing binary and empty entries, and verify input preservation.
Show normal passes and defect-specific assertion failures, not import/setup errors.
Preserve original bytes/modes and remove owned project-local disposable copies.
Commands/results suffice; do not retain a permanent harness/report or apply repairs.
Work only inside this project, with no network, dependencies, external discovery,
other skills, delegation or publication.'''
    files = {'releasekit/__init__.py': 'from .endpoint import create_package\n',
             'releasekit/endpoint.py': ENDPOINT, 'releasekit/writer.py': WRITER,
             'test_package.py': TESTS, 'requirements.md': CONTRACT}
    requests = [('zip-audit-single', 'Omit only the external_attr assignment in pack; keep payload writing unchanged.'),
                ('zip-audit-multiple', 'Check two independent faults in pack: omit only the external_attr assignment; '
                 "separately replace writestr(info, payload) with writestr(info, b'') while preserving metadata.")]
    return [dict(id=identity, skill='con-artist', files=dict(files), task=request + '\n\n' + shared,
                 criteria=['Inspect real sources and prove same-process test/endpoint/writer bindings.',
                           'Execute normal and each independently requested fault with the original native tests.',
                           'Verify the same stronger complete-record native assertion on normal and surviving faults, including input preservation.',
                           'Preserve originals and remove owned scratch without scope expansion.'])
            for identity, request in requests]


def preflight():
    observations = []
    for variant in ('correct', 'permissions', 'payload'):
        with tempfile.TemporaryDirectory(prefix='zip-audit-control-', dir=ROOT / 'benchmarks') as directory:
            project = Path(directory)
            for name, content in cases()[0]['files'].items():
                path = project / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
            if variant != 'correct':
                fault = FAULTS[variant]
                assert WRITER.count(fault['old']) == 1
                (project / fault['target']).write_text(WRITER.replace(fault['old'], fault['new']))
            (project / 'test_complete.py').write_text(STRONG)
            before = {str(p.relative_to(project)): (p.read_bytes(), p.stat().st_mode) for p in project.rglob('*') if p.is_file()}
            imported = subprocess.run([sys.executable, '-B', '-c', 'import releasekit; assert callable(releasekit.create_package)'],
                                      cwd=project, text=True, capture_output=True, timeout=10)
            assert imported.returncode == 0, imported.stderr
            for module, count in (('test_package', 2), ('test_complete', 1)):
                program = '''import unittest
import releasekit, releasekit.endpoint, releasekit.writer, test_package, test_complete
assert test_package.build is releasekit.create_package is releasekit.endpoint.create_package
assert test_complete.build is releasekit.create_package
assert releasekit.endpoint.create_package.__globals__['_pack'] is releasekit.writer.pack
suite = unittest.defaultTestLoader.loadTestsFromName(MODULE)
assert suite.countTestCases() == COUNT
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
'''.replace('MODULE', repr(module)).replace('COUNT', str(count))
                proc = subprocess.run([sys.executable, '-B', '-c', program], cwd=project,
                                      text=True, capture_output=True, timeout=10)
                expected = int(module == 'test_complete' and variant != 'correct')
                output = proc.stdout + proc.stderr
                assert proc.returncode == expected and f'Ran {count} test' in output, output
                if expected:
                    assert 'AssertionError: Lists differ:' in output and 'ERROR:' not in output, output
                assert before == {str(p.relative_to(project)): (p.read_bytes(), p.stat().st_mode) for p in project.rglob('*') if p.is_file()}
                observations.append(dict(variant=variant, module=module, exit_code=proc.returncode,
                                         fresh_public_import_exit=imported.returncode,
                                         output=output.replace(str(project), '<PREFLIGHT>')))
    return observations


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases-output', type=Path, required=True)
    parser.add_argument('--preflight-output', type=Path, required=True)
    args = parser.parse_args()
    if args.cases_output.exists() or args.preflight_output.exists():
        parser.error('Refusing to overwrite cases or prior evidence')
    controls = preflight()
    for path, value in ((args.cases_output, cases()), (args.preflight_output, controls)):
        with path.open('x') as stream:
            json.dump(value, stream, indent=2)
            stream.write('\n')
    print('Two authored tasks and six native controls retained; no model calls.')
