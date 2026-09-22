# Onboarding

Public repository access does not require GitHub credentials.
Installing a skill does not select your model or
change your approval settings.

## Install with the skills CLI

The repository follows the standard `skills/*/SKILL.md` layout and can be
installed without a Questionable Hires npm package:

```sh
npx skills add SoonGwan/questionable-hires
```

For a non-interactive project-local Codex installation of one skill:

```sh
npx skills add SoonGwan/questionable-hires \
  --agent codex --skill mother-in-law --copy -y
```

This invokes the independent [Vercel Labs skills CLI](https://github.com/vercel-labs/skills).
The tested `skills@1.5.26` requires Node.js **22.20.0 or newer**. Our
[local CLI checkpoint, 2026-09-21](../benchmarks/SKILLS-CLI-INSTALL-03.md), source `8114957`,
installs all eight hires and verifies all 51 resource files plus executable smoke
checks in an isolated project. This tests the CLI entrypoint with a local source,
not remote authentication or public availability. Review third-party CLIs and
skill contents before installation; an unpinned CLI can change its requirements.

[Authenticated remote checkpoint01](../benchmarks/REMOTE-INSTALL-01.md),
2026-09-22/source`5e6beab`, also verifies both a pinned GitHub helper installation
and actual npx remote cloning into a temporary project. All8 skills/51 resources
match; nine installed Python entrypoints and selected native behavior pass.
The CLI tarball was cached: no fresh npm download, anonymous public access or
host registration is established.

## Install into a project

Requires Python 3.8+ and Git. From a directory where you keep tools:

```sh
git clone https://github.com/SoonGwan/questionable-hires.git
cd questionable-hires
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills --dry-run
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills
```

Replace the example project path with your project's actual path. To install just one hire, add `--skill necromancer`; repeat `--skill` for several hires. The installer refuses to overwrite any existing target. On a copy error or cancellation it attempts to remove every skill folder created by that invocation, preserving the original error even if cleanup fails. If filesystem permissions prevent cleanup, partial folders can remain: inspect the reported destination before retrying, and preserve unrelated or pre-existing files.

Source skill folders must contain regular local resources, not symbolic links.
The installer checks all selected skills before writing, including during dry
runs, and rejects linked files/directories rather than copying external targets.
Use a trusted checkout that is not being modified concurrently; this preflight
is not a sandbox or a defense against concurrent source replacement.
The installation destination must be outside this checkout's `skills/` source
tree; copying an installation into its own source is rejected, including dry runs.

For all your projects, choose your user skill directory instead:

```sh
python3 scripts/install.py --dest "$HOME/.agents/skills" --skill necromancer
```

Codex discovers skills in `.agents/skills`. Start a new thread; restart Codex if they don't appear. In Codex CLI or the IDE extension:

```text
$necromancer Can this workaround be removed?
$receipt Verify that this fix prevents duplicate submissions.
$friday Review this release's rollback path.
```

In the ChatGPT skill selector, use `@`. Discovery and invocation follow the [official skill documentation](https://learn.chatgpt.com/docs/build-skills). Normal automatic selection remains enabled; narrow descriptions keep the hires focused on their actual jobs.

## Updates and removal

Check an existing project installation against this local checkout without writing:

```sh
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills --skill con-artist --check
```

Omit `--skill` to check all eight. JSON reports missing, changed (bytes or file
modes) and extra resources per hire. Exit 0 means all selected copies match;
2 means differences/missing installs; 1 means the comparison failed (for example,
a linked/special resource or unreadable file). Generated Python cache files are
ignored. No destination is created and no files are replaced, deleted or repaired.
Differences can be personal edits, not just outdated files. This compares only
the local checkout—not remote freshness, model discovery or skill safety. Use a
trusted, quiescent checkout/install; this is not concurrent filesystem isolation.

Run `git pull --ff-only` in your source checkout. Installed skills are copies, so pulling alone does not update them. Compare your installed folder with the corresponding source folder, move the old installed folder to a backup location outside the discovery directory, and rerun the installer for that hire. Preserve any personal edits before replacing a copy.

To uninstall, move only the installed hire folders you selected out of `.agents/skills` into a backup location. Restart the host if needed. This project installs no hooks, background services, credentials, or model settings.

## Plugin package

The repository includes a validated `.codex-plugin/plugin.json`. A local marketplace bundle has also passed an actual CLI install/list/cache-comparison/remove cycle; see the [installation record](INSTALLATION-TEST.md).

To build a new bundle:

The builder rejects symbolic links in the skill tree, plugin metadata, license
and marketplace source before creating output. It does not follow links to
external resources. Build from a trusted checkout without concurrent source
changes; this check is not a security sandbox.
Keep bundle output outside the copied skill and plugin-metadata trees to avoid
self-copying. The documented `dist/bundle` location is outside those trees.

```sh
python3 scripts/build.py --output dist/bundle
codex plugin marketplace list --json
```

If no marketplace named `personal` is already registered, install this local bundle:

```sh
codex plugin marketplace add /absolute/path/to/questionable-hires/dist/bundle
codex plugin add questionable-hires@personal
```

Replace the absolute path. If `personal` already belongs to another source, use the standalone installer above; do not replace your existing marketplace. The bundle directory must stay available while its local marketplace is registered. Build into a new output directory when `dist/bundle` already exists.

To remove this test installation, use `codex plugin remove questionable-hires@personal`. Remove the `personal` marketplace registration only if you created it for this bundle and it has no unrelated use. Public-directory publishing and remote Git marketplace installation are not claimed as tested.

## Developer checks

```sh
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

These checks validate packaging, documentation links, and installer behavior. They do not measure the quality of a model's engineering decisions.
