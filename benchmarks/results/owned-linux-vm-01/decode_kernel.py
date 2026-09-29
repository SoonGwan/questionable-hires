"""Decode an EFI ZBOOT gzip payload into the owned ARM64 boot image."""
from pathlib import Path
import struct
import sys
import zlib

source, target = map(Path, sys.argv[1:])
data = source.read_bytes()
assert data[4:8] == b'zimg' and data[24:29] == b'gzip\0'
offset, size = struct.unpack_from('<II', data, 8)
assert 0 < offset < len(data) and 0 < size <= len(data) - offset
raw = zlib.decompress(data[offset:offset+size], 31)
assert raw[56:60] == b'ARM\x64'
assert 0 < struct.unpack_from('<Q', raw, 16)[0] <= len(raw)
with target.open('xb') as stream:
    stream.write(raw)
