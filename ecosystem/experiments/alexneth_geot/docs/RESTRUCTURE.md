# RFC 0.2 restructuring decisions

## Implemented data path

| Stage | Actual default contract |
|---|---|
| Input | finite B×3×224×224 float tensor, synthetic in validation |
| Stem | five AlexNet convolutions; taps B×192×27×27, B×384×13×13, B×256×13×13 |
| Align | project each tap to 16 channels; bilinear 16×16 alignment; merge to B×16×16×16 |
| Fold | H–W–H permutation to B×128×4×8; reversible only for this selected tensor |
| FoldedTriQuad | learned symmetric four-fiber quadratic energies over windows 0123, 2345, 4567; initialized I/4 |
| Cubic assembly | concatenate folded/energy features, project D=64, learned 32→64 spatial map |
| Grid | periodic (Z/4Z)^3, x fastest, self plus six face neighbors per cell |
| State | bounded unit q=(w,m), .25<w<.9, normalized vector with declared zero fallback |
| Route | Lorentz lift, Qh=sinh²(distance), beta=(1-w)/w, sparsemax(-beta*cost), residual value mixing |
| Control | same parameters, graph and shapes; squared spinor chordal cost instead of Lorentz Qh |
| Heads | class logits; separate fixed-c=1 64D Poincare embedding with interior margin 1e-5 |
| Export | typed approximate descriptor sidecar, model/source digests and consent, no new Tile form |

The learned spatial projection is not invertible and does not recover physical
depth. FoldedTriQuad coefficients are an explicit engineering proposal because
the source paper's complete operator specification was not supplied. The three
quadrance APIs remain distinct: TriangleTQF, FoldedTriQuad and hyperbolic Qh.
The Lorentz H3 state is not a replacement for the 64D semantic embedding.

Routing evaluates 64×7 local candidates, not a dense 64×64 matrix. Zero sparsemax
weights do not automatically skip value work on this implementation. Support,
self-loop mass and self-only fraction are monitored; no speedup or learned
anti-collapse result is claimed. Directed valve A_ij is zero for this first lane.

## Numeric/reference boundaries

Torch geometry rejects nonfinite/non-unit inputs; sparsemax translates logits
for numerical stability. Rational oracle accepts only Fraction/integer inputs,
checks annular/unit constraints, and bounds numerator/denominator sizes on
inputs, outputs and selected intermediates. Python arbitrary precision is used;
this is not a fixed-width accelerator or a quantized learned-state implementation.

The semantic exp-map uses its analytic zero limit, including a nonzero derivative
at the origin. A regression checks that gradient and strict interior behavior.
No float tensor is silently converted to an exact Hurwitz or rational state.

Original RFC and six supplied tests/primitives are archived verbatim in research/.
Adapted runtime primitives live separately under src/. Existing core geometry,
ordering conventions, protocol fields and golden vectors are unchanged.

## Corpus limits

The RFC reports a 13-document review. This turn supplies nine PDFs; the four-file
ZIP contains the RFC and prototype, not the additional original source papers.
Golden Toroid, folded-packet, Sparsemax Pump and QCC papers referenced in the RFC
are not independently available as those source PDFs. Their RFC formulas are
proposed contracts, not independently verified proofs in this task.

Selected searchable passages were inspected; image-only PDFs cannot be fully
reviewed through text extraction. Representative chronometry page 1 renders blank
apart from export furniture. No statement that all 19 pages were visually
reviewed is made. The visually inspected sumption page's universal O(1) GPU and
CPU-bypass claims are not adopted. The image-only Fifteen Lemmas remains bounded
by already verified code/fixtures. See source-inventory.json for file hashes.

## Wave and ownership status

| RFC wave | Current evidence | Remaining |
|---|---|---|
| A | source inventory and profile separation | original trained v0.1 baseline absent |
| B | multiscale stem, reversible folding and gradients | trained spatial-detail ablation |
| C | actual matched Euclidean/Lorentz routers and backward pass | multi-seed accuracy/resource comparison |
| D | rational oracle plus existing C/Python wire gates | learned-state quantization and fixed-width kernel |
| E | original ordered-product reference tests preserved | video data, temporal training, residual/keyframe codec |
| F | real agent/control sidecar transport | remote schema/purpose enforcement and CubiLoom persistence |
| G | no hardware claim | parity/torus/phase experiments and accelerated implementations |

Keep experimental integration here for review. Stable vision operators may move
to Manifold-Projection after evaluation; shared codecs belong to SHD-CCP-core;
agent/privacy and control validation require separate owning-repo PRs. FractalOS
has a draft Tile-job header, not a working tensor backend. Eight-phase scheduling
remains proposed vocabulary rather than a normative clock migration.
