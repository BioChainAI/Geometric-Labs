# Research paper intake manifest

No PDFs have been supplied. Names below are descriptive titles mentioned in the
blueprint, not fabricated filenames or verified section citations. Place the
actual PDFs in `core/` and `series/`; then reconcile exact links and citations.

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
