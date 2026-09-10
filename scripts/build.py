#!/usr/bin/env python3
"""Build a local marketplace bundle without changing the host's configuration."""

import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def build(destination):
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
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
    return plugin


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="A new directory")
    args = parser.parse_args()
    try:
        print(build(args.output))
    except OSError as error:
        parser.exit(1, f"Build failed: {error}\n")
