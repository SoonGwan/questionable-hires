# Onboarding

The repository is private. GitHub access is required to clone it. Installing a skill does not select your model or change your approval settings.

## Install into a project

Requires Python 3.8+ and an authenticated Git client. From a directory where you keep tools:

```sh
git clone https://github.com/SoonGwan/questionable-hires.git
cd questionable-hires
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills --dry-run
python3 scripts/install.py --dest /absolute/path/to/your-project/.agents/skills
```

Replace the example project path with your project's actual path. To install just one hire, add `--skill necromancer`; repeat `--skill` for several hires. The installer refuses to overwrite any existing target and rolls back newly created skill folders on a copy error.

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

Run `git pull --ff-only` in your source checkout. Installed skills are copies, so pulling alone does not update them. Compare your installed folder with the corresponding source folder, move the old installed folder to a backup location outside the discovery directory, and rerun the installer for that hire. Preserve any personal edits before replacing a copy.

To uninstall, move only the installed hire folders you selected out of `.agents/skills` into a backup location. Restart the host if needed. This project installs no hooks, background services, credentials, or model settings.

## Plugin package

The repository includes a validated `.codex-plugin/plugin.json`. A local marketplace bundle has also passed an actual CLI install/list/cache-comparison/remove cycle; see the [installation record](INSTALLATION-TEST.md).

To build a new bundle:

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
