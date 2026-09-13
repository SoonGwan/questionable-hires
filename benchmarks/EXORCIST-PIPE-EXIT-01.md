# Foreground-exit pipe cleanup — 2026-09-14

Local runtime fix `b861c4e`, compared with `17a0901`; not a model benchmark.

A foreground command that exits can leave a descendant holding its output pipe.
Previously the wrapper waited until its whole deadline before killing that group,
reporting `timed_out: true` despite the direct command having exited with status 7.
This adds avoidable delay for a tool that already promises to clean remaining
group members after foreground completion.

The selector now checks direct-child exit at most every 50 ms, subject to OS
scheduling, and starts its existing group cleanup immediately on observing exit.
It then drains buffered output under the original deadline. A live direct command
still receives its deadline; escaped groups remain outside containment. This
changes descendant lifetime: remaining background work is stopped sooner. Do not
use the tool for launchers whose background jobs are supposed to survive them.

## Native comparison

Three alternating previous/candidate runs, timeout 2 seconds, on the same host:

| Repeat | Previous seconds | Candidate seconds | Previous timeout | Candidate timeout |
| --- | ---: | ---: | --- | --- |
| 1 | 2.003 | 0.107 | true | false |
| 2 | 2.003 | 0.108 | true | false |
| 3 | 2.002 | 0.107 | true | false |

Every result retains child exit 7, output `parent done\n`, no output truncation
and direct-child cleanup confirmation. Candidate mean is about 0.107 seconds
versus 2.003 seconds. This is a selected local idle-descendant case with changed
cleanup timing, not equal completed descendant work or general developer savings.
No token or model-session speed claim; no featured chart update.

Reproduce from the repository root (spawns only owned local sleeping descendants):

```sh
PYTHONPATH=skills/exorcist/scripts python3 -B - <<'PY'
import json, subprocess, sys
import run_probe
old = {'__name__': 'previous_probe'}
exec(compile(subprocess.check_output([
    'git', 'show', '17a0901:skills/exorcist/scripts/run_probe.py'
], text=True), 'previous_probe', 'exec'), old)
code = ('import subprocess,sys; subprocess.Popen([sys.executable,"-c",'
        '"import time; time.sleep(20)"]); print("parent done",flush=True); sys.exit(7)')
for repeat in range(3):
    for label, run in [('previous', old['run']), ('candidate', run_probe.run)]:
        print(json.dumps(dict(repeat=repeat+1, version=label,
            **run([sys.executable, '-B', '-c', code], timeout=2))), flush=True)
PY
```

## Checks and limits

15 probe-runner tests pass in 3.562s: actual success/failure, nested forwarded
output/status, genuine blocking/cancellation-suppression deadlines, closed output,
early-exit inherited pipe, bounded Unicode tail draining and mocked incomplete
cleanup/interruption. Four runtime/signal/provenance/adoption tests pass in 1.146s.
Skill metadata validation passes. This is not a full-suite or hosted-CI result.

`cleanup_complete` still confirms only direct-child exit, not every descendant.
Tests do not prove process isolation, escaped-child containment, adversarial
concurrent PID reuse safety or a hard OS scheduling guarantee. Diagnostic scripts
must still be trusted and authorized. No model-session result has measured this
version's adoption or aggregate performance.

Subsequent full local regression at launch `ead49db`: **428 tests passed in
169.970s** on macOS/Python 3.9.6, no skips reported. No executable changes or model
benchmark ran concurrently. [Release gate](../docs/RELEASE-READINESS.md) separates
this result from the current hosted account restriction and older Linux checks.
