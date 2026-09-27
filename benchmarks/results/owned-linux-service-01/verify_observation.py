import json,sys
from pathlib import Path
root=Path(sys.argv[1]);observed=json.loads((root/'result.json').read_text())['observations'][0]
wheel=json.loads(Path(sys.argv[2]).read_text())['wheels']
expected=next(e['native_elf_headers'][0]['sha256'] for e in wheel if e['name']=='MarkupSafe')
assert observed['service_ready']['native_extension_sha256']==expected,'Loaded extension differs from verified wheel'
assert observed['http']['url']==observed['service_ready']['url']+'get?control=owned-linux-service','HTTPbin echoed URL mismatch'
assert observed['service_ready']['versions']==dict(httpbin='0.4.1',Flask='1.1.4',Werkzeug='1.0.1',MarkupSafe='2.0.1'),'Actual service versions differ'
print(json.dumps(dict(loaded_native_extension_matches_verified_wheel=True,echoed_url_verified=True,versions_verified=True,extra_native_processes=0)))
