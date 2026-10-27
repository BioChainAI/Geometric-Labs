# First research archive intake

Date: 2026-10-26 (America/Chicago). Base commit:
`0040e9e8c3635ade7a59afa3f65ee551bc7b81ce`.
Branch: `codex/research-archive`. The initial intake snapshot below was recorded
before publication. No cross-repository write or Pages deployment was performed.

Publication preparation, 2026-10-27: the user authorized committing and pushing the archive
branch. Fresh `make verify-all`, `make -C Research_IDE check` (27 tests), and Pages tests
(12 tests) passed. `origin/main` still matches the base commit. The earlier five untracked
architecture-investigation artifacts are outside this archive commit. Git history and the
remote branch record the resulting publication; this report does not assert a merge or deployment.

## Result

The first eleven supplied PDFs are preserved under `Research_IDE/papers/`, with stable
RP IDs, original filenames and source-byte hashes. Ten WORK families organize them;
the two torsional memory-pump formulations share a family without asserting revision order.
Five PDFs are byte-identical to available earlier uploads. The new Fifteen Lemmas file
differs from the older similarly titled upload; no supersession is assumed.

The [archive guide](../../../Research_IDE/archive/README.md) defines identity, lineage,
classification, future intake and release promotion. The
[architecture map](../../../Research_IDE/archive/ARCHITECTURE_MAP.md) and generated index
provide page-cited triage plus eight repository reading lists. Originals are stored once;
future component citations pin an archive commit, RP ID and source hash. The seven
independent component checkouts were not modified.

The existing library CATALOG now contains eleven entries. Its original browser HTML and
IDE lock remain unchanged. Existing library stages and proof semantics are preserved.
The additive archive tool checks exact source bytes, metadata, duplicate revisions,
repository names, explicit relation targets/cycles and release evidence records. It
generates deterministic indexes, filters relevance by repository/topic/status, and
identifies renamed duplicates by hash. Archive checks run through the existing
`make -C Research_IDE check` CI entrypoint. Python standard library only.

Root/documentation links and the reviewed Pages section metadata point to the archive.
The site already scans CATALOG counts; its curated upload allowlist remains intact.
PDFs were not added to the deployed static artifact, and historic checkpoint records
were not regenerated as though their old evidence applied to this wave.

## Scientific review scope

This is architectural relevance triage, not a full mathematical audit. All eleven PDFs
have derived layout text, extraction provenance and individual reading notes. Text and
selected passages were reviewed for architectural placement; formula pages in the 4D,
folded-packet and sparsemax papers were visually inspected. Display equations are lost
in parts of the first three PDFs. No OCR, external citation verification, original PDF
appendix-script execution, Lean compilation, model training or physical measurement
was performed. Author proof/release labels remain source claims.

Key distinctions recorded include torus versus full S³ state space, winding assumptions,
quadratic feature measurements versus exact geometric TQF, rational sparsemax versus the
full valve-modified pump, base-referenced versus stationary current, and computed
calibration budgets versus measured uncertainty. The exact existing Hurwitz implementation
reproduces a counterexample to the memory paper's fixed-coordinate-width inference:
`h_mul(H_TIER, (1,1,1,1)) == (0,0,2,0)`, with norm one on both sides.

All documents remain `research-draft`, `retained-reference`, library stage `intake`,
Lean status `none`. A release record requires a declared version, approval/date,
license and tracked evidence bound to the source hash. Metadata validation is not
authentication of the approver or scientific proof.

## Validation

- Baseline `make verify-all`: PASS, including 40 unittest methods and five frozen-vector files.
- `make -C Research_IDE check`: PASS, eleven live entries, catalog/IDE/archive integrity,
  27 tests (16 existing library tests plus 11 archive tests).
- `python3 -m unittest discover -s tools/pages/tests -v`: PASS, 12 tests.
- All eleven archived PDFs equal the supplied uploads byte-for-byte: 3,897,547 source bytes.
- Local Markdown archive/entry links resolve; exact duplicate identification and
  repository/topic filtering exercised; `git diff --check` passes.
- Protected exact-math sources, scientific vectors and workflows, original Makefile,
  component clones and original IDE HTML/lock have no changes from this wave.

The five untracked investigation artifacts present before this task were retained unchanged.
They are separate from the archive intake. No new full-ecosystem or hardware verification
claim is made. See [machine-readable intake evidence](research-archive-validation.json).
