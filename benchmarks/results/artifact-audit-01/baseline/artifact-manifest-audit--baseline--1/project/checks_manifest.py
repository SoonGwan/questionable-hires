import json
from manifest import write_manifest

def test_manifest(destination, artifacts):
    assert write_manifest(destination, artifacts) == len(artifacts)
    assert destination.is_file()
    assert json.loads(destination.read_text(encoding="utf-8")) == artifacts

def test_empty(destination):
    assert write_manifest(destination, []) == 0
    assert json.loads(destination.read_text(encoding="utf-8")) == []
