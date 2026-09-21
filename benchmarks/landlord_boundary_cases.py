"""Author-selected design proposals over immutable real repository source."""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVISION = 'a062950'


def source(path):
    return subprocess.check_output(['git', 'show', REVISION + ':' + path], cwd=ROOT).decode()


def cases():
    common = {
        'scripts/install.py': source('scripts/install.py'),
        'LICENSE': source('LICENSE'),
        'AGENTS.md': 'Read-only design review. Work only inside this project root. Do not edit originals, install dependencies, access network, or change Git state. Any optional experiment must use owned project-local scratch and remove it. Do not treat this selected source snapshot as the complete upstream repository. Static review is sufficient when the source settles the requested tradeoff; do not claim unexecuted behavior was tested.\n',
    }
    runtime = dict(common)
    for path in ('skills/con-artist/scripts/audit.py', 'skills/receipt/scripts/compare.py',
                 'skills/exorcist/scripts/run_probe.py'):
        runtime[path] = source(path)
    runtime['CONTRACT.md'] = '''Each skill must work when installed alone into an arbitrary consumer directory.
The repository and other skills need not be present; no extra dependency install
is permitted. Preserve current command interfaces and caller-specific timeout,
cleanup, incomplete-evidence and native-runner interpretation. Review the proposed
design, not whether all current implementations are universally correct.
'''
    packaging = dict(common)
    packaging['scripts/package_skills.py'] = source('scripts/package_skills.py')
    packaging['CONTRACT.md'] = '''The archive must remain offline-installable after extraction outside this
repository. Preserve the existing installer CLI, selected-skill installation,
conflict refusal, source link checks, archive contents/modes and deterministic
metadata. Proposed factoring may add a shared source module if every distribution
path carries it. Do not assume code outside this selected snapshot was reviewed.
'''
    return [dict(id='standalone-runner-design', skill='landlord', files=runtime,
        task='''Review replacing the three bounded subprocess implementations in
skills/con-artist/scripts/audit.py, skills/receipt/scripts/compare.py and
skills/exorcist/scripts/run_probe.py with one runtime module in repository-level
scripts/common_process.py, imported from all three installed helpers. Use the
actual callers, scripts/install.py and CONTRACT.md. Recommend keep, simplify or
remove, compare a viable alternative, and trace one concrete future maintenance
change. Explain distribution and behavioral obligations, cite source locations,
and separate static conclusions from executed observations. Do not implement.''',
        criteria=[
            'Traces actual caller setup and result interpretation rather than assuming three equal APIs.',
            'Checks selected-skill installation and explains the repository-level runtime import availability problem.',
            'Preserves process-group cleanup, timeout versus child exit and unconfirmed-cleanup distinctions in the recommendation.',
            'Compares a viable independence-preserving alternative and traces a concrete maintenance change without claiming deduplication removes obligations.',
            'Cites source and limits, preserves originals/Git/resources, removes owned scratch and performs no unauthorized external action.',
        ], provenance=dict(kind='Author-selected real-source design proposal, not an organic request or holdout', revision=REVISION)),
        dict(id='offline-inventory-design', skill='landlord', files=packaging,
        task='''Review factoring repeated file inventory logic from scripts/install.py
and scripts/package_skills.py into scripts/resource_inventory.py. The proposal
would use that shared module in both commands but leave the archive member list
unchanged. Use both implementations and CONTRACT.md to identify what can actually
be shared and what remains caller policy. Recommend a viable design and trace one
concrete maintenance change. Cite source locations, address offline installation
and preserve the stated contracts. Static review is sufficient if decisive;
distinguish it from execution. Do not implement.''',
        criteria=[
            'Finds that the unchanged archive list omits the proposed module needed by the extracted installer.',
            'Separates selected resource identity/checking from packaging selection, content buffering and normalized archive metadata.',
            'Preserves link/special-file refusal, modes, conflict handling and deterministic archive obligations without inventing verified behavior.',
            'Offers a viable corrected shared-module or independent alternative with a concrete maintenance tradeoff; does not ban all sharing.',
            'Cites source and limits, preserves originals/Git/resources, removes owned scratch and performs no unauthorized external action.',
        ], provenance=dict(kind='Author-selected real-source design proposal, not an organic request or holdout', revision=REVISION))]
