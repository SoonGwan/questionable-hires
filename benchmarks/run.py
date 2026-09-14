#!/usr/bin/env python3
"""Run independent Codex sessions on synthetic tasks; never score by prose length."""

import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import hashlib
import json
import os
import random
import re
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "Keep the change focused, investigate relevant evidence, and verify your conclusions with appropriate checks."
INDEX_CAPTURE_LIMIT = 20_000_000


def unittest_transcript_candidate(item):
    """Flag a narrow verbose-count mismatch for review, never score the tests.

    Custom runners, multiple invocations, subtests and arbitrary output can defeat
    this heuristic. Silence is not evidence of complete capture.
    """
    command_text = item.get('command', '')
    output = item.get('aggregated_output', '')
    explicit_verbose = ('unittest' in command_text and
                        re.search(r'(?<![\w-])(?:-v|--verbose)(?![\w-])', command_text))
    summaries = re.findall(r'^Ran (\d+) tests? in [^\n]+$', output, re.MULTILINE)
    if len(summaries) != 1:
        return None
    reported = int(summaries[0])
    # Standard verbose method headers, not failure-trace headings or subtest rows.
    observed = len(re.findall(r'^\S+ \([^\n]+\) \.\.\.(?: |$)', output, re.MULTILINE))
    # Programmatic TextTestRunner calls need no CLI -v. Retained native verbose
    # headers can establish a reviewable mismatch without guessing Python syntax.
    # Quiet output with no headers and no explicit verbosity remains unclassified.
    if (explicit_verbose or observed) and observed < reported:
        return dict(item_id=item.get('id'), reported_tests=reported,
                    observed_verbose_headers=observed,
                    interpretation='Possible partial transcript or nonstandard runner output; manual review required.')
    return None


def inspect_capture(stdout, stderr):
    """Describe capture limitations without inventing lost output or scoring quality."""
    events, invalid_lines, non_objects = [], [], []
    for number, line in enumerate(stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            invalid_lines.append(number)
            continue
        if not isinstance(event, dict):
            non_objects.append(number)
            continue
        events.append(event)
    empty_outputs, event_errors, transcript_candidates, missing_summaries = [], [], [], []
    node_missing_summaries = []
    for event in events:
        if event.get('type') in ('error', 'turn.failed'):
            event_errors.append(event.get('type'))
        item = event.get('item')
        if (event.get('type') == 'item.completed' and isinstance(item, dict)
                and item.get('type') == 'command_execution'):
            if not item.get('aggregated_output'):
                empty_outputs.append(item.get('id'))
            candidate = unittest_transcript_candidate(item)
            if candidate:
                transcript_candidates.append(candidate)
            # A shell's last exit may belong to git status, not the test process.
            # This also flags legitimate redirection, setup failures or unrun
            # commands: review evidence, never infer lost capture or test failure.
            if (re.search(r'(?<!\S)-m\s+unittest\b', item.get('command', ''))
                    and not re.search(r'^Ran \d+ tests? in [^\n]+$',
                                      item.get('aggregated_output', ''), re.MULTILINE)):
                missing_summaries.append(dict(
                    item_id=item.get('id'),
                    interpretation='No native unittest count summary in this command output; '
                    'tests may be unrun, redirected, failed during setup, or incompletely captured. '
                    'Review test-specific exit/evidence; shell success alone is insufficient.'))
            # Narrow command-text heuristic, not a shell parser: quoted examples,
            # redirection and unrun branches can also require manual review.
            if re.search(r'''(?<![\w.-])node\s+--test(?=[\s;'\"]|$)''', item.get('command', '')):
                output = re.sub(r'\x1b\[[0-9;]*m', '', item.get('aggregated_output', ''))
                fields = set(re.findall(
                    r'^(?:#|ℹ) (tests|pass|fail|cancelled|skipped) \d+\s*$', output, re.MULTILINE))
                if fields != {'tests', 'pass', 'fail', 'cancelled', 'skipped'}:
                    node_missing_summaries.append(dict(
                        item_id=item.get('id'),
                        interpretation='No complete Node TAP/spec count summary in this command output; '
                        'tests may be unrun, redirected, use another reporter, fail during setup, '
                        'or be incompletely captured. Review test-specific evidence; '
                        'this is not a test-failure or proven-capture-loss verdict.'))
    return events, dict(
        invalid_json_lines=invalid_lines, non_object_json_lines=non_objects,
        empty_command_output_items=empty_outputs, error_event_types=event_errors,
        unittest_transcript_review_candidates=transcript_candidates,
        unittest_missing_summary_review_candidates=missing_summaries,
        node_missing_summary_review_candidates=node_missing_summaries,
        patch_rejection_count=stderr.lower().count('patch rejected'),
        limitation='Empty command output may be legitimate. Nonempty output may still be incomplete. '
                   'These diagnostics neither prove full tool-output capture nor score task success.')


def command(args, cwd, **kwargs):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True, **kwargs).stdout.strip()


