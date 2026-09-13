import httpx
import pytest

CASES = [
    pytest.param([b"prefix ", b"\xe2", b"\x82"], "prefix \ufffd", id="incomplete-at-eof"),
    pytest.param([b"prefix ", b"\xe2", b"\x82", b"\xac"], "prefix \u20ac", id="valid-split-control"),
]

@pytest.mark.parametrize("chunks, expected", CASES)
def test_utf8_eof_sync(chunks, expected):
    response = httpx.Response(200, content=iter(chunks))
    response.encoding = "utf-8"
    assert "".join(response.iter_text()) == expected

@pytest.mark.anyio
@pytest.mark.parametrize("chunks, expected", CASES)
async def test_utf8_eof_async(chunks, expected):
    async def stream():
        for chunk in chunks:
            yield chunk
    response = httpx.Response(200, content=stream())
    response.encoding = "utf-8"
    assert "".join([part async for part in response.aiter_text()]) == expected
