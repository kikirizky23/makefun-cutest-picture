# Mochi in a Strawberry Basket — version 4

A program entry for the make.fun bounty **"Make the cutest picture"**
(cutest-picture-01).

## What the picture shows

A fluffy baby kitten in an oversized pastel pink bunny hoodie, sitting
inside a tiny strawberry-shaped basket and hugging a miniature yellow
plush duck with its tiny paws. The kitten has huge sparkling eyes, a
tiny pink nose, chubby cheeks, and a little tongue sticking out.
Around it float pastel pink hearts, tiny strawberries, soft flowers,
and magical sparkles, on a dreamy pastel pink and cream background
with warm golden sunlight.

The image was generated from the user's own prompt with an image
model. It is bundled with the entry as `entry.png`.

## How the program works

This entry follows the competition kit's own starter pattern: the
simplest entry is a repository holding the image and a one-line
program that copies it to the output directory. `main.py` does exactly
that — it locates `entry.png` next to itself and copies it byte-for-byte
to `<output_dir>/entry.png`, then prints the SHA-256 and size of the
copied file so the copy can be checked.

- The output directory comes from the `MAKEFUN_OUTPUT_DIR` environment
  variable and defaults to `/output` (the grader's writable directory;
  the repository itself is read-only in the grading container).
- Python 3.13, standard library only (`hashlib`, `os`, `shutil`,
  `pathlib`). No network access, no third-party packages, fully
  deterministic: every run produces the identical bytes.

## How to run it

```sh
python3 main.py
# or, outside the grader's container:
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Output

- `entry.png` — 683×1024, JPEG bytes, 171,344 bytes (under the 1 MiB
  limit), SHA-256
  `a65c9be0000d85bbea7248e1465aad54b5efe1048096799c85d140bad5844cdc`.

## License

MIT — see `LICENSE`.
