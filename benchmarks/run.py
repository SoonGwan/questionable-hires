#!/usr/bin/env python3
"""Run independent Codex sessions on synthetic tasks; never score by prose length."""

import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from datetime import datetime, timezone
import hashlib
import json
import os
import random
from pathlib import Path
import shutil
import signal
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
CONTROL = "Keep the change focused, investigate relevant evidence, and verify your conclusions with appropriate checks."


def command(args, cwd, **kwargs):
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=True, **kwargs).stdout.strip()


def prepare(case, workspace):
    commits = case.get("history") or [{"message": "Initial application", "files": case["files"]}]
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


def run_cell(case, arm, repeat, output, model, effort, timeout, disabled):
    cell = output / f"{case['id']}--{arm}--{repeat}"
    cell.mkdir()
    workspace = Path(tempfile.mkdtemp(prefix="qh-eval-")) / "project"
    base = prepare(case, workspace)
    prompt = case["task"] + "\n\nWork only inside this synthetic project. Do not use external services or other installed skills. Do not delegate."
    if arm == "auto":
        prompt = case["task"] + "\n\nWork only inside this synthetic project. Do not use external services. Do not delegate."
    skill_hash = None
    if arm in {"skill", "auto"}:
        source = ROOT / "skills" / case["skill"]
        if arm == "auto":
            for hire in (ROOT / "skills").iterdir():
                if (hire / "SKILL.md").is_file():
                    shutil.copytree(hire, workspace / ".agents/skills" / hire.name)
        else:
            shutil.copytree(source, workspace / ".agents/skills" / case["skill"])
        skill_hash = hashlib.sha256((source / "SKILL.md").read_bytes()).hexdigest()
        if arm == "skill":
            prompt = f"Use ${case['skill']} at .agents/skills/{case['skill']}/SKILL.md.\n\n" + prompt
    elif arm == "control":
        prompt += "\n\n" + CONTROL
    config = "skills.config=[" + ",".join("{path=" + json.dumps(str(p)) + ",enabled=false}" for p in disabled) + "]"
    args = ["codex", "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral", "--sandbox", "workspace-write", "--model", model,
            "-c", f'model_reasoning_effort="{effort}"', "-c", config, "--json", "-C", str(workspace), prompt]
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
    events = []
    for line in stdout.splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    messages = [e["item"]["text"] for e in events if e.get("type") == "item.completed" and e.get("item", {}).get("type") == "agent_message"]
    usage = next((e.get("usage") for e in reversed(events) if e.get("type") == "turn.completed"), None)
    command(["git", "add", "-N", "."], workspace)
    diff = command(["git", "diff", base, "--", ".", ":(exclude).agents", ":(exclude)__pycache__"], workspace)
    def redact(text):
        return text.replace(str(workspace), "<WORKSPACE>").replace(str(Path.home()), "<HOME>")
    (cell / "stdout.original.jsonl").write_text(stdout)
    (cell / "stderr.original.txt").write_text(stderr)
    (cell / "events.jsonl").write_text(redact(stdout))
    (cell / "stderr.txt").write_text(redact(stderr))
    (cell / "answer.md").write_text(redact("\n\n".join(messages)) + "\n")
    (cell / "changes.diff").write_text(redact(diff) + "\n")
    snapshot = cell / "project"
    shutil.copytree(workspace, snapshot, ignore=shutil.ignore_patterns(".git", ".agents", "__pycache__"))
    limited = any(term in (stdout + stderr).lower() for term in
                  ("usage_limit_reached", "usage limit", "rate_limit_exceeded", "insufficient_quota", "billing hard limit"))
    meta = {"limit_detected": limited, "attempted": True, "case": case["id"], "skill": case["skill"], "arm": arm, "repeat": repeat, "model": model, "reasoning_effort": effort,
            "base_commit": base, "skill_sha256": skill_hash, "elapsed_seconds": duration, "exit_code": process.returncode,
            "timed_out": timed_out, "usage": usage, "completed": usage is not None and process.returncode == 0 and not timed_out,
            "workspace": str(workspace), "prompt": prompt, "disabled_personal_skills": len(disabled)}
    (cell / "metadata.json").write_text(json.dumps(meta, indent=2) + "\n")
    return meta


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New output directory; contains logs requiring review before publication")
    parser.add_argument("--case", action="append")
    parser.add_argument("--suite", choices=["main", "clean"], default="main")
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
    cases_path = ROOT / "benchmarks" / ("cases.json" if args.suite == "main" else "clean-cases.json")
    cases = json.loads(cases_path.read_text())
    if args.case:
        unknown = set(args.case) - {c["id"] for c in cases}
        if unknown:
            parser.error(f"Unknown cases: {sorted(unknown)}")
        cases = [c for c in cases if c["id"] in args.case]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    schedule = [(case, arm, repeat) for repeat in range(1, args.repeats + 1)
                for case in cases for arm in dict.fromkeys(args.arms)]
    random.Random(args.seed).shuffle(schedule)
    manifest = {"jobs": args.jobs, "timeout_seconds": args.timeout, "seed": args.seed,
                "schedule": [f"{c['id']}--{a}--{r}" for c, a, r in schedule],"started_at": datetime.now(timezone.utc).isoformat(), "revision": command(["git", "rev-parse", "HEAD"], ROOT),
                "codex_version": command(["codex", "--version"], ROOT), "model": args.model, "effort": args.effort,
                "arms": args.arms, "repeats": args.repeats, "case_ids": [c["id"] for c in cases],
                "suite": args.suite, "cases_sha256": hashlib.sha256(cases_path.read_bytes()).hexdigest(),
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
                running[pool.submit(run_cell, case, arm, repeat, output, args.model, args.effort, args.timeout, disabled)] = item
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
