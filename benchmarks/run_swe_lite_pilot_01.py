"""Exclusive four-cell external pilot; generic capture/containers are reused."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

import run
import swe_lite_environment as environment
from swe_lite_container import container_launcher
from extract_rollout_tools import extract

ROOT = run.ROOT
RESOURCE = '8ee6c56'
SELECTION = ROOT/'benchmarks/local-runs/swe-lite-pilot-01-selection.original.json'
SELECTION_HASH = 'd906940879ab70be1d5b472b1a8610a1aaf199bd1298f0a3b8d705610d246b5a'
SCHEDULE = [('requests', 'baseline'), ('requests', 'current'),
            ('pytest', 'current'), ('pytest', 'baseline')]
SETTINGS = dict(model='gpt-6-astra', effort='medium', inner_timeout=360,
                outer_timeout=380, jobs=1, repeats=1, memory_gib=6, cpus=2)
WRAPPER = (
    'Implement a fix for the reported issue in this checkout. Preserve existing '
    'behavior, add a focused regression test when needed, and run relevant native '
    'tests using the installed Python environment. Do not weaken or suppress '
    'existing tests. Do not install or change dependencies, retrieve upstream '
    'history/solutions, use internet resources, modify installed skills, or make '
    'commits or stage changes. Keep edits within the project; runtime-created temporary files under '
    '`.git/qh-tmp` are allowed. Do not deliberately change Git history or configuration. Report the '
    'changes, verification commands/results, and any remaining uncertainty.\n\n'
    'Environment: `python` is the prepared interpreter. Requests tests use local '
    'HTTP/HTTPS endpoints via HTTPBIN_URL and normal certificate verification. '
    'An empty pytest configuration at the project-local temporary root prevents '
    'nested self-tests from inheriting parent project options. Do not inspect '
    'runtime credentials.\n\nIssue report:\n')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], timeout=30)


def cases():
    if digest(SELECTION) != SELECTION_HASH:
        raise ValueError('Projected selection changed')
    rows = {row['repo']: row for row in json.loads(SELECTION.read_text())['selected']}
    result = {}
    for project, repo, identity in [('requests','psf/requests','psf__requests-2317'),
                                    ('pytest','pytest-dev/pytest','pytest-dev__pytest-7432')]:
        row = rows[repo]
        if row['instance_id'] != identity:
            raise ValueError('Unexpected selected issue')
        result[project] = dict(id=project+'-'+identity.rsplit('-',1)[1],
            instance_id=identity, skill='necromancer', task=WRAPPER+row['problem_statement'])
    return result


def expected_prompt(case, arm):
    restriction = ('Do not use external services or other installed skills.' if arm == 'baseline'
                   else 'Do not use external services.')
    return case['task'] + '\n\nWork only inside this local repository. ' + restriction + ' Do not delegate.'


def snapshot(destination):
    for line in git('ls-tree','-r',RESOURCE,'--','skills').decode().splitlines():
        info, name = line.split('\t',1)
        mode, kind, oid = info.split()
        if kind != 'blob' or mode not in ('100644','100755'):
            raise ValueError('Unsupported resource kind')
        path = destination/name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(git('cat-file','blob',oid))
        path.chmod(int(mode[-3:],8))
    if len(list((destination/'skills').glob('*/SKILL.md'))) != 8:
        raise ValueError('Expected all eight skills')


def identities():
    paths = ['benchmarks/'+name for name in (
        'run_swe_lite_pilot_01.py','run.py','swe_lite_container.py','swe_lite_environment.py',
        'extract_rollout_tools.py','SWE-LITE-PILOT-01-PROTOCOL.md')]
    paths += ['tests/test_swe_lite_pilot_runner.py']
    paths += ['benchmarks/results/swe-lite-pilot-01-final-environment/02-summary.json']
    paths += ['benchmarks/local-runs/swe-lite-pilot-01-scoring/'+name+'.json'
              for name in ('psf__requests-2317','pytest-dev__pytest-7432')]
    return {name:digest(ROOT/name) for name in paths}


def validate_preflight():
    evidence = ROOT/'benchmarks/results/swe-lite-pilot-01-final-environment'
    record = json.loads((evidence/'02-summary.json').read_text())
    for name, value in record['identities'].items():
        if digest(ROOT/'benchmarks'/name) != value:
            raise ValueError('Native preflight code changed: '+name)
    controls = record['controls']
    if {(r['project'],r['network']) for r in controls} != {
            ('requests','none'),('requests','bridge'),('pytest','bridge')} or len(controls) != 3:
        raise ValueError('Missing native path controls')
    for row in controls:
        life = row['lifecycle']
        if row['exit_code'] != 0 or not row['source_unchanged'] or not life['removed'] or life['oom_killed']:
            raise ValueError('Unusable native control')
        log = (evidence/('02-'+row['project']+'-'+row['network']+'-stdout.log')).read_text()
        count = 142 if row['project'] == 'requests' else 77
        if f'{count} passed' not in log or f'QH_PUBLIC_SOURCE_BINDINGS={count}' not in log:
            raise ValueError('Missing native source-bound pass evidence')


def frozen(output):
    runtime = json.loads(environment.docker('info','--format',
        '{"memory":{{.MemTotal}},"cpus":{{.NCPU}},"architecture":"{{.Architecture}}",'
        '"version":"{{.ServerVersion}}"}').stdout)
    if runtime['memory'] < 7*1024**3 or runtime['cpus'] != 2:
        raise ValueError('Dedicated VM does not match the protocol capacity')
    for image in environment.IMAGES.values():
        observed = environment.docker('image','inspect',image,'--format','{{.Id}}').stdout.decode().strip()
        if observed != image:
            raise ValueError('Unexpected solver image identity')
    return dict(identities=identities(), cases=cases(), settings=dict(SETTINGS),
        runtime=runtime,
        schedule=[list(row) for row in SCHEDULE], context=environment.CONTEXT,
        images=dict(environment.IMAGES), resource_revision=git('rev-parse',RESOURCE).decode().strip(),
        resource_digest=run.resource_digest(output/'current/skills'),
        source_digests={p:run.resource_digest(output/'sources'/p) for p in ('requests','pytest')})


def save(output, manifest):
    (output/'run.json').write_text(json.dumps(manifest, indent=2)+'\n')


def prepare(output):
    if output.exists():
        raise FileExistsError(output)
    validate_preflight()
    selected = cases()
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    (output/'sources').mkdir()
    for condition in ('baseline','current'):
        (output/condition/'skills').mkdir(parents=True)
    snapshot(output/'current')
    for project in selected:
        environment.source(project, output/'sources'/project)
    manifest = dict(frozen(output), prepared_at=datetime.now(timezone.utc).isoformat(),
        cells=[dict(project=p, condition=c, status='unrun',
                    prompt=expected_prompt(selected[p], 'baseline' if c == 'baseline' else 'auto'))
               for p,c in SCHEDULE], stopped_reason=None)
    save(output,manifest)
    return manifest


def verify(output, manifest):
    if any(manifest.get(key) != value for key,value in frozen(output).items()):
        raise ValueError('Frozen inputs changed; do not restart')


def execute(output, auth_file):
    manifest = json.loads((output/'run.json').read_text())
    verify(output,manifest)
    with (output/'execution-started.json').open('x') as stream:
        json.dump(dict(revision=git('rev-parse','HEAD').decode().strip(),
                       started_at=datetime.now(timezone.utc).isoformat()),stream)
    # Only this already-owned fixture is started/stopped; no context switching.
    environment.docker('start',environment.SERVICE)
    try:
        subprocess.run(['openssl','x509','-checkend','86400','-noout','-in',
            str(ROOT/'benchmarks/local-runs/swe-lite-tls-01/server.pem')],check=True,capture_output=True)
        environment.docker('exec',environment.SERVICE,'python','-c',
            'import time, urllib.request, urllib.error\n'
            'deadline=time.monotonic()+15\n'
            'while True:\n'
            ' try:\n'
            '  assert urllib.request.urlopen("http://127.0.0.1/get",timeout=2).status == 200\n'
            '  break\n'
            ' except urllib.error.URLError:\n'
            '  if time.monotonic() >= deadline: raise\n'
            '  time.sleep(.1)\n')
        with tempfile.TemporaryDirectory(prefix='qh-pilot-auth-',dir=output.parent) as private:
            copied = Path(private)/'auth.json'
            shutil.copyfile(auth_file,copied)
            copied.chmod(0o600)
            for position,(project,condition) in enumerate(SCHEDULE):
                verify(output,manifest)
                row = manifest['cells'][position]
                row['status'] = 'running'
                save(output,manifest)
                case = manifest['cases'][project]
                arm = 'baseline' if condition == 'baseline' else 'auto'
                state = output/'runtime-state'/f'{project}-{condition}'
                launch = container_launcher(environment.IMAGES[project],copied,state,project,
                    network='bridge',timeout=SETTINGS['inner_timeout'],context=environment.CONTEXT,
                    memory_gib=SETTINGS['memory_gib'])
                def launcher(workspace,args):
                    return launch(workspace,args[:-1]+['-c','web_search="disabled"',args[-1]])
                print('Starting '+project+' / '+condition,flush=True)
                result = run.run_cell(case,arm,1,output/condition,SETTINGS['model'],SETTINGS['effort'],
                    SETTINGS['outer_timeout'],[],skills_root=output/'current/skills',
                    project_source=output/'sources'/project,launcher=launcher,
                    workspace_root=output/'workspaces'/condition,persist_session=True)
                row.update(status='attempted',**{key:result[key] for key in
                    ('completed','timed_out','limit_detected','usage','elapsed_seconds','exit_code')})
                lifecycle = json.loads((state/'lifecycle.json').read_text())
                row['lifecycle'] = lifecycle
                reasons = []
                if not lifecycle['removed'] or lifecycle.get('oom_killed') or lifecycle['interrupted']:
                    reasons.append('container lifecycle failure')
                if result['prompt'] != row['prompt']:
                    reasons.append('prompt mismatch')
                sessions = list((state/'sessions').rglob('*.jsonl'))
                if len(sessions) != 1:
                    reasons.append('missing or ambiguous session')
                else:
                    _, captured = extract(sessions[0],output/condition/f'{case["id"]}--{arm}--1/events.jsonl')
                    row['session_sha256'] = captured['source_sha256']
                if result['limit_detected']:
                    reasons.append('account limit')
                manifest['stopped_reason'] = '; '.join(reasons) or None
                save(output,manifest)
                print(json.dumps({k:v for k,v in row.items() if k != 'prompt'}),flush=True)
                if reasons:
                    break
    except Exception as error:
        manifest['stopped_reason'] = type(error).__name__
        for row in manifest['cells']:
            if row['status'] == 'running':
                row.update(status='runner_error', error_type=type(error).__name__)
        save(output,manifest)
        raise
    finally:
        environment.docker('stop',environment.SERVICE)
        manifest['finished_at'] = datetime.now(timezone.utc).isoformat()
        save(output,manifest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--execute',action='store_true')
    args = parser.parse_args()
    output = args.output.resolve()
    if args.execute:
        auth = Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))/'auth.json'
        if auth.is_symlink() or not auth.is_file():
            raise ValueError('Existing regular authentication file required')
        execute(output,auth)
    else:
        prepare(output)
        print('Prepared two external tasks / four frozen cells; no model calls.')
