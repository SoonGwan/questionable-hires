# Owned native pytest01 — frozen runtime FAIL/PASS controls

2026-09-27,parent`cad6ae94`,unchanged8skills,zero models/selected-case tests.
Reuse the readonly official reconstructed root and guest-only binfmt from
[binfmt01](OWNED-GUEST-BINFMT-01.md), exact kernel/modloop/registration inputs.
Do not reapply image layers or change packages/project source.

A private authored driver creates two guest-RAM directories. Each has identical
pytest tests: answer() must return42, and a native Python subprocess must print42.
Only implementation changes from return41 to return42. Run both via actual
`sys.executable -B -m pytest -rA`, cwd matching fixture, same environment and tests.
Keep output, native exit and pytest call-phase reports using an identical local
plugin. Require before nativeexit1/one failed+one passed and after nativeexit0/two
passed, without skips/collection errors. Actual answer assertion should expose
41 versus42 in before output; process0 alone cannot establish test success.
This authored negative/positive control is runtime calibration, not a selected
benchmark repair, independent quality validation or whole-task efficiency result.

Verify core imports, source paths and pinned resource hashes. Guest root/probe
shares readonly; only guest tmpfs receives fixture/source/reports/cache. No host
profiles/install/binfmt changes, external issue/test/gold body or native case run.
Retain original failed controller/runtime attempts and changed hypotheses.
Same180s guest/200s independent parent watchdog with owned process-group cleanup;
each native pytest subprocess timeout30s. Require guest stop and detach after
collection. No token/time saving or all8 update adoption follows from this gate.

## Device-mount intervention addendum — before the next execution

The first driver aborted on a missing observer report before exporting native
stderr; preserve this capture gap and original source/result/log. A second,
missing-report-tolerant collector exposed both native startup failures at pytest's
capture initialization: `/dev/null` absent, nativeexit1, no call-phase reports.
This is not the intended answer assertion failure. Keep both original outcomes.
Next add guest-only devtmpfs at the existing chroot `/dev` mountpoint, leaving
root readonly and tests/native commands unchanged. No `-s`, capture disabling,
package/test alteration or host device access. VM device inventory remains unchanged;
only guest virtual devices are visible. Record device mount exit and require0.
