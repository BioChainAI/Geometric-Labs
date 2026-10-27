# The Hyperbolic Sparsemax Pump: A Rational, Parity-Safe Executable Kernel for the SHD–CCP Lattice

RP-0005 · WORK-0005 · archived research reference · relevance triage on 2026-10-26.

[Unmodified source PDF](source/The_Hyperbolic_Sparsemax_Pump_A_Rational.pdf) · [Search text](postprocessing/extracted-layout.txt) · [Manifest](manifest.json)

## What belongs here

Rational Lorentz lift, hyperbolic quadrance, sparsemax projection and a separate symmetric-base/reverse-valve construction on a 64-cell toroidal graph.

## Reading and review scope

PDF pp. 2–5: assumptions, Lorentz lift, quadrance and sparsemax; pp. 6–7: base walk, reverse valve and base-referenced current; pp. 8–9: synthesis and scope; p. 10: references. PDF p. 3 was inspected visually.

This is architectural relevance triage of the supplied PDF, not a complete mathematical audit. Author tags and printed script logs remain source claims. Extracted text is a search aid, not an approved transcription.

## Repository placement

- **SHD-CCP-core (primary):** PDF §§2–10: candidate exact-rational routing operator; canonical promotion requires a reviewed profile and bounded representation.
- **Geometric-Labs (supporting):** Closest mathematical source for the Fraction oracle and float AlexNet-H/GEOT router; full pump remains separate work.
- **FractalOS-runtime (supporting):** Exact fraction width/overflow and execution ABI must be specified before device parity claims.
- **Kernel-Registry (supporting):** Store operator assumptions, numeric domain and evidence separately from author theorem tags.
- **PolyShard-Agent (context):** Possible trained local feature-routing use; no production inference acceptance follows from paper triage.

## Interpretation and release blockers

The paper distinguishes sparsemax S from the full valve-modified pump K. Current code implements a bounded Fraction oracle for lift/quadrance/sparsemax and a learned floating model; it does not implement all of K or a parity-preserving end-to-end exact device kernel. Theorem 17 is a current relative to the base measure, not necessarily the stationary measure of K (Remark 22). Hyperbolic quadrance sinh²(d) is a kernel/dissimilarity, not a triangle-inequality distance. The scalar annulus excludes identity and half-turns, so it is a latent routing domain, not general pose space.

No official version, license clearance, release approval or independent proof status is inferred from this upload. Document date: 2026-06-21. Revision label: unknown. Library stage remains `intake`; archive retention does not mean superseded or abandoned.

## Existing implementation references

- [ecosystem/experiments/alexneth_geot/src/alexneth_geot/oracle.py](../../../ecosystem/experiments/alexneth_geot/src/alexneth_geot/oracle.py) — related source, not evidence that every paper claim is implemented.
- [ecosystem/experiments/alexneth_geot/src/alexneth_geot/model.py](../../../ecosystem/experiments/alexneth_geot/src/alexneth_geot/model.py) — related source, not evidence that every paper claim is implemented.

## Next review

Add a separately specified rational base/valve reference and its tests; evaluate learned temperature/support controls before training comparisons.
