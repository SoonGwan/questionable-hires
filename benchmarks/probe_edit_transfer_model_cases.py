"""Model requests for the frozen native existing-test improvement workload."""
import json
from pathlib import Path
import probe_edit_transfer_cases as fixture

ROOT = Path(__file__).resolve().parents[1]
TASK = '''Review the existing TestSpecifier.test_specifiers_valid constructor smoke
test in tests/test_specifiers.py. Determine whether this selected test detects
the specified independent defect in Specifier.__str__. This is not a claim about
the full upstream test suite: later tests may already protect string behavior.

Run the existing selected test on correct and faulty code in fresh project-local
disposable copies. If it survives, strengthen that existing method so each supplied
specifier must construct successfully and have exactly the supplied string
representation. Keep the original parameterization/imports and all other file
contents unchanged. Verify the same proposed test on correct and faulty code.
Do not leave the proposed edit or defect applied in this project.

Use the supplied preinstalled Python with -B and native pytest (or its native API)
with exactly this selector/options in every requested phase:
tests/test_specifiers.py::TestSpecifier::test_specifiers_valid -q --tb=short -p no:cacheprovider
Copy-local src must be on the import path. Verify packaging, packaging.specifiers
and tests.test_specifiers resolve inside the actual copy and the native test's
Specifier binding is that implementation in each executing pytest process.
An independent import process is not proof of what pytest loaded. There is an
installed packaging distribution in the environment which is not under review.

Report actual phase counts, exits and assertion values, including survival or
unknowns. A setup/collection error is not defect detection. Reuse valid observations
only when their inputs/environment still match; label any reuse and count actual
executions rather than comparisons. A failure in one phase must not be represented
as a successful comparison or a reason to discard earlier evidence.

Preserve all supplied source/tests/licenses, bytes/modes, Git HEAD/index and skill
resources. Remove owned scratch even on failure; leave no permanent harness/report.
No installation, network, external-project discovery, Git changes, publication or
production repair. The given interpreter and installed dependencies may be used.
Use whichever valid workflow meets the request; no particular helper is required.
'''


def cases(python):
    python = Path(python)
    if not python.is_absolute():
        raise ValueError('Use an absolute preinstalled interpreter')
    variants, fault, _ = fixture.inputs()
    return [dict(id='probe-edit-' + label, skill='con-artist', files=dict(files),
        task=TASK + '\nSource form: ' + ('full original upstream test file' if label == 'full'
            else 'exact upstream prefix through the selected first method; later tests omitted')
            + '\nSpecified fault (only this replacement):\n' + json.dumps(fault,indent=2)
            + '\nPreinstalled Python: ' + str(python),
        criteria=[
            'Actual native pytest uses supplied package/test paths and same-process Specifier binding.',
            'Correct original selected cases pass; independent faulty original cases are executed and survival/detection is accurately reported.',
            'If needed, same-path strengthening preserves parameters and unrelated bytes and passes correct code while rejecting the specified fault for the requested string behavior.',
            'Counts/exits/assertions and any reuse are supported by original execution evidence, not inferred from CLI completion.',
            'Original source/modes/Git/resources preserved; owned scratch removed and project-only scope retained.'
        ]) for label,files in variants.items()]
