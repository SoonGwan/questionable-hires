import builtins
import json
from pathlib import Path

builtins.MANIFEST_DELIMITER = json.loads(Path(__file__).with_name('format.json').read_text())['delimiter']
