I’ll use the landlord skill to compare the validation contracts and run the requested cases against the local source with the supplied Python and `-B`. I’ll keep the review read-only and distinguish observed results from inferred proposal effects.


**Keep the existing separation.** I would reject this as behavior-preserving deduplication: it replaces distinct filename policies with metadata-name validation, changing both accepted inputs and exception types. The small line-count saving does not justify that compatibility cost.

Executed with the supplied Python and `-B`, using unmodified native parsers and default controls. Assertions confirmed `packaging`, `utils`, `version`, and `tags` loaded from this project, and both parser functions’ code paths pointed to local `packaging/utils.py`.

| Filename | Observed native result | Proposed result—inferred, not executed |
|---|---|---|
| `demo_pkg-1.0-py3-none-any.whl` | `'demo-pkg'`, `Version('1.0')` | Same |
| `demo__pkg-1.0-py3-none-any.whl` | `InvalidWheelFilename` | `'demo-pkg'`, `Version('1.0')` |
| `éclair-1.0-py3-none-any.whl` | `'éclair'`, `Version('1.0')` | `InvalidName` |
| `_demo-1.0-py3-none-any.whl` | `'-demo'`, `Version('1.0')` | `InvalidName` |
| `demo-pkg-1.0.tar.gz` | `'demo-pkg'`, `Version('1.0')` | Same |
| `demo__pkg-1.0.zip` | `'demo-pkg'`, `Version('1.0')` | Same |
| `éclair-1.0.tar.gz` | `'éclair'`, `Version('1.0')` | `InvalidName` |
| `-1.0.zip` | `InvalidSdistFilename` | Same |

Exception classes above belong to `packaging.utils`. Every successful native wheel result also returned build `()` and a frozen tag set containing `Tag('py3', 'none', 'any')`.

The decisive source differences are:

- [Wheel validation](project/packaging/utils.py#L267) rejects double underscores and uses a [Unicode-aware wheel regex](project/packaging/utils.py#L77), then normalizes separately.
- [Metadata-name validation](project/packaging/utils.py#L70) requires ASCII alphanumeric endpoints but permits repeated internal underscores. [`validate=True`](project/packaging/utils.py#L115) raises `InvalidName`; neither proposed call translates that exception into a filename-specific exception.
- [Sdist parsing](project/packaging/utils.py#L351) checks for a separator and nonempty name, then normalizes without name validation. Retaining its empty-name guard preserves that particular failure, but adding validation rejects previously accepted nonempty names.

These are observed compatibility differences, **not evidence that accepted inputs violate a specification**. The source comments identify different policy contexts; runtime acceptance alone cannot settle specification conformance.

A viable alternative is to retain both parser-specific checks and their existing calls to `canonicalize_name(name_part)`. Normalization is already shared. Merely wrapping `InvalidName` would repair exception categorization, but would not restore the accepted-input sets.

For a concrete hypothetical future policy change, suppose metadata names must prohibit consecutive underscores. With the existing separation, that policy belongs in `canonicalize_name(..., validate=True)`; the [metadata consumer](project/packaging/metadata.py#L628) already translates `InvalidName`. Wheel parsing continues rejecting `demo__pkg` with `InvalidWheelFilename`, while sdist parsing continues returning `'demo-pkg'`. Under the proposal, both parsers inherit the metadata change: wheels switch from the proposal’s newly accepted input to `InvalidName`, and sdists lose existing acceptance. That coupling makes an independent metadata policy change a filename API change.

Downstream, [pylock’s wheel and sdist validation](project/packaging/pylock.py#L613) wraps parser exceptions broadly, preserving its outer error category while inheriting acceptance changes and different causes.

No upstream tests or historical comparison ran; this snapshot supplies neither. No files, modes, Git HEAD/index, or skill resources were changed, and no scratch files were created.
