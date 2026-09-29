"""Exact extracted prospective author inventory; not a solver preservation policy."""
from pathlib import Path
import os,hashlib
NATIVE_CACHE_ROOTS = {'.cache', '.pytest_cache', '.hypothesis'}
def inventory(project):
 source, cache = {}, {}
 for f in project.rglob('*'):
  relative = f.relative_to(project)
  if relative.parts[0] == '.git': continue
  if f.is_symlink():
   record = {'symlink': os.readlink(f), 'mode': f.lstat().st_mode & 0o777}
  elif f.is_file():
   record = {'sha256': hashlib.sha256(f.read_bytes()).hexdigest(), 'mode': f.stat().st_mode & 0o777}
  else: continue
  target = cache if relative.parts[0] in NATIVE_CACHE_ROOTS or '__pycache__' in relative.parts else source
  target[relative.as_posix()] = record
 return {'source': source, 'runtime_cache': cache}
