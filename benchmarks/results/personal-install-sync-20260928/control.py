import hashlib,importlib.util,json,subprocess,sys,shutil
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'benchmarks'))
import run
from receipt_ledger_cases import cases

def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
installer=load('installer',ROOT/'scripts/install.py')
selected=['con-artist','necromancer','receipt']
live=Path.home()/'.agents/skills'
base=Path.home()/'.agents/skill-backups/questionable-hires'/('20260928-personal-sync-'+subprocess.check_output(['git','rev-parse','--short=8','HEAD'],text=True).strip())
state_file=Path('/tmp/qh-personal-sync-20260928-state.json')

def write(path,value):path.write_text(json.dumps(value,indent=2)+'\n')
def native(label,helper_path):
 helper=load('receipt_'+label,helper_path);rows=[]
 for i in (0,1):
  project=base/'native'/label/str(i)/'project';project.parent.mkdir(parents=True)
  run.prepare(cases()[i],project);before=helper.tree_inventory(project)
  recipe=dict(fixed=['checks','ledger/schema.sql','ledger/__init__.py'],vary=['ledger/delivery.py'],before='HEAD^',after='HEAD',imports=['ledger.delivery','checks.test_delivery'],runner='unittest',invocation='module',tests=['-v','checks.test_delivery'],guard_tree=True,observe_assertions=True)
  try:
   result=helper.compare(project,recipe);error=None
  except (ValueError,KeyError) as exc:
   result=None;error=dict(type=type(exc).__name__,message=str(exc))
  assert helper.tree_inventory(project)==before
  rows.append(dict(case=cases()[i]['id'],result=result,error=error,source_preserved=True))
 write(base/(label+'-native.json'),dict(helper_sha256=hashlib.sha256(helper_path.read_bytes()).hexdigest(),rows=rows))
 return rows

if sys.argv[1]=='prepare':
 assert not subprocess.check_output(['git','status','--porcelain'],text=True)
 assert not base.exists() and not state_file.exists()
 old={n:installer.resource_inventory(live/n) for n in installer.available()}
 new={n:installer.resource_inventory(ROOT/'skills'/n) for n in installer.available()}
 assert [n for n in installer.available() if old[n]!=new[n]]==selected
 provenance=[]
 for name in selected:
  assert not old[name].keys()-new[name].keys()
  for rel in old[name].keys()&new[name].keys():
   if old[name][rel]==new[name][rel]:continue
   blob=subprocess.check_output(['git','hash-object','--stdin'],input=(live/name/rel).read_bytes()).decode().strip()
   history=subprocess.check_output(['git','log','--all','--format=%H','--find-object='+blob,'--','skills/'+name+'/'+rel],text=True).splitlines()
   assert history,(name,rel)
   provenance.append(dict(skill=name,path=rel,git_blob=blob,history=history))
 base.mkdir(parents=True,mode=0o700);(base/'old').mkdir();(base/'displaced-new').mkdir()
 installer.install(base/'staged',selected)
 for name in selected:assert installer.resource_inventory(base/'staged'/name)==new[name]
 smokes=[]
 for name in selected:
  for script in sorted((base/'staged'/name/'scripts').glob('*.py')):
   if "if __name__ == '__main__':" not in script.read_text():continue
   r=subprocess.run([sys.executable,'-B',str(script),'--help'],capture_output=True,text=True,timeout=10)
   assert r.returncode==0 and 'usage:' in r.stdout,(script,r.stderr)
   smokes.append(dict(skill=name,script=script.name,exit_code=r.returncode))
 state=dict(source_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),base=str(base),selected=selected,old=old,new=new,provenance=provenance,staged_cli_smokes=smokes,phase='prepared')
 write(state_file,state);write(base/'manifest.json',state)
 rows=native('before',live/'receipt/scripts/compare.py')
 print('Prepared',str(base),'CLI smokes',len(smokes))
 for row in rows:print(row['case'],'error',row['error'],'status',row['result']['status'] if row['result'] else None,'observations',[c.get('assertion_observation') for c in row['result']['checks'].values()] if row['result'] else None)
elif sys.argv[1]=='apply':
 state=json.loads(state_file.read_text());assert state['phase']=='prepared'
 def same(actual,expected):return json.loads(json.dumps(actual))==expected
 for name in installer.available():assert same(installer.resource_inventory(live/name),state['old'][name])
 for name in selected:assert same(installer.resource_inventory(base/'staged'/name),state['new'][name])
 replaced=[]
 try:
  for name in selected:
   (live/name).rename(base/'old'/name);replaced.append(name)
   (base/'staged'/name).rename(live/name)
   assert same(installer.resource_inventory(live/name),state['new'][name])
  report=installer.check_installation(live,installer.available());assert report['matches']
  rows=native('after',live/'receipt/scripts/compare.py')
  for i,row in enumerate(rows):
   assert row['error'] is None and row['result']['status']=='observed'
   result=row['result'];assert [c['native_exit_code'] for c in result['checks'].values()]==[1,0 if i==0 else 1]
   assert result['comparison_copies_removed'] and result['tree_guard']['unchanged']
   for c in result['checks'].values():
    assert c['provenance_ready'] and c['suite_observation']['tests']==5 and not c['suite_observation']['skipped']
    obs=c['assertion_observation'];assert obs['v']==3 and obs['complete'] and len(obs['observations'])==14
  for name in selected:assert same(installer.resource_inventory(base/'old'/name),state['old'][name])
  state['phase']='verified';state['after_check']=report
 except BaseException:
  for name in reversed(replaced):
   if (live/name).exists():
    if not same(installer.resource_inventory(live/name),state['new'][name]):raise RuntimeError('Concurrent changes; preserve live and backup for manual recovery')
    (live/name).rename(base/'displaced-new'/name)
   (base/'old'/name).rename(live/name)
  state['phase']='rolled-back';write(state_file,state);write(base/'manifest.json',state);raise
 write(state_file,state);write(base/'manifest.json',state)
 print('Updated exactly three installs; all eight match source bytes/modes; old copies preserved.')
 print('Installed native comparisons: complete fix 1/0, partial fix 1/1; five tests and fourteen v3 pairs per phase.')
else:raise ValueError('Unknown phase')
