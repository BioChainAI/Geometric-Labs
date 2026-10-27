> **Official release collection:** designated by the repository owner on 2026-10-27. [Academia publication](https://www.academia.edu/169060820/The_Torsional_Markov_Memory_Offload_Pump_A_Three_Scale_Quaternionic_Delta_Chain_with_Inverse_Compensation_and_Non_Equilibrium_Circulation_Owl_Academy) · [Designation and source provenance](workflows/official-designation.md). Scientific audit and Lean status remain separate.

# The Torsional Markov Memory-Offload Pump: A Three-Scale Quaternionic Delta-Chain with Inverse Compensation and Non-Equilibrium Circulation

RP-0009 · WORK-0004 · archived research reference · relevance triage on 2026-10-26.

[Unmodified source PDF](source/The_Torsional_Markov_Memory_Offload_Pump.pdf) · [Search text](postprocessing/extracted-layout.txt) · [Manifest](manifest.json)

## What belongs here

Expanded formal offload model, with block telescoping and partition results, principal-branch fractional lifts, three-state stationary current and an explicit discussion of the rational sparsemax companion.

## Reading and review scope

PDF pp. 2–5: chain conventions, telescoping, partition and fractional lift; pp. 5–6: stationary current and holonomy; pp. 7–8: schematic recursion and relation to sparsemax; pp. 8–9: scope and references.

This is architectural relevance triage of the supplied PDF, not a complete mathematical audit. Author tags and printed script logs remain source claims. Extracted text is a search aid, not an approved transcription.

## Repository placement

- **CubiLoom (primary):** PDF §§3–5 and 15 motivate ordered block history and retained residuals; storage/replay remains to be built.
- **Geometric-Labs (supporting):** Test noncommutative telescoping, partitions, branch cases and memory-loss limits.
- **FractalOS-runtime (supporting):** PDF §14 requires a declared rational/transcendental execution boundary.
- **Polycentric-Orchestrator (supporting):** PDF §7 current model may inform a future scheduling policy after K and π are specified.
- **PolyShard-Agent (context):** Potential local history compression; do not export private fine history by implication.

## Interpretation and release blockers

Exact SLERP reconstruction applies to a selected principal-branch increment, not recovery of arbitrary lost fine history or a bound on accumulated drift. §15 labels coherent global memory offload an engineering design; explicit transition K, invariant π and error bounds remain work. §14 separates exact rational forward execution from transcendental reconstruction. No declared supersession of RP-0004 is inferred from its fuller presentation.

No official version, license clearance, release approval or independent proof status is inferred from this upload. Document date: 2026-06-21. Revision label: unknown. Library stage remains `intake`; archive retention does not mean superseded or abandoned.

## Existing implementation references

- [src/geometric_labs/blockchain/holonomy_prefix_scan.py](../../../src/geometric_labs/blockchain/holonomy_prefix_scan.py) — related source, not evidence that every paper claim is implemented.
- [ecosystem/experiments/alexneth_geot/src/alexneth_geot/oracle.py](../../../ecosystem/experiments/alexneth_geot/src/alexneth_geot/oracle.py) — related source, not evidence that every paper claim is implemented.

## Next review

Retain residual fine history, pin multiplication/branch conventions and test replay; keep irrational reconstruction outside the exact forward path unless explicitly rationalized with an error contract.
