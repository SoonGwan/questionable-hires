"""Reuse native observer boundary controls against the candidate codec."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'benchmarks'))
from export import redact_paths
source = ROOT / 'skills/receipt/scripts/assertions.py'
control = ROOT / 'benchmarks/results/assertion-observer-prototype-02/control.py'
interpreters = [Path('/Library/Developer/CommandLineTools/usr/bin/python3'), Path(sys.executable)]
rows = []
with tempfile.TemporaryDirectory(prefix='qh-codec-boundaries-') as temp:
    directory = Path(temp)
    shutil.copyfile(source, directory/'observer.py')
    shutil.copyfile(control, directory/'control.py')
    for python in interpreters:
        assert python.is_file()
        version = subprocess.check_output([str(python), '--version'], text=True).strip()
        for mode in ('off', 'on', 'byte-limit', 'record-limit', 'encoder-error', 'existing-profile'):
            for broken in ((False,) if mode == 'existing-profile' else (False, True)):
                result = subprocess.run([str(python), '-B', str(directory/'control.py'), mode, *(['broken'] if broken else [])],
                                        cwd=directory, capture_output=True, text=True, timeout=15)
                assert result.returncode == int(broken), (version, mode, broken, result.stderr)
                if mode != 'existing-profile':
                    assert 'Ran 3 tests' in result.stderr
                    assert ('FAILED (failures=1)' if broken else '\nOK\n') in result.stderr
                report = None
                if mode not in ('off', 'existing-profile'):
                    report = json.loads(result.stdout)
                    assert not report['complete']
                    expected = {'on':'unavailable_value', 'byte-limit':'byte_limit', 'record-limit':'record_limit', 'encoder-error':'observer_error'}[mode]
                    assert report['reason'] == expected
                    assert len(result.stdout.strip().encode('ascii')) <= (128 if mode == 'byte-limit' else 4096)
                rows.append(dict(python=version, mode=mode, broken=broken, native_exit=result.returncode,
                                 stdout=result.stdout, stderr=result.stderr, report=report))
spec = importlib.util.spec_from_file_location('candidate_codec', source)
observer = importlib.util.module_from_spec(spec); spec.loader.exec_module(observer)
observation = observer.observe()
replacement = lambda *args: None
sys.setprofile(replacement)
value = json.loads(observation.close())
assert sys.getprofile() is replacement and value['reason'] == 'profile_replaced' and not value['complete']
assert json.loads(observation.close()) == value
sys.setprofile(None)
for option in ({'max_bytes':127}, {'max_bytes':65537}, {'max_bytes':True}, {'max_records':0}, {'max_records':65}):
    try: observer.observe(**option)
    except ValueError: pass
    else: raise AssertionError('invalid bound accepted')
    assert sys.getprofile() is None
result = dict(checkpoint='assertion-value-codec-boundaries-01', date='2026-09-27',
              source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              reused_control_sha256=hashlib.sha256(control.read_bytes()).hexdigest(),
              native_controls=len(rows), replacement_and_repeated_close=True, invalid_bounds=5,
              rows=rows, models=0, installed_changes=False)
Path(__file__).with_name('boundaries.json').write_text(redact_paths(json.dumps(result, indent=2))+'\n')
print('Native boundary controls:',len(rows),'; replacement ownership/repeated close and five invalid bounds pass')
