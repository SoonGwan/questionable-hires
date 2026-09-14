# Current all-eight skills CLI installation — 2026-09-14

Source archive `45fe88e`, CLI `skills@1.5.26` from npm. Package repository metadata
points to [Vercel Labs skills](https://github.com/vercel-labs/skills). Package SHA-1
`1fa24b1ae298034ec5153277630a05433a3f42a9`; integrity
`sha512-D5jnWoMPDRQ3fJM3RpQH8SBrAS9tmVlTC7OdOB2tk7D6nORbRnw8RLwjVj81IIGlxwWuBthEgUChM7SOZGvTHQ==`.
The tested package declares Node `>=22.20.0`. Resolved runtime dependencies:
tar 7.5.22, yaml 2.9.1, @isaacs/fs-minipass 4.0.1, chownr 3.0.0,
minipass 7.1.3, minizlib 3.1.0 and yallist 5.0.0.

## Environment and scope

The initial host `npx --no-install skills --help` found no cached executable and
exited 1. We downloaded the pinned tarball and installed its runtime dependencies
only under ignored `benchmarks/local-runs/skills-cli-1.5.26.iU4Ah2`, with npm
lifecycle scripts disabled. No global npm install, account setup or host agent
registration. The tarball/cache/runtime remain available locally.

Actual CLI execution occurs in disposable Linux arm64 containers, Node v24.20.0,
Python 3.12.3, existing image
`sha256:59f6ca68c1b94db38c241951f74f3a40b377afff5cc87fbf873154b8531df350`.
Network disabled, telemetry opt-out flags set, source and CLI mounted read-only.
The CLI installs only into a fresh temporary Codex project inside the container.
No private Git credentials are mounted. This tests the installed CLI entrypoint,
not an end-to-end remote `npx` registry/authentication workflow.

## Observed results

[Corrected checker output](results/skills-cli-install-01/install-check.json)
retains commands, outputs and all resource hashes/modes:

- `add <source> --list` lists the eight hires without creating project skills.
- `add <source> --agent codex --skill '*' --copy -y` installs exactly eight.
- All **38 files** within the selected skill folders match source bytes and modes;
  no symlinks or missing resources. Source remains unchanged.
- All **seven Python script entrypoints** execute `--help` from installed copies
  under isolated Python, outside the source checkout.
- Installed Python and JavaScript task-aware callbacks execute, preserve argument
  and returned-object identity and complete owned task cleanup.

The [first checker failure](results/skills-cli-install-01/initial-checker-error.txt)
included the catalog `skills/README.md` in the expected installed inventory.
That file is outside every installable skill. The checker now derives inventory
from the eight selected `SKILL.md` directories; it does not drop any per-skill
file. The corrected run passes without modifying source or the third-party CLI.

`check_skills_cli_install.py` reproduces the check given a trusted source archive
and installed CLI entrypoint. It does not fetch packages or change global installs.
Native feature behavior is only a smoke test, not exhaustive skill behavior,
automatic selection, model efficiency, authenticated remote installation or public
availability. Repository visibility and featured performance charts are unchanged.
