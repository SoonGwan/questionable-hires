"""Local whole-collector profile; output parity required, no model performance claim."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import statistics
import subprocess
import tempfile
import time
import types

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = 'skills/con-artist/scripts/context.py'


def module(source, name):
    loaded = types.ModuleType(name)
    exec(compile(source, SCRIPT, 'exec'), loaded.__dict__)
    return loaded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--original', default='3a985e8')
    args = parser.parse_args()
    old = subprocess.check_output(['git','show',args.original+':'+SCRIPT],cwd=ROOT)
    new = (ROOT/SCRIPT).read_bytes()
    variants = {'original':module(old,'original_context'), 'candidate':module(new,'candidate_context')}
    rows=[]
    with tempfile.TemporaryDirectory(dir=ROOT/'benchmarks/local-runs',prefix='context-profile-') as scratch:
        root=Path(scratch)
        for count in (1,25,200):
            source='\n'.join('@fixture(name="case_%s")\ndef test_%s():\n    return %r\n' %
                (i,i,dict(record=i,payload='x'*100)) for i in range(count))
            (root/'conftest.py').write_text(source)
            expected=None
            timings={'original':[], 'candidate':[]}
            for repeat in range(3):
                for name in (('original','candidate') if repeat%2==0 else ('candidate','original')):
                    start=time.perf_counter()
                    result=variants[name].collect(root,['conftest.py:test_0'])
                    timings[name].append(time.perf_counter()-start)
                    if expected is None:
                        expected=result
                    assert result==expected, 'Output differs from original'
                    assert (root/'conftest.py').read_bytes()==source.encode()
            encoded=json.dumps(expected,sort_keys=True,ensure_ascii=False).encode()
            rows.append(dict(decorators=count,input_bytes=len(source.encode()),
                output_sha256=hashlib.sha256(encoded).hexdigest(),output_bytes=len(encoded),
                output_equal=True,source_unchanged=True,seconds=timings,
                median_seconds={k:statistics.median(v) for k,v in timings.items()}))
    print(json.dumps(dict(original_revision=args.original,python=platform.python_version(),
        source_sha256={k:hashlib.sha256(v).hexdigest() for k,v in [('original',old),('candidate',new)]},
        rows=rows,limitation='Authored decorator-density profile, three in-process alternating repetitions; warm shared host. Includes collection/read/parse/output-size validation, excludes interpreter startup and CLI printing. Not model tokens/time or representative developer performance.'),indent=2))


if __name__=='__main__':
    main()
