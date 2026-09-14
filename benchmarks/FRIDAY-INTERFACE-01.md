# Friday interface split — 2026-09-14

Instruction resource `1c483b9`; runtime remains `bef0937`. This is an unmeasured
documentation/routing candidate, not a new performance result.

Literal-reader screen 01 confirmed CLI adoption but recorded +10.07% tokens and
−24.73% time with unequal work. That model loaded the entire 6,447-byte interface,
including Python embedding/BLOB and detailed byte-accounting explanations unused
by its ordinary CLI recipe. This motivates progressive disclosure; it does not
prove how much of the measured cost those paragraphs caused.

The core CLI guide is now **3,733 bytes**; optional API/result details are **2,821
bytes**, **6,554 combined**. These are UTF-8 file sizes, not tokenizer counts,
model input savings or execution speed. Advanced workflows may read both files
and incur another tool call. No reduction is claimed for them.

The core retains the executable recipe, actual-consumer requirement, literal
reference grammar and dynamic-module rejection, source provenance limitation,
completion/exit semantics, partial/truncated-result warnings, read-only controls,
path limits and major byte/SQL-time budgets. Python API/BLOB representation,
duplicate/empty-column details and exact byte accounting move to a linked guide
selected only for those needs. No caller is authorized to omit required checks,
rewrite unsupported migrations or mistake static declarations for runtime binding.

Native validation: **35 Friday tests pass in 0.924s**, including execution of
the core guide's JSON recipe through real schema transitions and the relocated
Python API example with BLOB output. Original schema files remain unchanged in
the new example check. **15 install tests pass in 1.986s**, including complete
resource copying, standalone/marketplace equality and installed entrypoint runs.
Skill/repository validation and featured synchronization pass. Runtime code is
unchanged, and no new whole-suite count or model result is implied.

Next behavioral evidence must check both ordinary CLI use and a workflow needing
advanced details. Reading fewer bytes only helps if required semantics and
delivery survive; do not repeatedly run the favorable task alone or treat file
size reduction as a model-performance benchmark. Earlier measurements and
featured charts stay tied to their measured resources.
