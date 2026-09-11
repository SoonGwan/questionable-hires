#!/usr/bin/env python3
"""Build a local marketplace bundle without changing the host's configuration."""

import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    destination = Path(destination).resolve()
    # Reject linked source trees before following them or reserving any output.
    sources = (ROOT / 'skills', ROOT / '.codex-plugin', ROOT / 'LICENSE',
               ROOT / 'packaging/marketplace.json')
    for source in sources:
        ancestors = [p for p in source.parents if p != ROOT and ROOT in p.parents]
        if source.is_symlink() or any(p.is_symlink() for p in ancestors) or any(
                p.is_symlink() for p in source.rglob('*')):
            raise OSError('Source symlinks are unsupported: ' + str(source.relative_to(ROOT)))
        if source.is_dir() and (source.resolve() == destination or source.resolve() in destination.parents):
            raise OSError('Build output must not be inside a copied source tree')
    destination.mkdir(parents=True, exist_ok=False)
    try:
        plugin = destination / "plugins/questionable-hires"
        plugin.mkdir(parents=True)
        shutil.copytree(ROOT / ".codex-plugin", plugin / ".codex-plugin")
        for source in (ROOT / "skills").iterdir():
            if (source / "SKILL.md").is_file():
                shutil.copytree(source, plugin / "skills" / source.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy2(ROOT / "LICENSE", plugin / "LICENSE")
        catalog = destination / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        shutil.copy2(ROOT / "packaging/marketplace.json", catalog)
    except BaseException:
        # Exclusive creation above succeeded: only this invocation's output is
        # eligible for cleanup. Never replace the original error/cancellation.
        try:
            shutil.rmtree(destination)
        except BaseException:
            pass
        raise
    return plugin


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="A new directory")
    args = parser.parse_args()
    try:
        print(build(args.output))
    except OSError as error:
        parser.exit(1, f"Build failed: {error}\n")
