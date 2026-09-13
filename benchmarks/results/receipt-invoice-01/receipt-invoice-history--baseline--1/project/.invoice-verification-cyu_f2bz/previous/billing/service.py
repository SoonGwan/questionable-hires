import json
from pathlib import Path
from .money import total

def invoice(lines):
    settings = json.loads(Path('config/company.json').read_text())
    return {'currency': settings['currency'], 'total': total(lines, settings['quantum'])}
