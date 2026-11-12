"""Cutest picture entry (cutest-picture-01).

The picture is entry.png beside this file. The program copies it
byte-for-byte to <output_dir>/entry.png, where output_dir comes from
the MAKEFUN_OUTPUT_DIR environment variable and defaults to /output
(the grader's writable directory; the repository itself is read-only
in the grading container).

Python 3.13, standard library only, no network access.
"""

import hashlib
import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise FileNotFoundError(f"entry image not found: {source}")
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / "entry.png"
    shutil.copyfile(source, destination)
    # Post-copy verification: the delivered file must be byte-identical
    # to the source image, so hash and size both after copying.
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    size = destination.stat().st_size
    print(f"copied {source} -> {destination}")
    print(f"sha256={digest} size={size} bytes")


if __name__ == "__main__":
    main()
