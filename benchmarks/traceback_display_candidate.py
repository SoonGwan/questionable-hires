"""Unadopted optional Hostage display routing, derived from d3e7d5b6."""


def entry(text):
    old = ('When terminal capture is unreliable and local evidence files are permitted, use the '
           '[single-run native capture fallback](references/native-evidence.md); read retained '
           'results instead of rerunning solely for output.')
    new = ('When repeated Python tracebacks are expected, or terminal capture is unreliable, '
           'use [single-run retained native output](references/native-evidence.md) if local '
           'evidence is permitted. It keeps full raw output and the native exit while displaying '
           'identical repeated frames by reference. Prefer direct output for small checks; '
           'do not rerun tests solely for a different display.')
    if text.count(old) != 1:
        raise ValueError('Expected the frozen Hostage capture route')
    return text.replace(old, new)


def guide(text):
    old = ('# Retain one native check when terminal capture is unreliable\n\n'
           'Prefer an existing native report tied to the current command and inputs. Use this\n'
           'fallback only when output has been lost or capture is known to be unreliable,\n'
           'and project-local evidence files are permitted. It does not recover past output.\n'
           'Do not rerun side-effectful work to obtain a nicer transcript.')
    new = ('# Retain native output; fold identical traceback prefixes\n\n'
           'Use for expected repeated Python tracebacks or unreliable capture when local\n'
           'evidence is permitted. Prefer a report already tied to current inputs; never\n'
           'rerun solely for display. The renderer reads a completed raw file, preserves\n'
           'all distinct frames, test identities, failure values and summaries, and uses\n'
           'original line references only for exact repeated prefixes. Read the raw file\n'
           'for unresolved details. Passing/unknown output stays unchanged; it never grows\n'
           'the display. This is not test execution, grading or past-output recovery.')
    command = '  cat "$evidence_dir/output.txt"'
    replacement = ('  # Resolve <skill-dir> to this installed skill directory.\n'
                   '  python3 -B <skill-dir>/scripts/fold_tracebacks.py "$evidence_dir/output.txt" ||\n'
                   '    cat "$evidence_dir/output.txt"')
    if text.count(old) != 1 or text.count(command) != 1:
        raise ValueError('Expected the frozen native capture recipe')
    return text.replace(old, new).replace(command, replacement) + (
        '\nRenderer exit0 means display succeeded, not that tests passed. The subshell\n'
        'still returns the captured native exit. Inputs over1 MiB error and the recipe\n'
        'falls back to raw output. Keep the raw file through inspection; honor required\n'
        'cleanup of owned evidence afterward. No extra test harness is introduced.\n')
