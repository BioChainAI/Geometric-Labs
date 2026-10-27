# Memory in the Twelve-Engine Hierarchy

RP-0007 · WORK-0007 · archived research reference · relevance triage on 2026-10-26.

[Unmodified source PDF](source/Memory%20in%20the%20Twelve-Engine%20Hierarchy.pdf) · [Search text](postprocessing/extracted-layout.txt) · [Manifest](manifest.json)

## What belongs here

Three results: ordered implied-fourth parity, inverse tier offload, and a phase-channel decomposition. Explicitly limits erasure recovery and storage capacity.

## Reading and review scope

PDF pp. 1–3: summary, assumptions and M1 parity; p. 4: M2 tier inverse and fixed-width claim; pp. 5–6: counts and M3 phases; pp. 7–8: verification log and limits.

This is architectural relevance triage of the supplied PDF, not a complete mathematical audit. Author tags and printed script logs remain source claims. Extracted text is a search aid, not an approved transcription.

## Repository placement

- **CubiLoom (primary):** M1 and M2 motivate erasure/replay storage, with 25% parity overhead and explicit failure boundaries.
- **PolyShard-Agent (supporting):** Retain private local histories; exporting parity alone cannot reconstruct all individual events.
- **Polycentric-Orchestrator (supporting):** Coordinate missing-engine recovery without inventing independent history from one parity product.
- **FractalOS-runtime (supporting):** M3 phase/stream scheduling requires explicit time-slot semantics and measured capacity.
- **Geometric-Labs (supporting):** Exact parity/inverse tests and counterexample to M2 fixed-coordinate-width inference.

## Interpretation and release blockers

One loss per four-engine group is recoverable under the ordering model; two in a group are not generally recoverable. A parity product does not store separate histories. Norm preservation in M2 does not imply equal per-coordinate bit width: doubled coordinates (1,1,1,1) become (0,0,2,0) under h=(1,−1,1,1)/2. Separate time slots and phasors on one carrier have different capacities. Embedded verification logs were not rerun from the original verify_memory.py, which is absent.

No official version, license clearance, release approval or independent proof status is inferred from this upload. Document date: 2026-10-16. Revision label: unknown. Library stage remains `intake`; archive retention does not mean superseded or abandoned.

## Existing implementation references

- [src/geometric_labs/threading/cubocta_12engine_ring.py](../../../src/geometric_labs/threading/cubocta_12engine_ring.py) — related source, not evidence that every paper claim is implemented.
- [docs/specification_status.md](../../../docs/specification_status.md) — related source, not evidence that every paper claim is implemented.

## Next review

Specify erasure-code event layout, word order and retained history, then exercise loss/replay cases; correct the fixed-coordinate-width claim in a reviewed revision.
