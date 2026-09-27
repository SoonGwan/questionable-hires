import hashlib,json,os,subprocess,sys
from pathlib import Path
os.chdir('/testbed');env=os.environ.copy();env['PYTHONPATH']='/_qh_probe_01/layers'+(':'+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
p=subprocess.run([sys.executable,'-B','-m','pytest','--collect-only','-q','-p','qh_collection','-o','cache_dir=/tmp/qh-collection-cache'],cwd='/testbed',capture_output=True,timeout=30,env=env)
report=Path('/tmp/qh-collection-report.json')
text=(p.stdout+p.stderr).decode(errors='replace')
result=dict(checkpoint='owned-official-collection-01',models=0,selected_test_calls=0,native_exit=p.returncode,stdout_bytes=len(p.stdout),stdout_sha256=hashlib.sha256(p.stdout).hexdigest(),stderr_bytes=len(p.stderr),stderr_sha256=hashlib.sha256(p.stderr).hexdigest(),report=json.loads(report.read_text()) if report.is_file() else None,heuristic_diagnostic_counts={name:text.count(name) for name in ('ModuleNotFoundError','ImportError','SyntaxError','FileNotFoundError')},fixed_dependency_mentions={name:text.count("No module named '"+name+"'") for name in ('mock','pytest_httpbin','httpbin','flask','werkzeug')})
print('QH_COLLECTION_OBSERVATION');print(json.dumps(result,sort_keys=True))
