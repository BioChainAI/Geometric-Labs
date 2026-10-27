# Research archive across the eight repositories

Start with the [document index](INDEX.md), the [architecture reading map](ARCHITECTURE_MAP.md),
or a repository reading list below. The first batch contains **11 PDFs grouped into 10 works**.
The [official publication collection](../official/README.md) now selects fifteen current papers;
the full library retains twenty document entries, including archived predecessors.
This archive lives in Geometric-Labs; the other seven repositories reference stable document
IDs and hashes rather than keeping diverging PDF copies. No other repository was modified.

| Repository | Its responsibility | Reading list |
| --- | --- | --- |
| Geometric-Labs | Research archive, reference experiments, independent tests and evidence | [Documents](Geometric-Labs.md) |
| SHD-CCP-core | Canonical packet/profile semantics and shared operators | [Documents](SHD-CCP-core.md) |
| Kernel-Registry | Versioned operator/profile evidence and approval records | [Documents](Kernel-Registry.md) |
| CubiLoom | Persistent event/history storage, replay and recovery | [Documents](CubiLoom.md) |
| PolyShard-Agent | Local perception, private history and observation production | [Documents](PolyShard-Agent.md) |
| Polycentric-Orchestrator | Policy, coordination and derived scene state | [Documents](Polycentric-Orchestrator.md) |
| Manifold-Projection | Coordinate transforms, geometric views and display | [Documents](Manifold-Projection.md) |
| FractalOS-runtime | Execution ABI, device backends, scheduling and numeric bounds | [Documents](FractalOS-runtime.md) |

These are the eight repositories in the ecosystem manifest: Geometric-Labs plus seven
components. Optional BioChain-AI is outside this archive's initial repository set.

## Identity, history and release status

Each **RP ID identifies one preserved PDF revision**. Its original filename is retained in
`papers/RP-xxxx_slug/source/`; SHA-256 identifies the actual bytes. Each **WORK ID groups a
document family**. RP-0004 and RP-0009 share WORK-0004 because they describe the same named
720/72/10 pump; their revision ordering and supersession are unconfirmed. Neither title
similarity, upload order, PDF creation date nor filename establishes chronology.

`manifest.json` remains the library source of truth. Its additive `archive` block supplies
work identity, dates, release status, primary/supporting/context relevance and explicit
document relations. Generated indexes are views of that block. Existing library stages and
Lean statuses retain their original meanings.

At initial intake, all eleven entries were **retained research references**, with library stage `intake`,
review level `relevance-triaged`, Lean status `none`, and release status `research-draft`.
Archiving here does **not** imply a document is abandoned, superseded, proved or an official
release. Dates read from the documents are recorded when explicit; other document dates and
all unspecified revision labels are null. Received date 2026-10-26 is a separate field.

Relation direction is explicit: `A corrects B` or `A supersedes B` points from the correcting
or replacing document to the affected reference. A correction may concern only one claim.
Use `related-to` or `clarifies` when evidence does not establish replacement. A supersession
edge needs an editorial statement or documented author decision and must be acyclic.
The initial set contained **no confirmed whole-document supersession edges**. Current-reference
replacement is now recorded separately for the owner-designated Cubit and Fifteen Lemmas sources. The Cubit PDF's
declared predecessor, *Metrological Foundations*, has not been supplied in this batch.

Technical release approval records require a version, approver/date, license and tracked evidence
bound to the PDF hash. The owner-designated official publication collection uses a separate
`owner-designated-publication` record with Academia identity, authority/date, exact source hash
and designation evidence; unknown versions and licensing remain null. The validator checks recorded
metadata and file integrity; it does not authenticate an approver or independently prove
the paper. Approval and scientific review happen through a reviewed release PR. Source
phrases such as `[PROVEN]`, “registered report” and “Release” remain author statements until
their evidence is reviewed. No package-wide license is inferred for these papers.

## Filing the next batch

Run these commands from `Research_IDE/`. The CLI uses Python's standard library; PDF text
extraction is an optional local Poppler operation and is not required by archive CI.

