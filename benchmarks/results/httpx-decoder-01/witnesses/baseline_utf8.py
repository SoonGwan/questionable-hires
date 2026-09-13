import pytest
import httpx

CASES = [
    pytest.param((b"prefix:\xe2", b"\x82"), ["prefix:", "\ufffd"], id="incomplete-at-eof"),
    pytest.param((b"prefix:\xe2", b"\x82\xac"), ["prefix:", "\u20ac"], id="valid-split-control"),
]

@pytest.mark.parametrize("chunks,expected", CASES)
def test_utf8_stream_finalization(chunks, expected):
    response = httpx.Response(200, content=iter(chunks))
    assert response.encoding == "utf-8"
    assert not hasattr(response, "_content")
    assert list(response.iter_text()) == expected

@pytest.mark.anyio
@pytest.mark.parametrize("chunks,expected", CASES)
async def test_utf8_async_stream_finalization(chunks, expected):
    async def stream():
        for chunk in chunks:
            yield chunk
    response = httpx.Response(200, content=stream())
    assert response.encoding == "utf-8"
    assert not hasattr(response, "_content")
    assert [part async for part in response.aiter_text()] == expected
