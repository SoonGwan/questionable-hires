import json
from pathlib import Path
from .reader import read_parts
from .writer import render

def assemble(directory):
    config = json.loads(Path('settings.json').read_text())
    return render(read_parts(directory), config['separator'])
