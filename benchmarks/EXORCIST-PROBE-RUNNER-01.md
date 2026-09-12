# Probe runner adoption: mechanics reused, no efficiency win

Candidate `24c05ed`, clean execution HEAD `d3b157d`. One fresh GPT-6 Astra medium
skill session on the existing search diagnosis development task. No rerun,
baseline, exclusion or full-team screen. Raw evidence is retained under ignored
`local-runs/exorcist-runner-02` (the directory name is not a second helper trial).

| Sample | Input including cache + output tokens | Seconds |
| --- | ---: | ---: |
| Bounded instructions, hand-written process deadline | 86,090 | 52.371 |
| Optional probe runner | 89,674 | 52.353 |

Tokens increase 4.2%; wall time is effectively unchanged. Against screen 05's
unbounded diagnosis, both remain more expensive. Do not call helper adoption a
performance improvement or attribute these separated single-sample costs causally.

The model uses the installed runner once, removing the previous script's signal
alarm and outer timeout plumbing. The new probe retains bounded signal/task waits
and task cancellation; process cleanup is protected only when invoked through the
documented wrapper. Its recorded result checks actual Search and transport, both
response orders, fresh cache-free responses, and no-cache headers. The diagnosis
and production-uncertainty statement remain correct.

However, the model reads the full helper source together with its reference,
despite the interface-only usage guidance. It also writes a JSON result artifact
and then reads it in another command. This preserves evidence but adds work;
neither source inspection nor artifact retention was required by this tiny task.
Do not add ever-stronger prohibitions based on one sample or remove useful
inspection authority. Interface adoption alone does not guarantee lower context cost.

The empty-output diagnostic is expected: the runner command redirects stdout to
the new result file; the next captured command displays the complete JSON. Its
child exit is 0, timeout false, output untruncated. No rejected patch. Author
inspection confirms both original files are unchanged and all four installed
Exorcist resources match `24c05ed`. A separate author replay through the same
wrapper reproduces both final-result outcomes with exit 0. It does not replace
or retroactively supplement the model's original evidence.

Disposition: functional optional runner, efficiency hypothesis not established.
Keep the adverse result. Repeatedly rerunning this exposed task or adding more
mandatory instructions is not the next step; broader representative work and
lighter tool discovery must justify further changes. No new all-skill claim.
