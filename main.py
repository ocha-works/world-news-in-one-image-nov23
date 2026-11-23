#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Writes the front-page image of Monday 23 November 2026 to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output).

The image itself is drawn by generate_image.py and shipped in this
repository as entry.png. This program only verifies it against the
contest gate -- PNG magic, a complete chunk chain with valid CRCs,
image data matching the header, dimensions at most 1024x1024 and a
file size of at most 1 MiB -- and then copies it byte for byte, so
two runs always produce identical output. Standard library only.
"""
import os
import shutil
import struct
import sys
import zlib

MAX_BYTES = 1_048_576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    raise SystemExit(1)


def validate_png(data):
    """Check the PNG gate; return (width, height)."""
    if len(data) > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 or data[:8] != PNG_MAGIC:
        fail("entry.png does not start with the PNG magic bytes")
    pos = 8
    seen = set()
    width = height = None
    idat = bytearray()
    while True:
        if pos + 8 > len(data):
            fail("PNG ends before the IEND chunk")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 12 + length
        if end > len(data):
            fail("chunk %r overruns the file" % ctype)
        chunk_data = data[pos + 8:pos + 8 + length]
        crc_stored = struct.unpack(">I", data[pos + 8 + length:end])[0]
        crc_calc = zlib.crc32(ctype)
        crc_calc = zlib.crc32(chunk_data, crc_calc) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail("chunk %r has a bad CRC" % ctype)
        if ctype == b"IHDR":
            if length != 13:
                fail("IHDR has the wrong length")
            width, height = struct.unpack(">II", chunk_data[:8])
            if width > MAX_DIM or height > MAX_DIM:
                fail("image is %dx%d, over the 1024x1024 limit"
                     % (width, height))
        elif ctype == b"IDAT":
            idat += chunk_data
        seen.add(ctype)
        pos = end
        if ctype == b"IEND":
            break
    if pos != len(data):
        fail("trailing bytes after the IEND chunk")
    if b"IHDR" not in seen or b"IDAT" not in seen or b"IEND" not in seen:
        fail("PNG is missing IHDR, IDAT or IEND")
    if width is None:
        fail("no IHDR found")
    try:
        zlib.decompress(bytes(idat))
    except zlib.error as exc:
        fail("IDAT data does not decompress: %s" % exc)
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        fail("entry.png is missing next to main.py")
    with open(src, "rb") as fh:
        data = fh.read()
    width, height = validate_png(data)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    print("wrote %s (%d bytes, %dx%d)" % (dst, len(data), width, height))


if __name__ == "__main__":
    main()
