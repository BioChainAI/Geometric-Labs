# Changelog

Changes to the IDE build and to this folder's tooling. Changes to individual papers are recorded in each paper's `RESEARCH_LOG.md`.

## 2026-10-23

### Added
* `index.html`: Geometric Labs PDF-to-Markdown & LaTeX Research IDE, **SHD-CCP IDE v3.2** (upload `geometric_labs_pdf_to_markdown_latex_research_ide_11.html`), installed unchanged. SHA-256 pinned in `ide.lock.json`.
* `docs/MASTER_OPERATION_GUIDE.md`: the IDE master operation, SHD-QL and agentic execution manual, unchanged from upload.
* `WALKTHROUGH.md`: step-by-step guide from PDF to a verified library entry.
* Paper library: `papers/`, `templates/paper/`, `inbox/`, `CATALOG.json` / `CATALOG.md`, `tools/library.py` (`new`, `ingest`, `track`, `set`, `list`, `index`, `check`, `lock-ide`) and its tests.

### Known issues in this IDE build
* **Export Lean 4 (.lean)** repeats `import Mathlib.Tactic` inside each node after other code, so the file does not compile as exported. `WALKTHROUGH.md` Step 12 shows the fix-up.
* The 9 default flowchart nodes start with status `✓ Proven` whatever their code contains. The IDE does not run Lean.
* `marked` and `lucide` load from CDNs at unpinned versions (`ide.lock.json`).
