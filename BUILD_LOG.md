# BUILD_LOG — "Mochi the kitten" (cutest-picture-01)

Bounty: https://make.fun/bounty/cutest-picture-01 — $250, 20 places,
closes Fri 13 Nov 2026 10:00 UTC (17:00 WIB). AI judge compares images
pairwise and picks the cuter one.

## Brief (as read 13 Nov 2026 ~02:07 WIB)

- Program at `main.py` (Python 3.13) in the repo root; writes
  `/output/entry.png`.
- Image: whole PNG or JPEG, at most 1 MiB and 1024×1024 px.
- No network; the program runs twice and both runs must write the same
  bytes (deterministic).
- Deliverables: public GitHub repo under an OSI-approved license (MIT used
  here) + the AI coding-agent transcripts of the sessions that built it,
  uploaded with each submission. Max 10 submissions/day, 20 total; the last
  submission before the deadline is the final entry.
- $250 USDC is locked in the bounty escrow on Solana.

## Approach

- **Stdlib only.** Same reasoning as the sister entry: the grading
  sandbox is Python 3.13 and no third-party image library is guaranteed,
  so the program uses only `math`, `os`, `random`, `struct`, `zlib`, with a
  hand-written PNG encoder (RGB, 8-bit, Up filter, zlib level 9).
- **Scene choice:** a sitting kitten in a flower meadow — the cuteness
  signals an image judge keys on: huge glossy eyes with double
  highlights, round head, pink nose + blush, whiskers, a bow, plus
  supporting cute props (butterfly, yarn ball, hearts, paw prints) and a
  soft pastel palette.
- **Composition (1024×1024):** pastel sky, sun top-left, clouds; green
  hill at the bottom (top edge ≈ y 860); kitten centred (head r=200 at
  (512, 430), body 205×185 at (512, 800)); tail curling on the right with
  an orange tip; flowers and grass on the hill.
- **Determinism:** one fixed seed (`SEED = 20261114`), `random.Random`
  instance only; no `hash()`, no time, no timestamps in the PNG.

## Build steps

1. Read both bounty briefs + `make.fun/skill.md` (13 Nov ~02:07 WIB).
   Confirmed main.py / Python 3.13, `/output/entry.png`, 1 MiB /
   1024×1024 limits, determinism rule.
2. Wrote `main.py` and ran it (first version had a leftover no-op line
   and a head patch poking outside the head disc; both fixed before the
   first visual check).
3. Visual check v1: face was already adorable, but (a) the body was
   nearly invisible — cream on cream, (b) the tail read as a floating
   capsule, (c) the ears read as party hats (too tall/narrow),
   (d) the butterfly was a blurry blob, (e) the hill was too pale.
4. Iteration v2: deeper green hill raised to y≈860; shorter/wider ears;
   a proper curl tail from control points; bow moved onto the ear;
   smaller butterfly wings. Visual check v2: better, but the body was
   still washed out and the tail tip was a fat orange blob.
5. Iteration v3: warm body fill (255, 236, 210) + strong dark-tan outline
   (196, 138, 92) + soft halo behind the body; outlined tail (outline
   pass + fill pass) with a smaller tapered orange tip; stronger paw/foot
   outlines; butterfly wings separated with saturated colours.
   Visual check v3: accepted — the sitting-kitten silhouette reads
   clearly (head, body, curled tail, paws, feet), the face is the focal
   point, and the props frame it.

## Test results (final, 13 Nov 2026 ~02:12 WIB)

- Runtime: ~2.8 s per run (local Python 3.12.3; target is Python 3.13).
- Determinism: ran twice with `ENTRY_PATH` set, then once with the
  default `/output/entry.png` path — all three outputs byte-identical.
  SHA-256: `65554211130ab13b1837e27a19f83eae44ca9a2461af82059374bcbe711d5360`
- PNG validity: header + IHDR parse OK (1024×1024, 8-bit, colour type 2
  RGB).
- Size: **180,150 bytes** — well under the 1,048,576-byte limit.
- Dimensions: 1024×1024 — at the limit, allowed.
- Visual check: viewed the rendered PNG — subject clearly visible,
  not blank, not broken; the kitten face (eyes, nose, blush, whiskers,
  bow) is the clear focal point.

## Submission notes (for the parent agent, not done by this build)

- Nothing was submitted to make.fun and no GitHub repo was created.
- To submit: create a public GitHub repo (owner: Rizki's account) with
  `main.py` + `README.md` + `LICENSE` at its root, then submit it with
  the AI-agent transcripts of the sessions that built it (this build's
  transcript lives in the parent agent's conversation).
- The program writes `/output/entry.png` by default; `ENTRY_PATH` only
  exists for local testing and does not affect the output bytes.
