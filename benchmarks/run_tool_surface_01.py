"""Small fixed tool-availability probe; no changes to user configuration."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch
import run

ROOT = Path(__file__).resolve().parents[1]
FLAGS = {'default': [], 'apps_off': ['--disable', 'apps'], 'host_off': ['--disable', 'code_mode_host']}
SETTINGS = dict(model='gpt-6-astra', effort='medium', timeout=120)
CASE = dict(id='native-surface-fix', skill='receipt', files={
 'app.py': 'def quantity():\n    return 1\n\ndef payload():\n    return b"\\x00\\xff"\n',
 'test_app.py': 'import unittest\nfrom app import quantity, payload\n\nclass Tests(unittest.TestCase):\n    def test_quantity(self):\n        self.assertEqual(quantity(), 2)\n    def test_payload(self):\n        self.assertEqual(payload(), b"\\x00\\xff")\n',
 'notes.txt': 'original owner note\n',
 'AGENTS.md': 'Python standard-library unittest. Work only inside this project. Preserve tests and owner changes. No installs, services, delegation or commits.\n'},
 working_files={'notes.txt': 'uncommitted owner change\n'},
 task='Fix app.quantity to satisfy the supplied contract tests. Read app.py, test_app.py and project instructions. Execute python3 -B -m unittest -v test_app before and after the fix, retaining actual results and process exits. Change app.py only; preserve test coverage, payload behavior and all owner changes. No scratch reports, dependencies, external access or commits.')


def frozen():
    return json.loads(json.dumps(dict(case=CASE, flags=FLAGS, settings=SETTINGS,
        sources={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in (
            'benchmarks/run_tool_surface_01.py','benchmarks/TOOL-SURFACE-01-PROTOCOL.md',
            'benchmarks/run.py','tests/test_tool_surface_01.py')},
        python=sys.executable, python_version=sys.version,
        cli_version=subprocess.check_output(["codex", "--version"], text=True).strip())))


def process_wrapper(original, flags):
    def invoke(args, *positional, **keywords):
        if isinstance(args, (list, tuple)) and list(args[:2]) == ['codex', 'exec']:
            args = [*args[:2], *flags, *args[2:]]
        return original(args, *positional, **keywords)
    return invoke


def preflight():
    with tempfile.TemporaryDirectory(prefix='surface-author-',dir=ROOT/'benchmarks') as temporary:
        root=Path(temporary)
        for name,content in CASE['files'].items(): (root/name).write_text(content)
        before=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_app'],cwd=root,text=True,capture_output=True)
        assert before.returncode==1 and 'Ran 2 tests' in before.stderr and 'AssertionError: 1 != 2' in before.stderr and 'errors=' not in before.stderr
        (root/'app.py').write_text(CASE['files']['app.py'].replace('return 1','return 2'))
        after=subprocess.run([sys.executable,'-B','-m','unittest','-v','test_app'],cwd=root,text=True,capture_output=True)
        assert after.returncode==0 and 'Ran 2 tests' in after.stderr and 'OK' in after.stderr
        return dict(before_exit=1,after_exit=0,before=before.stderr.replace(str(root),'<AUTHOR-COPY>'),after=after.stderr.replace(str(root),'<AUTHOR-COPY>'))


def prepare(output):
    if output.exists(): raise FileExistsError(output)
    controls=preflight()
    output.mkdir(parents=True)
    manifest=dict(frozen(),completed=[],schedule=list(FLAGS),prepared_at=datetime.now(timezone.utc).isoformat())
    (output/'preflight.json').write_text(json.dumps(controls,indent=2)+'\n')
    for directory in (output,*(output/k for k in FLAGS)):
        directory.mkdir(exist_ok=True)
        (directory/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest


def execute(output,manifest):
    if any(manifest.get(k)!=v for k,v in frozen().items()) or manifest['completed']:
        raise ValueError('Frozen input changed or execution already attempted')
    with (output/'execution-started.json').open('x') as stream:
        json.dump(dict(started_at=datetime.now(timezone.utc).isoformat()),stream)
    disabled=run.disabled_skills()
    for condition,flags in FLAGS.items():
        if any(manifest.get(k)!=v for k,v in frozen().items()):raise ValueError('Frozen drift; do not restart')
        print('Starting '+condition,flush=True)
        with patch.object(run.subprocess,'Popen',new=process_wrapper(run.subprocess.Popen,flags)):
            result=run.run_cell(CASE,'baseline',1,output/condition,SETTINGS['model'],SETTINGS['effort'],SETTINGS['timeout'],disabled,workspace_root=output/'workspaces'/condition,persist_session=True)
        row=dict(condition=condition,**{k:result[k] for k in ('completed','timed_out','limit_detected','usage','elapsed_seconds')})
        manifest['completed'].append(row)
        (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')
        print(json.dumps(row),flush=True)
        if result['limit_detected'] or not result['completed']:break
    manifest['finished_at']=datetime.now(timezone.utc).isoformat()
    (output/'run.json').write_text(json.dumps(manifest,indent=2)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args();output=args.output.resolve()
    if args.execute:execute(output,json.loads((output/'run.json').read_text()))
    else:prepare(output);print('Three probe conditions prepared; no model calls.')
