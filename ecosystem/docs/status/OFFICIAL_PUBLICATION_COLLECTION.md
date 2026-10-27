# Official publication collection and Research IDE v3.3

Date: 2026-10-27 (America/Chicago). Base: `9ae52515af98` (archive CI/route fix
merged through PR #8). Branch: `codex/official-research-corpus`.

## Outcome

The owner's fifteen Academia URLs designate the first **official ecosystem paper
collection**. [Official catalog](../../../Research_IDE/official/CATALOG.md) and
[maintenance instructions](../../../Research_IDE/official/README.md) record the set.
The IDE opens this collection by default instead of its six built-in sample excerpts.
Select a paper for source metadata, repository/label information and publication/PDF
links; Open PDF in IDE checks SHA-256 before parsing and rendering the preserved source.
Working transcriptions remain local until exported. No AI request is made by this flow.

Manual PDF/Markdown imports and new drafts always enter the separate Research Desk,
including when the official tab was selected. They do not join the official list.
Catalog failure displays a retryable error instead of silently restoring sample papers.
Missing icon/3D dependencies no longer interrupt paper browsing. PDF.js is still
required for inspection; source PDF links remain available independently.

## Source matching and reference transfer

- Fifteen uploads contain fourteen distinct byte streams: Sparsemax was uploaded twice.
- Five supplied PDFs exactly match existing entries (RP-0002, 0004, 0005, 0009 and 0010);
  designation uses those entries without duplicating their PDFs.
- The short-named Fokker upload is the **companion**, now RP-0019, matched to publication
  179087320. The main publication 179087267 uses the title-matched, 38-page RP-0008 PDF
  already supplied at earlier intake. This source choice is recorded explicitly; no
  remote Academia file-version equality is claimed.
- Nine new distinct source files become RP-0012 through RP-0020. Twenty document entries
  are retained; fifteen are selected as current official publications and five remain
  archived references.
- RP-0018 (Cubit) replaces the RP-0011 reference entry; RP-0020 (Fifteen Lemmas) replaces
  RP-0006. Their WORK families, repository relevance, tags and topics transfer with the
  predecessor's source hash and metadata snapshot. The older PDFs remain unchanged and
  their manifests/READMEs resolve to the new official references. Distinct export bytes
  do not establish a scientific content-revision order.
- The companion inherits useful relevance from the related main sieve paper without
  replacing it. The two separately listed memory-pump publications remain separately
  official; no unsupported supersession between them is inferred.

## Status semantics and publication

Owner-designated official status is separate from proof review, Lean compilation,
physical experiments, accepted protocol changes and software releases. The additive
`owner-designated-publication` release record binds the owner's instruction, Academia
identity, designation date, source hash and tracked evidence. It does not invent a
license or version. Previous technical approval record requirements remain intact.
Library stage remains intake and Lean status none; author theorem titles/tags are
source statements. This intake is relevance/identity triage, not a full paper audit.

The IDE HTML and local loader are hash-locked as v3.3, retaining the prior IDE hash.
The original uploaded IDE remains in Git history. Generated archive reading lists
include both releases and archived references with explicit reference state.
`releases.py resolve` follows current-reference links; validators reject lost inherited
labels/repositories, mismatched sources, duplicate publications and invalid lineage.

Pages now publishes exactly the selected official PDFs, catalog and loader, retaining
the previously fixed uppercase Research_IDE redirect. Unselected archive PDFs are
excluded. Artifact checks reject missing, tampered or extra PDFs. No component checkout,
mathematical source, frozen vector, protocol profile or device backend is modified.

## Executed checks

- Root baseline: `make verify-all` passes (40 test methods and five frozen-vector files).
- Full pinned acceptance passes on actual Python 3.10.22 and 3.12.14, including 23 offline
  methods, four integration methods, 183 packet cases, locks and exact demo TQF 576.
- Library/archive/official checks pass on Python 3.10 and 3.12: 34 tests.
- Pages checks: 15 tests; pure JavaScript corpus checks: four tests.
- Functional Chromium IDE check passes with real PDF.js 3.11.174: exact official-only
  default membership, manual Markdown/PDF isolation, SHA-checked original PDF rendering,
  tampered-PDF refusal, catalog failure and retry. Local pinned PDF.js test dependencies
  were retrieved from jsDelivr because the environment proxy blocks cdnjs. Other CDNs
  were blocked in this check; styling/3D and AI calls are outside its validation scope.
- Existing desktop/mobile homepage and project-subpath browser checks pass.
- Previously tracked PDFs remain byte-identical; IDE inline JavaScript parses; generated
  catalogs and source hashes validate. Original PDF instructions/scripts were treated as
  source data, not automatically executed.

Machine-readable evidence: [official-publication-validation.json](official-publication-validation.json).
Browser logs and test reports live under `/tmp/geometric-official-*`. Changes publish
through a review branch; live Pages changes require a subsequent main merge/deployment.
The five pre-existing untracked architecture-investigation files remain outside this wave.
