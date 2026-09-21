I’m using the landlord skill to compare the validation contracts and run the requested probes against the local source, without changing any files.

**Keep the existing separation; reject this as behavior-preserving deduplication.** Normalization is already shared. The proposal merges different validation policies and changes accepted inputs and exception types.

Executed all eight probes with the supplied Python using `-B`, without patches or disabled checks. Assertions confirmed `packaging`, `utils`, `version`, and `tags` loaded from this project’s `packaging/` directory, not site-packages.

The current results below were **observed**. Proposal outcomes are **static inferences**, not executed results. Exception classes belong to `packaging.utils`; successful versions are `Version('1.0')`.

| Filename | Observed current result: name, version or exception | Proposed result, inferred |
|---|---|---|
| `demo_pkg-1.0-py3-none-any.whl` | `'demo-pkg'`, `Version('1.0')` | Unchanged |
| `demo__pkg-1.0-py3-none-any.whl` | `InvalidWheelFilename` | `'demo-pkg'`, `Version('1.0')` |
| `éclair-1.0-py3-none-any.whl` | `'éclair'`, `Version('1.0')` | `InvalidName` |
| `_demo-1.0-py3-none-any.whl` | `'-demo'`, `Version('1.0')` | `InvalidName` |
| `demo-pkg-1.0.tar.gz` | `'demo-pkg'`, `Version('1.0')` | Unchanged |
| `demo__pkg-1.0.zip` | `'demo-pkg'`, `Version('1.0')` | Unchanged |
| `éclair-1.0.tar.gz` | `'éclair'`, `Version('1.0')` | `InvalidName` |
| `-1.0.zip` | `InvalidSdistFilename` | Unchanged |

Every successful wheel probe also returned build `()` and a frozenset containing `Tag('py3', 'none', 'any')`.

The decisive source differences are:

- [Wheel validation](project/packaging/utils.py#L267) rejects `__` and uses a Unicode-aware escaped-name regex defined at [line 79](project/packaging/utils.py#L79). It raises `InvalidWheelFilename`.
- [Canonical validation](project/packaging/utils.py#L70) applies the separately identified Core Metadata name policy: ASCII alphanumeric endpoints, with repeated internal underscores allowed. Failure raises [InvalidName](project/packaging/utils.py#L115).
- [Sdist parsing](project/packaging/utils.py#L351) checks the separator and empty name, then normalizes without validating name syntax. The proposal adds a new rejection boundary while retaining the empty-name exception.

Thus the proposal both loosens wheel acceptance (`demo__pkg`) and tightens other acceptance (`éclair`, `_demo`). It also introduces `InvalidName` into parser failures. These exception classes are sibling `ValueError` subclasses, so catching `InvalidWheelFilename` or `InvalidSdistFilename` will not catch `InvalidName`. Existing malformed wheel names rejected by both policies would likewise change exception class.

These are compatibility observations, not proof that accepted filenames satisfy or violate an external specification.

The viable alternative is the current implementation: share `canonicalize_name` for normalization and keep format-specific validation at each parser boundary. Its maintenance cost is a small explicit guard; a configurable shared validator would add machinery without eliminating the distinct policies. Simply translating `InvalidName` into parser exceptions would still leave acceptance changes.

For a concrete future policy change, suppose wheel parsing intentionally starts allowing repeated underscores. With the current separation, remove only the wheel’s `__` rejection: wheel `demo__pkg` starts returning `'demo-pkg'`; sdist `demo__pkg` continues returning `'demo-pkg'` unchanged. Other wheel validation and parser exception contracts survive. Routing both through the metadata validator achieves that wheel change only while bundling unrelated restrictions into both consumers.

There are actual downstream consumers: [pylock](project/packaging/pylock.py#L613) parses both formats and wraps exceptions, but changed acceptance still affects its validation path. [Metadata](project/packaging/metadata.py#L628) already uses `validate=True` and explicitly translates `InvalidName`, reinforcing that this validation policy has its own consumers.

No upstream tests or historical revision were supplied or run. Workspace file hashes and modes were unchanged across execution, including Git metadata and skill resources; HEAD/status remained unchanged. No scratch files were created.
