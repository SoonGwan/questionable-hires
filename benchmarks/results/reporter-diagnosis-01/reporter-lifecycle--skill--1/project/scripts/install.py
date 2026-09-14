#!/usr/bin/env python3
"""Install selected hires without overwriting an existing skill."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat


ROOT = Path(__file__).resolve().parents[1]


def available():
    return sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))


def resource_inventory(root):
    """Read regular resources only; mirror installation's cache exclusions."""
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Expected a regular skill directory: ' + str(root))
    result = {}
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part == '__pycache__' or part.endswith('.pyc') for part in relative.parts):
            continue
        mode = path.lstat().st_mode
        if stat.S_ISDIR(mode):
            continue
        if not stat.S_ISREG(mode):
            raise ValueError('Unsupported linked or special resource: ' + str(relative))
        digest = hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(65536), b''):
                digest.update(chunk)
        result[relative.as_posix()] = (digest.hexdigest(), stat.S_IMODE(mode))
    return result


def check_installation(destination, names):
    """Compare without creating, replacing or removing any installed files."""
    destination = Path(destination).expanduser().resolve()
    if destination.exists() and not destination.is_dir():
        raise ValueError('Destination must be a directory')
    names = list(dict.fromkeys(names))
    unknown = set(names) - set(available())
    if unknown:
        raise ValueError('Unknown hires: ' + ', '.join(sorted(unknown)))
    if (ROOT / 'skills').is_symlink():
        raise ValueError('Source skill root must not be a symlink')
    reports = []
    for name in names:
        source = resource_inventory(ROOT / 'skills' / name)
        target = destination / name
        if not target.exists() and not target.is_symlink():
            reports.append(dict(skill=name, status='missing', missing=sorted(source), changed=[], extra=[]))
            continue
        installed = resource_inventory(target)
        missing, extra = sorted(source.keys() - installed.keys()), sorted(installed.keys() - source.keys())
        changed = sorted(p for p in source.keys() & installed.keys() if source[p] != installed[p])
        reports.append(dict(skill=name, status='different' if missing or extra or changed else 'matching',
                            missing=missing, changed=changed, extra=extra))
    return dict(comparison='local checkout bytes and file modes; not remote freshness or safety',
                skills=reports, matches=all(r['status'] == 'matching' for r in reports))


def install(destination, names, dry_run=False):
    destination = Path(destination).expanduser().resolve()
    names = list(dict.fromkeys(names))
    unknown = set(names) - set(available())
    if unknown:
        raise ValueError("Unknown hires: " + ", ".join(sorted(unknown)))
    conflicts = [name for name in names if (destination / name).exists() or (destination / name).is_symlink()]
    if conflicts:
        raise ValueError("Existing skills left untouched: " + ", ".join(conflicts))
    source_root = (ROOT / 'skills').resolve()
    if destination == source_root or source_root in destination.parents:
        raise ValueError('Installation destination must not be inside the source skill tree')
    # Refuse linked source resources instead of silently copying their referents.
    # Check every selected skill before creating any destination folders.
    for name in names:
        source = ROOT / 'skills' / name
        if (ROOT / 'skills').is_symlink() or source.is_symlink() or any(
                path.is_symlink() for path in source.rglob('*')):
            raise ValueError('Source symlinks are unsupported: ' + name)
    if dry_run:
        return [destination / name for name in names]
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    try:
        for name in names:
            # Reserve the target exclusively; don't replace a concurrently created skill.
            target = destination / name
            target.mkdir()
            installed.append(target)
            shutil.copytree(ROOT / "skills" / name, target, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    except Exception:
        # Only directories created by this invocation are eligible for rollback.
        for target in reversed(installed):
            try:
                shutil.rmtree(target)
            except BaseException:
                # Preserve the install error/cancellation and still attempt
                # rollback of the other targets created by this invocation.
                pass
        raise
    return installed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="Skill discovery directory, e.g. /path/to/project/.agents/skills")
    parser.add_argument("--skill", action="append", choices=available(), help="Repeat to choose hires; default: all")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Show destinations without writing")
    mode.add_argument("--check", action="store_true", help="Read-only JSON comparison with this checkout; exit 2 for differences")
    args = parser.parse_args()
    if args.check:
        try:
            report = check_installation(args.dest, args.skill or available())
        except (ValueError, OSError) as error:
            parser.exit(1, f'Comparison failed; no files changed: {error}\n')
        print(json.dumps(report, indent=2))
        parser.exit(0 if report['matches'] else 2)
    try:
        paths = install(args.dest, args.skill or available(), args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Installation failed: {error}\n")
    for path in paths:
        print(f"{'Would install' if args.dry_run else 'Installed'}: {path}")


if __name__ == "__main__":
    main()
