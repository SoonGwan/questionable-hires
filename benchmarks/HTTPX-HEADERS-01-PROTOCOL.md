# Header audit: separate two-boundary transfer

Freeze Con Artist at `a2b6258` (indexed context, native probes and batch audits).
Use the pinned full HTTPX source/environment from previous protocols, without
changing source or injecting author tests into evaluated projects. The new
`headers-audit` profile defines one request with two independently material
contracts: case-insensitive `Headers.__getitem__` and repeated ordered values
from default `Headers.get_list`. This is a new author-selected task, not a
maintainer ticket or broad holdout. Earlier adverse single-boundary runs remain.

Two fresh sessions, baseline and skill, one repetition each, GPT-6 Astra medium,
serial skill-first order, seed 20260912, 360-second deadline. No retries/exclusions
or resource changes during execution. Existing tests preflight again; do not run
heavy author regressions concurrently with model timing.

Required: correct existing header suite; one separate behavioral mutation per
contract; detecting test/assertion with actual failure evidence or a stronger
assertion passing correct/failing faulty code if missed; lowercase single-value
lookup and list retrieval control on correct code and each fault; original
source/tests preserved. Reusing the same valid correct observation is permitted,
not required. A support/syntax error is not a behavioral kill. New tests are not
required for already detected faults. No external network or dependency installs.

Author [oracle recipe](httpx-headers-oracle.json), executed before scheduling:
correct suite 27 pass. Removing lookup-key lowercasing gives 1 fail / 26 pass
at the uppercase-key check (KeyError 'A', not a harness failure). Truncating
default get_list to one value gives 2 fail / 25 pass at test_headers.py:16 and
:163, preserving the observed/expected missing values. Single-value controls
pass on correct and both faulty implementations. Six actual helper phases;
correct test/control observations reused for the second fault, not independently
executed again. No timeout. This recipe/verdict stays outside model projects.

Inspect context selection and body readback, actual batch adoption/reuse (if any),
fault independence, controls, imports/caller provenance, scope, original-file
integrity, capture failures and extra work. Report total input (cached included
once) + output and whole process time against the fresh baseline. Do not count
two faults as two independent model tasks or credit hypothetical helper savings.
Unequal work, one repetition, shared caches/order and authored scope remain
limitations. No featured-chart or localized numerical claim changes.
