"""Compile-only prerequisite observations; no project import or issue grading."""
import json
import shutil
import sys
import warnings


def main():
    sources = {
        "literal_guard": "if 1 is None:\n    pass\n",
        "variable_guard": "value = 1\nif value is None:\n    pass\n",
        "invalid_control": "if :\n    pass\n",
    }
    rows = []
    for label, source in sources.items():
        for policy in ("default", "error"):
            row = {"source": label, "policy": policy}
            with warnings.catch_warnings(record=True) as captured:
                warnings.resetwarnings()
                warnings.simplefilter(policy, SyntaxWarning)
                try:
                    compile(source, "<authored-guard>", "exec")
                except Exception as error:
                    row.update(outcome=type(error).__name__, message=str(error))
                else:
                    row["outcome"] = "compiled"
                row["warnings"] = [
                    {"category": type(w.message).__name__, "message": str(w.message)}
                    for w in captured
                ]
            rows.append(row)
    print(json.dumps({
        "version": sys.version, "executable": sys.executable,
        "git": shutil.which("git"), "conda": shutil.which("conda"),
        "observations": rows,
    }, indent=2))


if __name__ == "__main__":
    main()