def preserve_collector_index(workspace, cell):
    """Retain local index bytes before author git-add, outside model timing."""
    path = workspace / '.git/index'
    try:
        if (workspace / '.git').is_symlink() or not (workspace / '.git').is_dir():
            return dict(status='unavailable', reason='Git directory is not a local directory')
        info = path.lstat()
        if not stat.S_ISREG(info.st_mode) or info.st_size > INDEX_CAPTURE_LIMIT:
            return dict(status='unavailable', reason='Index is not a regular file within 20 MB')
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(descriptor, 'rb') as stream:
            opened = os.fstat(stream.fileno())
            if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                return dict(status='unavailable', reason='Index changed while opening')
            data = stream.read(INDEX_CAPTURE_LIMIT + 1)
        if len(data) > INDEX_CAPTURE_LIMIT:
            return dict(status='unavailable', reason='Index grew beyond 20 MB')
        name = 'git-index.before-collection.bin'
        (cell / name).write_bytes(data)
        return dict(status='retained', file=name, bytes=len(data),
                    mode=stat.S_IMODE(info.st_mode), sha256=hashlib.sha256(data).hexdigest(),
                    artifact_scope='Local raw artifact; binary index is not included by exporter')
    except OSError as error:
        return dict(status='unavailable', reason=type(error).__name__)


def prepare(case, workspace):
    commits = case.get("history") or [{"message": "Initial application", "files": case["files"]}]
    working = case.get('working_files', {})
    if not isinstance(working, dict):
        raise ValueError('working_files must map relative paths to text')
    for name, content in working.items():
        path = Path(name)
        if (not name or str(path) != name or path == Path('.') or path.is_absolute()
                or any(part in ('..', '.git', '.agents', '.codex') for part in path.parts)
                or not isinstance(content, str)):
            raise ValueError('Unsafe working_files input: ' + name)
    for commit in commits:
        for name in commit["files"]:
            path = Path(name)
            if path.is_absolute() or ".." in path.parts or ".git" in path.parts:
                raise ValueError(f"Unsafe fixture path: {name}")
    workspace.mkdir(parents=True)
    command(["git", "init", "-q", "--template="], workspace)
    command(["git", "config", "user.name", "Fixture Author"], workspace)
    command(["git", "config", "user.email", "fixture@example.invalid"], workspace)
    command(["git", "config", "commit.gpgsign", "false"], workspace)
    (workspace / ".git/no-hooks").mkdir()
    command(["git", "config", "core.hooksPath", str(workspace / ".git/no-hooks")], workspace)
    for index, commit in enumerate(commits):
        for name, contents in commit["files"].items():
            target = workspace / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(contents)
        command(["git", "add", "."], workspace)
        env = dict(os.environ, GIT_AUTHOR_DATE=f"2026-01-{index + 1:02d}T12:00:00Z", GIT_COMMITTER_DATE=f"2026-01-{index + 1:02d}T12:00:00Z")
        command(["git", "commit", "-qm", commit["message"]], workspace, env=env)
    for name, content in working.items():
        target = workspace / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
    return command(["git", "rev-parse", "HEAD"], workspace)


def disabled_skills():
    # Disable individually discovered personal skills without editing user config.
    paths = set()
    for root in (Path.home() / ".agents/skills", Path.home() / ".codex/skills"):
        if root.exists():
            for folder in root.iterdir():
                if folder.is_dir():
                    paths.update(p.resolve() for p in folder.rglob("SKILL.md"))
    return sorted(paths)


def prepare_repository(source, workspace):
    """Copy a clean upstream checkout, including its history, without shared Git files."""
    if command(["git", "status", "--porcelain"], source):
        raise ValueError("Upstream source must be clean")
    if not (source / ".git").is_dir():
        raise ValueError("Source must be a standalone clone, not a linked worktree")
    shutil.copytree(source, workspace, ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))
    hooks = workspace / '.git/qh-no-hooks'
    hooks.mkdir(exist_ok=True)
    command(['git', 'config', 'core.hooksPath', str(hooks)], workspace)
    command(['git', 'config', 'commit.gpgsign', 'false'], workspace)
    return command(['git', 'rev-parse', 'HEAD'], workspace)


