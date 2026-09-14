#!/usr/bin/env python3
"""Build a deterministic standalone skill archive from a trusted checkout."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import stat
import tarfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'questionable-hires'


def package(destination):
    destination = Path(destination).absolute()
    skills = ROOT / 'skills'
    if skills.is_symlink():
        raise ValueError('Linked skill root is unsupported')
    paths = [ROOT / 'LICENSE', ROOT / 'scripts/install.py']
    for folder in sorted(skills.iterdir()):
        if folder.is_symlink():
            raise ValueError('Linked skill directory is unsupported: ' + folder.name)
        if not (folder / 'SKILL.md').is_file():
            continue
        for path in sorted(folder.rglob('*')):
            relative = path.relative_to(folder)
            if any(part == '__pycache__' or part.endswith('.pyc') for part in relative.parts):
                continue
            if path.is_symlink() or not (path.is_dir() or path.is_file()):
                raise ValueError('Linked or special resource is unsupported: ' + str(relative))
            if path.is_file():
                paths.append(path)
    if len(paths) == 2:
        raise ValueError('No skills found')
    if skills.resolve() in destination.resolve().parents or (ROOT / 'scripts').resolve() in destination.resolve().parents:
        raise ValueError('Archive output must be outside source skills/scripts')
    members = {}
    for path in paths:
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != ROOT and ROOT in p.parents):
            raise ValueError('Linked source path is unsupported: ' + str(path))
        mode = path.stat().st_mode
        if not stat.S_ISREG(mode):
            raise ValueError('Expected regular source file: ' + str(path))
        members[path.relative_to(ROOT).as_posix()] = (path.read_bytes(), stat.S_IMODE(mode))
    manifest = {name: {'sha256': hashlib.sha256(data).hexdigest(), 'mode': mode}
                for name, (data, mode) in sorted(members.items())}
    members['CONTENTS.json'] = ((json.dumps(manifest, indent=2, sort_keys=True) + '\n').encode(), 0o644)
    # Reserve exclusively. A failure retains only this new partial output; callers
    # can inspect/remove it, and no previous archive is ever overwritten.
    with destination.open('xb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as zipped:
            with tarfile.open(fileobj=zipped, mode='w', format=tarfile.USTAR_FORMAT) as archive:
                for name, (data, mode) in sorted(members.items()):
                    item = tarfile.TarInfo(PREFIX + '/' + name)
                    item.size, item.mode, item.mtime = len(data), mode, 0
                    item.uid = item.gid = 0
                    item.uname = item.gname = ''
                    archive.addfile(item, io.BytesIO(data))
    return {'archive': str(destination), 'files': len(members),
            'input_bytes': sum(len(data) for data, _ in members.values()),
            'archive_bytes': destination.stat().st_size,
            'sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New .tar.gz path; parent must exist')
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output), indent=2))
    except (ValueError, OSError, tarfile.TarError) as error:
        parser.exit(1, f'Packaging failed: {error}. A newly created partial output may remain.\n')
