# Sources, assumptions and unresolved decisions

## Source access

The referenced conversation is “Design FractalOS Framework”, ID
6ad47e0d-bbf0-83ea-a7ae-681d35706282. Only its supplied bounded preview was
available. No thread-reading tool was exposed; its full AlexNet-H design and
13 paper attachments were not reviewed. Accordingly this proposal cannot claim
to preserve every prior decision or the custom flowchart viewer's syntax.

Available earlier full research bundle contains six PDFs and seven architectural
Markdown documents. Selected searchable passages were inspected for arithmetic,
protocol, temporal-reconstruction and runtime boundaries, not as a complete
mathematical proof review. In particular the Fifteen Lemmas PDF's extracted text
is not a reliable complete source; existing code/fixtures govern current behavior.
Hashes and precise filenames are in `contracts/source_inventory.v1.json`.
No research PDFs are recopied into the new proposal or claimed as newly verified.

Current implementation sources: Geometric-Labs baseline d8c92a4, the existing
local Tile profile, source package, ecosystem profile matrix and pinned
FractalOS compute_backend.h. Current baseline passes 40 tests; prior integration
report records 64 combined tests. This task reruns and reports actual checks
separately. Neither count measures neural training capability.

## Hypotheses, not inherited facts

1. Use torchvision-style AlexNet and a matched Euclidean prototype control.
2. Compare Poincare geometry at d=128, fixed c=1 before learning curvature.
3. Represent geometric metadata separately from learned continuous embeddings.
4. Stage quaternion, temporal, transport and accelerator experiments independently.
5. Keep all dataset access and publication opt-in; no downloads/training now.

These are new explicit implementation defaults, not quotes from the unavailable
AlexNet-H conversation. AlexNet has no demonstrated unique mathematical
compatibility with this engine; it is a tractable historical experimental baseline.

## Decisions for the first implementation PR

| Decision | Default until reviewed | Required evidence/change |
|---|---|---|
| Dataset/license | local synthetic smoke, then operator-provided licensed classification data | dataset manifest, disjoint source-level splits |
| Primary objective | classification; hierarchy/retrieval separate | predeclared primary metric and comparison margin |
| Full model dependencies | optional CPU PyTorch/torchvision pair | actual install/forward/backward test and lock, not hypothetical pins |
| Original AlexNet vs torchvision | precisely documented torchvision-style E0 | separate ID for LRN/grouped original or modified small-image stem |
| Geometric mapping | explicit metadata sidecar | calibrated correspondence before physical scene claims |
| Quaternion feature convention | optional learned four-channel latent groups | defined action and equivariance/gradient tests |
| New protocol forms | none | upstream versioned RFC/human review |
| Custom viewer ontology grammar | neutral node/edge JSON with proposed ontology paths | supply real grammar/example and test import/export before compatibility claim |
| Full prior AlexNet-H alignment | provisional | full thread export/attachments needed to reconcile prior decisions |
| Publishing/deployment | local proposal only | separate reviewable implementation stages |

No missing preference prevents producing this proposal. Dataset selection and an
actual compatible optional ML environment become prerequisites when P0/P1 begin.
