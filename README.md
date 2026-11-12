# Make the cutest picture — "Mochi the kitten"

Entry for the make.fun bounty **"Make the cutest picture"**
(https://make.fun/bounty/cutest-picture-01) — $250 prize pool, 20 places,
closes Friday 13 Nov 2026 10:00 UTC (17:00 WIB).

## What it draws

A big-eyed cream kitten ("Mochi") sitting in a flower meadow under a soft
pastel sky: huge glossy eyes with sparkle highlights, pink nose and blush,
whiskers, a pink bow on one ear, a curled tail with an orange tip, a
butterfly, a ball of pink yarn, floating hearts and paw prints, sunshine
and clouds.

## How to run

```sh
python3 main.py            # writes /output/entry.png
ENTRY_PATH=./entry.png python3 main.py   # write somewhere else (testing)
```

- **Language/runtime:** Python 3.13, **stdlib only** — the PNG encoder is
  hand-written (zlib + a small RGB rasterizer), so the program runs in any
  bare Python 3.13 sandbox with no third-party packages and no network.
- **Output:** `/output/entry.png`, 1024×1024 px, RGB PNG.
- **Determinism:** fixed seed (`SEED = 20261114`), no network, no wall
  clock, no timestamps in the PNG. Two runs produce byte-identical output
  (verified: same SHA-256 on repeated runs, see BUILD_LOG.md).

## Files

- `main.py` — the entry program (repo root, as the brief requires)
- `entry.png` — the generated output (180,150 bytes, under the 1 MiB limit)
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
