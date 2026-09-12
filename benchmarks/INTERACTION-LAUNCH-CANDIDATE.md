# Shared browser launch prerequisite

Candidate following the [blocked browser screen](BROWSER-MODEL-01-REVIEW.md).
The skill arm launched Chrome separately per browser test despite an identical
pre-page SIGABRT/EPERM failure. This repeats unavailable shared setup, not useful
independent interaction evidence. It then wrote a second fake-DOM suite, whose
limits were honest but whose work did not complete the requested browser QA.

The entrypoint now routes shared launch through suite setup or the first relevant
check, without prescribing an additional smoke invocation on successful paths.
An unchanged shared launch failure leaves dependent cases unrun with diagnostics;
changed conditions or evidence of a transient cause can justify another attempt.
Individual page/assertion failures must not suppress unrelated cases. Successful
launch still requires isolated per-case state. Lower-layer checks are optional
and question-driven, never a substitute for rendered evidence.

No host permissions or benchmark results changed. This revision has no model
adoption or resource-savings measurement. It cannot repair the sandbox runtime.
Forward validation must cover both shared launch failure and a working browser
with one failing interaction, checking that the latter does not skip other cases.
