"""Write /output/entry.png from the pre-rendered entry.png (stdlib only, no network).

entry.png is produced by make_image.py (needs Pillow); this script only copies it,
so two runs give byte-identical output.
"""
import shutil
import struct
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
DST = Path("/output/entry.png")


def check(data):
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", data[16:24])
    assert w <= 1024 and h <= 1024, f"too large: {w}x{h}"
    assert len(data) <= 1024 * 1024, f"over 1 MiB: {len(data)} bytes"


def main():
    check(SRC.read_bytes())
    DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DST)
    print(f"wrote {DST}")


if __name__ == "__main__":
    main()
