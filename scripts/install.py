#!/usr/bin/env python3
"""Install selected hires without overwriting an existing skill."""

import argparse
from pathlib import Path
import shutil
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def available():
    return sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))


def install(destination, names, dry_run=False):
    destination = Path(destination).expanduser().resolve()
    names = list(dict.fromkeys(names))
    unknown = set(names) - set(available())
    if unknown:
        raise ValueError("Unknown hires: " + ", ".join(sorted(unknown)))
    conflicts = [name for name in names if (destination / name).exists() or (destination / name).is_symlink()]
    if conflicts:
        raise ValueError("Existing skills left untouched: " + ", ".join(conflicts))
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
            shutil.copytree(ROOT / "skills" / name, target, dirs_exist_ok=True)
    except Exception:
        # Only directories created by this invocation are eligible for rollback.
        for target in reversed(installed):
            shutil.rmtree(target)
        raise
    return installed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, required=True, help="Skill discovery directory, e.g. /path/to/project/.agents/skills")
    parser.add_argument("--skill", action="append", choices=available(), help="Repeat to choose hires; default: all")
    parser.add_argument("--dry-run", action="store_true", help="Show destinations without writing")
    args = parser.parse_args()
    try:
        paths = install(args.dest, args.skill or available(), args.dry_run)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Installation failed: {error}\n")
    for path in paths:
        print(f"{'Would install' if args.dry_run else 'Installed'}: {path}")


if __name__ == "__main__":
    main()
