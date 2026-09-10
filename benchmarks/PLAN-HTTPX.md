# HTTPX test-sensitivity comparison: frozen tasks

Source: HTTPX 0.28.1 at `26d48e0634e6ee9cdc0533996db289ce4b430177`; see [environment preflight](HTTPX-PREFLIGHT.md). Preserve the complete source checkout and license in each isolated project. No evaluated model sessions have run at plan creation.

## Neutral requests

1. **WSGI cleanup:** Audit whether `tests/test_wsgi.py` protects response-iterable cleanup when a client closes a response. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.
2. **ASGI HEAD:** Audit whether `tests/test_asgi.py` protects HEAD response-body handling. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is missing, propose a focused test and verify it against correct and faulty behavior. Do not change the original source or tests.
3. **ASGI exceptions:** Audit whether `tests/test_asgi.py` protects default application-exception propagation. Demonstrate test sensitivity with a narrow isolated behavioral mutation. If coverage is adequate for the targeted fault, report that without demanding a stronger test. Do not change the original source or tests.

These targets were chosen from reading the transport/test files, before executing mutation oracles or evaluating agents. They are bounded audits, not hidden bug-fixing tickets. The targeted contracts are supplied equally to every condition. Adequate existing tests are a valid outcome. No fault is preinstalled in an evaluated checkout.

## Conditions and scoring

No-skill baseline, the existing generic control instruction, and Con Artist pinned at `bf420fe`: three tasks × three conditions × three independent repetitions = 27 sessions. Astra medium, concurrency one, 360-second cell limit, no cell retries. Randomize the 27-cell schedule once with seed 20260912 and record it before execution. Stop scheduling after an explicit account limit; retain partial evidence. Preinstall dependencies identically, tell all conditions the interpreter path, disallow external services and dependency installation during tasks.

Freeze runnable harness and environment before launch. Existing synthetic `run.py` cannot yet load a full upstream checkout; do not mislabel synthetic file copies as this experiment. Evaluated agents may create only local disposable mutation copies and diagnostic artifacts; prohibit upstream network writes and changes to the original checkout's existing files. Do not give agents oracle source, expected mutations, scoring notes, or previous answers.

For each cell review separately: (1) baseline actually runs and is green, (2) a reachable contract-breaking mutation is isolated and the relevant upstream tests are executed against it, (3) the observed survivor/killed conclusion matches commands, (4) any proposed new regression passes correct behavior and fails the chosen fault, or existing protection is correctly demonstrated, (5) original tracked files remain intact. Missing evidence is unknown, not pass; infrastructure failure is separate from a wrong finding. All five required for strict success. Do not award points for more mutations or longer prose.

Before grading, independently establish fault reachability and test sensitivity with local oracles. The oracle is development/author knowledge; evaluator contexts must exclude it. Record oracle surprises rather than editing requests to favor a condition. Author grading remains unblinded and public-code model familiarity remains possible. Report quality first, raw token/time data second, with per-task outcomes and all failures. This is one real repository, not evidence for every skill or general superiority.
