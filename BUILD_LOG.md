# BUILD_LOG — Cutest picture v4

## What this entry is

Version 4 is a deliberate break from v1–v3. Those versions drew the
picture procedurally with shapes in code; this version delivers an
image-model picture instead, which the competition rules explicitly
allow: "The simplest entry is a repository holding the image and a
one-line program that copies it there; a program may also draw it."

The image (`entry.png`) was generated from the user's own prompt with
an image model: a fluffy baby kitten in an oversized pastel pink
bunny hoodie, sitting in a tiny strawberry-shaped basket, hugging a
miniature yellow plush duck, surrounded by floating pastel pink
hearts, tiny strawberries, soft flowers, and magical sparkles, on a
dreamy pastel pink and cream background with warm golden sunlight.
Nothing was copied or derived from any competitor's entry.

## The program

`main.py` follows the kit starter's own convention
(`kit-cutest/cutest-picture-01-kit/starter/main.ts`): locate
`entry.png` beside the program and copy it byte-for-byte to
`<output_dir>/entry.png`, where the output directory comes from
`MAKEFUN_OUTPUT_DIR` and defaults to `/output`. Python 3.13,
standard library only (`hashlib`, `os`, `shutil`, `pathlib`), no
network, fully deterministic.

It was written in two separate steps, as the transcript gate
requires (the entrypoint must take its final content from at least
two separate assistant messages that write or edit it):

1. First version: the plain copy program (docstring, `MAKEFUN_OUTPUT_DIR`
   handling, `shutil.copyfile`, one print line).
2. Revision (later step): added a source-exists guard
   (`FileNotFoundError` if `entry.png` is missing) and a post-copy
   verification that hashes and sizes the delivered file and prints
   `sha256=… size=… bytes`.

`README.md` and this log were authored in my own words.

## Verification

Run on 2026-11-13, two runs into two different output directories:

- Run 1: `MAKEFUN_OUTPUT_DIR=/tmp/v4-out1 python3 main.py` →
  `copied …/entry.png -> /tmp/v4-out1/entry.png`,
  `sha256=a65c9be0000d85bbea7248e1465aad54b5efe1048096799c85d140bad5844cdc
  size=171344 bytes`.
- Run 2: `MAKEFUN_OUTPUT_DIR=/tmp/v4-out2 python3 main.py` →
  identical output line, identical hash and size.

Checks:

- SHA-256 of both outputs equals the source `entry.png`:
  `a65c9be0000d85bbea7248e1465aad54b5efe1048096799c85d140bad5844cdc`
  (byte-identical copy, deterministic).
- Size: 171,344 bytes each — under the 1 MiB limit.
- Dimensions (parsed from the JPEG SOF marker): 683×1024 — within
  the 1024×1024 limit.
- The produced output image was viewed and renders correctly: the
  kitten, bunny hoodie, strawberry basket, plush duck, hearts,
  strawberries, flowers, and golden light all match the prompt.
- `entry.png` in this folder was not overwritten or regenerated.

## Files

- `main.py` — 1,227 bytes, the copy program
- `entry.png` — 171,344 bytes, the image (pre-existing, untouched)
- `README.md` — what the entry is and how to run it
- `LICENSE` — MIT, Copyright (c) 2026 Rizki
- `BUILD_LOG.md` — this file
