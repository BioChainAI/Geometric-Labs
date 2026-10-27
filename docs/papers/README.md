# Research paper intake manifest

The initial blueprint intake below is retained for provenance. Eleven supplied PDFs are
now preserved centrally in the [Research IDE archive](../../Research_IDE/archive/README.md),
with [repository relevance](../../Research_IDE/archive/INDEX.md), stable RP IDs and hashes.
Use that library for new intake rather than duplicating files into `core/` and `series/`.
The expected-source list below is not a declaration that every named source is available.

| Tier | Expected paper / source | Governed modules | Verification pillar |
|---|---|---|---|
| 1 — core | The Fifteen Lemmas | hurwitz, tile_codec, S5, CRT, all chain/threading modules | 1–5 |
| 1 — core | Einstein Tile 64-bit RFC / Codex shapes | tile_codec, golden vectors | 3–4 |
| 1 — core | Acoustic Cubit Proposal | calibration/acoustic_cubit | 2 |
| 2 — series | Fokker–Planck Release | hurwitz, horn_frame_solver, wheel oracle, toroidal_state_matrix | 1–4 |
| 2 — series | From Linear Ledgers to Toroidal Matrices | blockchain | 4 |
| 2 — series | OpenAI 2026 source, Lemma 6.1 (title unprovided) | threading/torus_soliton_mux | 5 |

Available: [architecture blueprint](../architecture_blueprint.md),
[specification status](../specification_status.md), and
[local tile profile](../../spec_sync/einstein_tile_64bit_rfc.md).

Phase 2: inventory actual PDFs, verify sections/propositions and update module
and test docstrings; rerun `make verify-all` and `make test-pillars`. Do not label
an absent paper as reviewed or claim formal proof from an executable fixture.
