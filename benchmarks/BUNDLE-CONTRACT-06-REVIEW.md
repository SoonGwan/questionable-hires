# All-eight checkpoint 06 — review in progress

Resource/launch `20ec916`; [frozen protocol](BUNDLE-CONTRACT-06-PROTOCOL.md).
No aggregate result until all scheduled cells finish and evidence is reviewed.
No resource/task edits or author replay/test workloads during model timing.

## Persistence audit — baseline

Completed: **85,571 recorded tokens / 82.170 seconds**, five shell calls.
Builds project-local disposable correct/faulty copies and custom native runner.
Checks actual test function binding, loaded file/source and runtime reachability.
Same stronger assertion preserves the pre-existing record and requires append.

First audit aborts on its own reachability assertion: the no-op mutation line
does not produce the expected line event, despite the existing native test
passing. Model repairs the trace to record the actual function call and reached
return, then reruns the audit. This is retained in-session repair, not an author
retry or proof the production test detected the fault. The first shell payload
ends with git status, so its shell status can mask the earlier Python failure;
the traceback remains in original output and is not a successful audit.

Final native evidence captures correct stronger pass, faulty existing pass and
faulty stronger AssertionError (`['pre-existing']` versus the appended record).
Both audit command outputs lack their leading correct-existing section. Thus a
complete four-check native transcript cannot be claimed; later control flow and
final prose do not replace missing original output. Empty final git-status output
is legitimate and unrelated. Automatic nonempty-output diagnostics miss this gap.

Custom subprocess calls lack their own timeout; the outer model-cell deadline
remains. Extra tracing/source checks and the repair add work beyond basic binding
verification. No observed project-scope violation. Final native hashes, entry
inventory and explicit owned-directory removal are captured; source/raw/resource
reconciliation remains pending. Final recommendation correctly reports missed
write and stronger-test detection, subject to the capture limitation above.