def resource_manifest(root):
    """Inventory installed bytes/modes without following symlink targets."""
    for candidate in (root.parent, root):
        if candidate.is_symlink():
            return {'.': dict(kind='symlink-root', target=os.readlink(candidate))}
    manifest = {}
    for path in sorted(root.rglob('*')):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            manifest[name] = dict(kind='symlink', target=os.readlink(path))
        elif path.is_file():
            manifest[name] = dict(kind='file', sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                  mode=path.stat().st_mode & 0o777)
    return manifest


def resource_digest(root):
    """Hash paths, kinds, modes and bytes represented by resource_manifest."""
    encoded = json.dumps(resource_manifest(root), sort_keys=True,
                         separators=(',', ':')).encode()
    return hashlib.sha256(encoded).hexdigest()


def run_cell(case, arm, repeat, output, model, effort, timeout, disabled,
             skills_root=None, project_source=None, launcher=None,
             workspace_root=None):
    if project_source and case.get('working_files'):
        raise ValueError('working_files is only supported for authored fixtures')
    skills_root = skills_root or ROOT / "skills"
    cell = output / f"{case['id']}--{arm}--{repeat}"
    cell.mkdir()
    if workspace_root:
        allocated_workspace = workspace_root / f"{case['id']}--{arm}--{repeat}" / 'project'
        allocated_workspace.parent.mkdir(parents=True)
    else:
        allocated_workspace = Path(tempfile.mkdtemp(prefix="qh-eval-")) / "project"
    # Use the same physical root for preparation, CLI -C, installed resources and
    # evidence paths. macOS temporary directories may have /var and /private/var
    # aliases; do not broaden writable roots to accommodate different spellings.
    workspace = allocated_workspace.resolve()
    base = prepare_repository(project_source, workspace) if project_source else prepare(case, workspace)
    initial_diff, initial_tree = None, base
    if case.get('working_files'):
        # Record initial content without staging the user's fixture changes or
        # creating a commit. This tree is only an author-side diff reference.
        with tempfile.TemporaryDirectory(prefix='qh-initial-', dir=workspace / '.git') as scratch:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(scratch) / 'index'))
            command(['git', 'read-tree', base], workspace, env=env)
            command(['git', 'add', '--all', '--', '.'], workspace, env=env)
            command(['git', 'add', '--force', '--', *case['working_files']], workspace, env=env)
            initial_tree = command(['git', 'write-tree'], workspace, env=env)
        initial_diff = command(['git', 'diff', base, initial_tree, '--', '.'], workspace)
    project_kind = "local repository" if project_source else "synthetic project"
    prompt = case["task"] + f"\n\nWork only inside this {project_kind}. Do not use external services or other installed skills. Do not delegate."
    if arm == "auto":
        prompt = case["task"] + f"\n\nWork only inside this {project_kind}. Do not use external services. Do not delegate."
    skill_hash = None
    skill_resources_hash = None
    if arm in {"skill", "auto"}:
        source = skills_root / case["skill"]
        if arm == "auto":
            for hire in skills_root.iterdir():
                if (hire / "SKILL.md").is_file():
                    shutil.copytree(hire, workspace / ".agents/skills" / hire.name)
        else:
            shutil.copytree(source, workspace / ".agents/skills" / case["skill"])
        skill_hash = hashlib.sha256((workspace / '.agents/skills' / case['skill'] / 'SKILL.md').read_bytes()).hexdigest()
        skill_resources_hash = resource_digest(workspace / '.agents/skills' / case['skill'])
        if arm == "skill":
            prompt = f"Use ${case['skill']} at .agents/skills/{case['skill']}/SKILL.md.\n\n" + prompt
    elif arm == "control":
        prompt += "\n\n" + CONTROL
    installed_root = workspace / '.agents/skills'
    installed_before = resource_manifest(installed_root)
    config = "skills.config=[" + ",".join("{path=" + json.dumps(str(p)) + ",enabled=false}" for p in disabled) + "]"
    args = ["codex", "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral", "--sandbox", "workspace-write", "--model", model,
            "-c", f'model_reasoning_effort="{effort}"', "-c", config, "--json", "-C", str(workspace), prompt]
    execution = 'host-workspace-write'
    if launcher:
        args = launcher(workspace, args)
        execution = 'external-container'
    started = time.monotonic()
    process = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
    duration = round(time.monotonic() - started, 3)
    # Save received CLI streams before inspecting the possibly modified project.
    # Later Git/snapshot failures must not discard an already-paid execution.
    # This preserves emitted text, not output omitted upstream by the CLI.
    def redact(text):
        return text.replace(str(workspace), "<WORKSPACE>").replace(str(Path.home()), "<HOME>")
    (cell / "stdout.original.jsonl").write_text(stdout)
    (cell / "stderr.original.txt").write_text(stderr)
    (cell / "events.jsonl").write_text(redact(stdout))
    (cell / "stderr.txt").write_text(redact(stderr))
    collector_index = preserve_collector_index(workspace, cell)
    (cell / 'git-index.before-collection.json').write_text(json.dumps(collector_index, indent=2) + '\n')
    try:
        installed_after = resource_manifest(installed_root)
        resource_diagnostics = dict(changed_paths=sorted(
            name for name in installed_before.keys() | installed_after.keys()
            if installed_before.get(name) != installed_after.get(name)))
    except OSError as error:
        installed_after = None
        resource_diagnostics = dict(error=type(error).__name__)
    events, capture_diagnostics = inspect_capture(stdout, stderr)
    messages = [e["item"]["text"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
    usage = next((e.get("usage") for e in reversed(events) if e.get("type") == "turn.completed"), None)
    command(["git", "add", "-N", "."], workspace)
    if initial_diff is not None:
        present = [name for name in case['working_files']
                   if (workspace / name).exists() or (workspace / name).is_symlink()]
        if present:
            command(['git', 'add', '-N', '--force', '--', *present], workspace)
    diff = command(["git", "diff", initial_tree, "--", ".", ":(exclude).agents", ":(exclude)__pycache__"], workspace)
    (cell / "answer.md").write_text(redact("\n\n".join(messages)) + "\n")
    (cell / "changes.diff").write_text(redact(diff) + "\n")
    if initial_diff is not None:
        (cell / 'initial.diff').write_text(redact(initial_diff) + '\n')
    snapshot = cell / "project"
    shutil.copytree(workspace, snapshot, ignore=shutil.ignore_patterns(".git", ".agents", "__pycache__"))
    limited = any(term in (stdout + stderr).lower() for term in
                  ("usage_limit_reached", "usage limit", "rate_limit_exceeded", "insufficient_quota", "billing hard limit"))
    meta = {"limit_detected": limited, "attempted": True, "case": case["id"], "skill": case["skill"], "arm": arm, "repeat": repeat, "model": model, "reasoning_effort": effort,
            "base_commit": base, "skill_sha256": skill_hash,
            "skill_resources_sha256": skill_resources_hash,
            "elapsed_seconds": duration, "exit_code": process.returncode,
            "timed_out": timed_out, "usage": usage, "completed": usage is not None and process.returncode == 0 and not timed_out,
            "workspace": str(workspace), "allocated_workspace": str(allocated_workspace),
            "prompt": prompt, "disabled_personal_skills": len(disabled),
            "execution": execution,
            "capture_diagnostics": capture_diagnostics,
            "installed_resources_before": installed_before,
            "installed_resources_after": installed_after,
            "resource_diagnostics": resource_diagnostics}
    meta['pre_collection_index'] = collector_index
    if initial_diff is not None:
        meta['initial_tree'] = initial_tree
        meta['initial_working_files'] = {name: hashlib.sha256(content.encode()).hexdigest()
                                         for name, content in case['working_files'].items()}
    (cell / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory; contains logs requiring review before publication")
    parser.add_argument("--case", action="append")
    parser.add_argument("--suite", choices=["main", "clean"], default="main")
    parser.add_argument("--cases-file", type=Path, help="Separate preregistered task set; overrides --suite")
    parser.add_argument("--skills-root", type=Path, default=ROOT / "skills", help="Skill snapshot to evaluate without modifying installed or working skills")
    parser.add_argument("--arms", nargs="+", choices=["baseline", "control", "skill", "auto"], default=["baseline", "control", "skill"])
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20260911)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--model", default="gpt-6-astra")
    parser.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh"])
    args = parser.parse_args()
    if min(args.repeats, args.jobs, args.timeout) < 1:
        parser.error("repeats, jobs, and timeout must be positive")
    if args.jobs > 3:
        parser.error("jobs must not exceed 3")
    cases_path = args.cases_file or ROOT / "benchmarks" / ("cases.json" if args.suite == "main" else "clean-cases.json")
    cases = json.loads(cases_path.read_text())
    seen = set()
    for case in cases:
        for field in ("id", "skill"):
            value = case.get(field, "")
            if not value or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in value):
                parser.error(f"Invalid case {field}: {value!r}")
        if case["id"] in seen:
            parser.error(f"Duplicate case: {case['id']}")
        seen.add(case["id"])
    if args.case:
        unknown = set(args.case) - {c["id"] for c in cases}
        if unknown:
            parser.error(f"Unknown cases: {sorted(unknown)}")
        cases = [c for c in cases if c["id"] in args.case]
    if not cases:
        parser.error("Task set must not be empty")
    skills_root = args.skills_root.resolve()
    if set(args.arms) & {"skill", "auto"}:
        for case in cases:
            if not (skills_root / case["skill"] / "SKILL.md").is_file():
                parser.error(f"Missing skill: {case['skill']}")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    schedule = [(case, arm, repeat) for repeat in range(1, args.repeats + 1)
                for case in cases for arm in dict.fromkeys(args.arms)]
    random.Random(args.seed).shuffle(schedule)
    manifest = {"jobs": args.jobs, "timeout_seconds": args.timeout, "seed": args.seed,
                "schedule": [f"{c['id']}--{a}--{r}" for c, a, r in schedule],"started_at": datetime.now(timezone.utc).isoformat(), "revision": command(["git", "rev-parse", "HEAD"], ROOT),
                "codex_version": command(["codex", "--version"], ROOT), "model": args.model, "effort": args.effort,
                "arms": args.arms, "repeats": args.repeats, "case_ids": [c["id"] for c in cases],
                "suite": "custom" if args.cases_file else args.suite, "cases_sha256": hashlib.sha256(cases_path.read_bytes()).hexdigest(),
                "skill_snapshot_sha256": {p.parent.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(skills_root.glob("*/SKILL.md"))},
                "skill_resources_sha256": {p.parent.name: resource_digest(p.parent)
                                             for p in sorted(skills_root.glob("*/SKILL.md"))},
                "limitation": "Synthetic tasks; runtime system instructions remain. Personal skills disabled where discovered; review traces for contamination."}
    (output / "run.json").write_text(json.dumps(manifest, indent=2) + "\n")
    disabled = disabled_skills()
    incomplete = False
    stopped = False
    pending = iter(schedule)
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        running = {}
        def submit():
            item = next(pending, None)
            if item is not None:
                case, arm, repeat = item
                running[pool.submit(run_cell, case, arm, repeat, output, args.model, args.effort, args.timeout, disabled, skills_root)] = item
        for _ in range(args.jobs):
            submit()
        while running:
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                case, arm, repeat = running.pop(future)
                try:
                    result = future.result()
                except Exception as error:
                    result = {"case": case["id"], "arm": arm, "repeat": repeat, "attempted": True,
                              "completed": False, "usage": None, "timed_out": False,
                              "error": f"{type(error).__name__}: {error}"}
                    cell = output / f"{case['id']}--{arm}--{repeat}"
                    cell.mkdir(exist_ok=True)
                    (cell / "metadata.json").write_text(json.dumps(result, indent=2) + "\n")
                incomplete = incomplete or not result["completed"]
                stopped = stopped or result.get("limit_detected", False)
                print(f"{case['id']} {arm} #{repeat}: {'completed' if result['completed'] else 'incomplete'} ({result.get('elapsed_seconds')}s)", flush=True)
            if not stopped:
                for _ in done:
                    submit()
        for case, arm, repeat in pending:
            cell = output / f"{case['id']}--{arm}--{repeat}"
            cell.mkdir()
            (cell / "metadata.json").write_text(json.dumps({"case": case["id"], "arm": arm, "repeat": repeat,
                "attempted": False, "completed": False, "timed_out": False, "usage": None,
                "status": "unattempted_after_account_limit"}, indent=2) + "\n")
    manifest["finished_at"] = datetime.now(timezone.utc).isoformat()
    manifest["stopped_after_limit"] = stopped
    (output / "run.json").write_text(json.dumps(manifest, indent=2) + "\n")
    if incomplete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
