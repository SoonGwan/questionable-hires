import pytest
import httpx

CASES = [
    pytest.param((b"prefix \xe2", b"\x82"), ["prefix ", "\ufffd"], id="incomplete-at-eof"),
    pytest.param((b"prefix \xe2", b"\x82", b"\xac"), ["prefix ", "\u20ac"], id="valid-split-control"),
]

@pytest.mark.parametrize("data, expected", CASES)
def test_utf8_stream_finalization(data, expected):
    response = httpx.Response(200, content=iter(data),
                              headers={"Content-Type": "text/plain; charset=utf-8"})
    assert not response.is_stream_consumed
    assert list(response.iter_text()) == expected

@pytest.mark.anyio
@pytest.mark.parametrize("data, expected", CASES)
async def test_utf8_async_stream_finalization(data, expected):
    async def chunks():
        for chunk in data:
            yield chunk
    response = httpx.Response(200, content=chunks(),
                              headers={"Content-Type": "text/plain; charset=utf-8"})
    assert not response.is_stream_consumed
    assert [part async for part in response.aiter_text()] == expected
