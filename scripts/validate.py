#!/usr/bin/env python3
"""Check the shipped skill catalog and plugin references (not model behavior)."""

import json
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
HIRES = {"necromancer", "receipt", "landlord", "mother-in-law", "exorcist", "hostage-negotiator", "con-artist", "friday"}


def validate(root):
    errors = []
    skills = root / "skills"
    found = {p.parent.name for p in skills.glob("*/SKILL.md")}
    if found != HIRES:
        errors.append(f"Catalog mismatch: missing={sorted(HIRES - found)}, unexpected={sorted(found - HIRES)}")
    for name in sorted(found):
        path = skills / name / "SKILL.md"
        try:
            parts = path.read_text().split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                raise ValueError("missing opening YAML frontmatter")
            meta = yaml.safe_load(parts[1])
            if not isinstance(meta, dict) or meta.get("name") != name:
                raise ValueError("frontmatter name must match directory")
            if not isinstance(meta.get("description"), str) or not meta["description"].strip():
                raise ValueError("missing discovery description")
            if not parts[2].strip():
                raise ValueError("empty skill instructions")
            ui = yaml.safe_load((path.parent / "agents/openai.yaml").read_text())["interface"]
            if not 25 <= len(ui["short_description"]) <= 64:
                raise ValueError("UI description must be 25–64 characters")
            if f"${name}" not in ui["default_prompt"]:
                raise ValueError("UI prompt must invoke its own skill")
        except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
            errors.append(f"{name}: {error}")
    try:
        manifest = json.loads((root / ".codex-plugin/plugin.json").read_text())
        if manifest["name"] != "questionable-hires" or manifest["skills"] != "./skills/":
            errors.append("Plugin name or skill discovery path is incorrect")
        if not re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]):
            errors.append("Expected a three-part release version")
        if not manifest["interface"]["capabilities"]:
            errors.append("Missing plugin capabilities")
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append(f"plugin: {error}")
    # Validate repository-relative Markdown links, excluding anchors and URLs.
    documents = {root / "README.md", root / "CONTRIBUTING.md", *root.glob("*.md"),
                 *root.glob("docs/*.md"), *root.glob("examples/*.md"), *root.glob("evals/*.md"),
                 *root.glob("benchmarks/*.md"), *root.glob("benchmarks/results/*/*/answer.md"), *skills.rglob("*.md")}
    for file in sorted(documents):
        if not file.exists():
            errors.append(f"Missing document: {file.relative_to(root)}")
            continue
        for target in re.findall(r"\]\(([^)]+)\)", file.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            if not (file.parent / target.split("#", 1)[0]).exists():
                errors.append(f"{file.relative_to(root)}: broken link {target}")
    return errors


if __name__ == "__main__":
    errors = validate(ROOT)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {len(HIRES)} hires, UI metadata, plugin references, and local documentation links.")
