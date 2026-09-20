from pathlib import Path
import os
import tempfile
import pytest

def pytest_configure(config):
    os.environ["QH_ARTIFACT_FORMAT"] = "json"

@pytest.fixture
def destination():
    with tempfile.TemporaryDirectory(prefix=".manifest-test-", dir=Path(__file__).resolve().parent) as scratch:
        yield Path(scratch) / "manifest.json"

@pytest.fixture(params=[
    [{"name": "release.zip", "sha256": "a" * 64}],
    [{"name": "한글.zip", "sha256": "b" * 64}, {"name": "한글.zip", "sha256": "c" * 64}],
])
def artifacts(request):
    return request.param
