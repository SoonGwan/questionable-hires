# Hostage single-read callback interface candidate

The [keyed transfer screen](HOSTAGE-KEYED-PUBLISH-01-REVIEW.md) observed separate
entry/reference/asset reads, despite the asset's small implementation. It cost more
than baseline; reading is not established as the sole cause.

The skill now links directly to the asset. The module docstring contains its
callback API, argument-reference semantics, identity/cancellation behavior and
test-owned cleanup/limits. The old reference URL remains as a short redirect for
existing links, but is no longer on the skill's active route. Copied support now
carries its usage with it; no runtime dependency or new execution harness.

Executable AST excluding the module docstring is identical to the asset preserved
in the keyed screen (`d9e7711` implementation). Eight native asset tests pass in
0.246s, including standalone copying, real Form/defect controls and AST comparison.
Fifteen installer tests pass in 2.051s. Repository validation passes.

The single target file is 2,639 bytes; compatibility redirect is 282 bytes.
This reduces the need for separate reads but makes the copied file larger than
the earlier 1,244-byte code asset. File size/read opportunities are not observed
token savings. New route adoption, total task cost and transfer remain unmeasured.
Historical model resources and results are unchanged; no featured chart promotion.
