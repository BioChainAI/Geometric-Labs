> **Official release collection:** designated by the repository owner on 2026-10-27. [Academia publication](https://www.academia.edu/171106117/The_Geometric_Engine_of_Time_Mathematical_Architecture_of_the_6_Channel_5_Tier_Toroidal_Orbital_Calculator) · [Designation and source provenance](workflows/official-designation.md). Scientific audit and Lean status remain separate.

# The Geometric Engine of Time: Mathematical Architecture of the 6-Channel, 5-Tier Toroidal Orbital Calculator

RP-0010 · WORK-0009 · archived research reference · relevance triage on 2026-10-26.

[Unmodified source PDF](source/The_Geometric_Engine_of_Time_Mathematica.pdf) · [Search text](postprocessing/extracted-layout.txt) · [Manifest](manifest.json)

## What belongs here

Toroidal calculator model: five tier radius/winding laws, six channels, chirality, TQF anchors and caesium pulse bookkeeping. The upload filename ends Mathematica, but the artifact is a PDF, not a notebook.

## Reading and review scope

PDF pp. 2–3: intrinsic clock and tier laws; pp. 4–5: parity/kinematics and TQF; pp. 6–7: pulse closure and synthesis; p. 8: glossary.

This is architectural relevance triage of the supplied PDF, not a complete mathematical audit. Author tags and printed script logs remain source claims. Extracted text is a search aid, not an approved transcription.

## Repository placement

- **Manifold-Projection (primary):** PDF §§2–4 supplies a diagram/view model for tiers, channels and anchors.
- **Geometric-Labs (supporting):** Check winding sums, tier formulas, TQF identity and pulse arithmetic independently.
- **FractalOS-runtime (context):** Pulse model is motivation; device scheduling requires an actual clock and timing contract.
- **SHD-CCP-core (context):** Semantic labels inform a proposal; no wire-layout update follows automatically.

## Interpretation and release blockers

Separate the linear winding law Wn=16−2n from the quadratic radius law Rn=5n²+15n+15; the abstract confuses them. A chosen 60-pulse register does not prove an intrinsic physical clock or synchronization between agents. Closure at rational pulse windows is arithmetic under model assumptions; it is not measured global time. RP-0006 and RP-0011 clarify closure and calibration limits.

No official version, license clearance, release approval or independent proof status is inferred from this upload. Document date: unknown; no publication date inferred from PDF creation metadata. Revision label: unknown. Library stage remains `intake`; archive retention does not mean superseded or abandoned.

## Existing implementation references

- [src/geometric_labs/calibration/chronometry_window.py](../../../src/geometric_labs/calibration/chronometry_window.py) — related source, not evidence that every paper claim is implemented.

## Next review

Use dimensionless geometry for views; transmit explicit clock origin/uncertainty and calibration references rather than treating the diagram as a physical time source.
