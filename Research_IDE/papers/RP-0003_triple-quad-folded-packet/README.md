# Extending the Framework: Triple-Quad Function on a 3-Folded Packet

RP-0003 · WORK-0003 · archived research reference · relevance triage on 2026-10-26.

[Unmodified source PDF](source/Extending_the_Framework_Triple_Quad_Func.pdf) · [Search text](postprocessing/extracted-layout.txt) · [Manifest](manifest.json)

## What belongs here

Defines eight layers after three folds and three overlapping four-site quadratic measurements, then proposes projective/topological summaries and regularized reconstruction.

## Reading and review scope

PDF pp. 1–3: eight layers and quadratic windows (1,2,3,4), (3,4,5,6), (5,6,7,8); pp. 4–9: projective, persistent-homology and inverse-problem proposals; pp. 10–12: architectural synthesis. PDF p. 3 was inspected visually.

This is architectural relevance triage of the supplied PDF, not a complete mathematical audit. Author tags and printed script logs remain source claims. Extracted text is a search aid, not an approved transcription.

## Repository placement

- **Geometric-Labs (primary):** Direct design source for the AlexNet-H/GEOT folded-feature experiment; PDF §3 supplies its overlapping quadratic windows.
- **Manifold-Projection (supporting):** PDF §§5–6 propose projective and topological analysis of features, not measured 3D scene coordinates.
- **PolyShard-Agent (context):** Future local visual feature producer once trained, typed and purpose-bound.
- **Kernel-Registry (context):** Future operator evidence record must distinguish this Triple-Quad Function from geometric TQF.

## Interpretation and release blockers

This is not the exact triangle Gram/TQF identity in the core. The current learned FoldedTriQuad operator is an engineering realization of these overlapping windows. A fold permutation is invertible; three quadratic measurements alone are generally not (x and −x have the same homogeneous quadratic measurements). Projective invariance requires specified coefficients/normalization. Cubic index count does not establish inverse complexity or reconstruction uniqueness; TDA and inverse reconstruction are not implemented in the current model.

No official version, license clearance, release approval or independent proof status is inferred from this upload. Document date: unknown; no publication date inferred from PDF creation metadata. Revision label: unknown. Library stage remains `intake`; archive retention does not mean superseded or abandoned.

## Existing implementation references

- [ecosystem/experiments/alexneth_geot/src/alexneth_geot/model.py](../../../ecosystem/experiments/alexneth_geot/src/alexneth_geot/model.py) — related source, not evidence that every paper claim is implemented.
- [ecosystem/experiments/alexneth_geot/tests/test_geot.py](../../../ecosystem/experiments/alexneth_geot/tests/test_geot.py) — related source, not evidence that every paper claim is implemented.

## Next review

Keep the current fold inverse test and add task-specific reconstruction/data experiments with explicit measurement operators before making inverse or topology claims.