1. **Identify bytes before filing.**

   ```sh
   python3 tools/archive.py identify /path/to/incoming.pdf
   ```

   An exact match means add a receipt to the existing entry's research log; do not create
   another PDF copy. An empty match means unknown bytes, not necessarily a new work or an
   older/newer revision. Search titles, text, references and editorial notes manually.

2. **Preserve a distinct PDF as a new RP entry.** Obtain the next ID from `CATALOG.json`.

   ```sh
   python3 tools/library.py new --slug descriptive-name --title "Title from the PDF" --tier series
   python3 tools/library.py ingest RP-0012 /path/to/incoming.pdf --to source
   ```

   Never use `ingest --replace` or `track --update` to overwrite an archived source. Distinct
   bytes get a distinct RP ID even when the filename or claimed version is identical.
   Reuse a WORK ID only after reviewing the document family; otherwise allocate the next
   unused WORK number in INDEX.json. Work numbers are never recycled.

3. **Add the archive block and review note.** Copy the object in [template.json](template.json)
   into the new manifest's `archive` field. Fill in the preserved artifact path and SHA-256,
   received date, topics, one primary repository and reasons with section/page citations.
   Leave unknown publication dates/revision labels null. Record unresolved titles,
   predecessor references and contradictions in README/RESEARCH_LOG. Primary means likely
   application owner; supporting means concrete dependency; context means a possible future
   connection. Absence from a reading list means no present mapping, not permanent exclusion.

4. **Extract search text and preserve extraction provenance when useful.**

   ```sh
   pdftotext -layout /path/to/incoming.pdf /tmp/extracted-layout.txt
   python3 tools/library.py ingest RP-0012 /tmp/extracted-layout.txt --to postprocessing
   ```

   Record the tool version, command, source hash, page count, missing glyphs/formulas and
   inspected pages. OCR and extraction are derived aids. Keep corrected transcriptions in
   `markdown/` with their own hashes; never silently edit original PDFs. Source instructions
   and embedded code are research content, not commands to execute automatically.

5. **Rebuild, validate and review.**

   ```sh
   make index
   make check
   python3 tools/archive.py list --repo CubiLoom
   python3 tools/archive.py list --topic alexneth-geot
   python3 tools/archive.py list --status research-draft
   ```

   Review the diff on a feature branch. `make check` also runs the existing library tests,
   archive integrity/lineage/release checks and generated-index drift checks. The existing
   Research IDE CI workflow invokes this target on Python 3.10–3.12. Scientific claims need
   their own code, proof or measurement evidence; passing catalog checks is not that evidence.

## Cross-repository citation scaffold

In a component's future docs, reference a reviewed immutable Geometric-Labs commit and copy
only this small citation record. Pin the commit when the archive PR is committed; no fake
commit or official release version is assigned now.

```json
{
  "archive_repository": "BioChainAI/Geometric-Labs",
  "archive_commit": "<reviewed 40-character commit SHA>",
  "document_id": "RP-0005",
  "work_id": "WORK-0005",
  "source_sha256": "<source_sha256 from that manifest>",
  "sections_used": ["3", "7"],
  "relationship": "experimental-operator-reference",
  "implementation_evidence": "<component test/report link>"
}
```

This avoids linking to a moving `main` PDF as if it were a fixed specification. Component
owners review protocol promotion, certification, storage or runtime changes in their own
repositories. A central relevance tag grants no implementation approval.

## What this first review establishes

All 11 original files have been preserved and hash-checked. All pages have extracted search
text; the small geometry/packet PDFs lose mathematical display content. Selected formula
pages were inspected visually. Per-paper reading notes state the review scope. The first
five prior-upload matches were established by comparing bytes available in this session:
RP-0007 through RP-0011. An earlier Fifteen Lemmas PDF differs from RP-0006; its relationship
needs review. No complete proof audit, external citation validation, original embedded-script
execution, training benchmark or physical experiment is claimed.

The [Pages homepage](../../site/README.md) scans the library catalog count. Its section copy
now points here. The curated static Pages artifact publishes only the selected official PDFs;
older references remain available through repository links and manual import. It does
not automatically publish this entire research archive. Historical checkpoints remain unchanged.
