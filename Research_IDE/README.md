# Research IDE & Paper Library

This folder holds the **Geometric Labs PDF-to-Markdown & LaTeX Research IDE** (`index.html`, SHD-CCP IDE v3.2) and the **paper library** where everything we produce with it is filed: transcriptions, audits, Lean 4 proofs, flowcharts, Cosmo-ID ledgers, workflows and post-processing data.

The [eight-repository research archive](archive/README.md) now holds the first eleven
preserved PDFs, with repository reading lists, revision families, source hashes and release
status. Start with its [architecture map](archive/ARCHITECTURE_MAP.md) to find where a paper applies.

The IDE is a single browser page. It keeps your work in memory only. Nothing survives a page reload unless you export it. The library is how those exports become a searchable, hash-checked database in git.

**New here? Read [WALKTHROUGH.md](WALKTHROUGH.md).** It takes one paper from PDF to a verified, catalogued entry, step by step.

## Layout

```text
Research_IDE/
├── index.html                  the IDE (unchanged from upload; hash pinned in ide.lock.json)
├── ide.lock.json               IDE version, SHA-256 and CDN dependencies
├── WALKTHROUGH.md              step-by-step guide: PDF → library entry
├── README.md                   this file
├── CHANGELOG.md                changes to the IDE build and this folder's tooling
├── CATALOG.json                generated database index of every paper (do not edit)
├── CATALOG.md                  generated human-readable catalog (do not edit)
├── Makefile                    serve | new | ingest | track | list | index | check | lock-ide
├── docs/
│   └── MASTER_OPERATION_GUIDE.md   full IDE reference: UI zones, LLM rules, SHD-QL, DOM API
├── inbox/                      browser downloads land here; git-ignored until ingested
├── papers/
│   └── RP-0001_<slug>/         one folder per paper (created by `make new`)
│       ├── manifest.json       source of truth: metadata, stage, Lean status, artifact hashes
│       ├── README.md           citation, summary, key results, open questions
│       ├── RESEARCH_LOG.md     append-only lab notebook
│       ├── source/             original PDF / .tex / .txt
│       ├── markdown/           Markdown + LaTeX transcription
│       ├── audits/             audit prompt, canonical_registry.json, audit notes
│       ├── lean/               Lean 4 modules
│       ├── flowcharts/         flowchart JSON bundle + Mermaid walkthrough
│       ├── cosmo/              Cosmo-ID ledger JSON + sigil PNGs
│       ├── workflows/          agent runs, prompts, procedures used on this paper
│       └── postprocessing/     derived tables, plots, scripts, datasets
├── templates/paper/            skeleton copied by `make new`
├── tools/library.py            the library tool (standard library only)
└── tests/test_library.py
```

## How exports are sorted

`make ingest PAPER=RP-0001` files every download in `inbox/` by name:

| IDE button | File | Goes to |
| :--- | :--- | :--- |
| Upload PDF (your original) | `*.pdf`, `*.tex`, `*.txt` | `source/` |
| **Save to Repo** | `<paper>.md` | `markdown/` |
| **Save Audit Prompt v2 (.md)** | `Geometric_Engine_Lemma_Audit_Prompt_v2.md` | `audits/` |
| **Registry (69)** | `canonical_registry.json` | `audits/` |
| **Export Lean 4 (.lean)** | `GeometricLabs_<paper>.lean` | `lean/` |
| **Export JSON Bundle** | `Flowchart-Lean4-Bundle-<paper>.json` | `flowcharts/` |
| **Export Mermaid + Lean (.md)** | `Guided-Flowchart-Lean4-Walkthrough-<paper>.md` | `flowcharts/` |
| **Export Cosmo JSON** | `CosmoID-Ledger-<paper>.json` | `cosmo/` (also sets the paper's `cosmo_id`) |
| **PNG ↓** | `SHD-CCP-CosmoID-<hex>.png` | `cosmo/` |
| your notes | names containing `audit` / `workflow` | `audits/` / `workflows/` |
| anything else | other `.md` → `markdown/`; the rest → `postprocessing/` | or choose with `--to <folder>` |

Every filed artifact is recorded in the paper's `manifest.json` with its SHA-256, size and date.

## Paper lifecycle

| Stage | Means | `check` requires |
| :--- | :--- | :--- |
| `intake` | Folder exists; source may or may not be attached | — |
| `transcribed` | Markdown + LaTeX transcription exists | a `markdown/` artifact |
| `audited` | SHD-CCP audit run and findings recorded | + an `audits/` artifact |
| `formalized` | Lean 4 module written | + a `lean/` artifact |
| `verified` | Lean compiled outside the IDE | + `lean_status: lake-verified` |
| `archived` | Abandoned or superseded; kept as evidence | — |

`lean_status` is tracked separately: `none` → `draft` → `sorry-free` (no `sorry` outside comments) → `lake-verified` (compiled with `lake`, and the toolchain, command, date and person are recorded).

> **The IDE does not run Lean.** Its InfoView, `PASS` badges and the `proven` node status are display state that you set by hand. The 9 default flowchart nodes start marked `proven`. Only `lake-verified` in the library means a compiler accepted the file.

## Commands

```sh
make serve                                    # IDE at http://localhost:8080/
make new SLUG=fifteen-lemmas TITLE="The Fifteen Lemmas of the Geometric Engine" TIER=core
make ingest PAPER=RP-0001                     # file inbox/ into the paper
make track PAPER=RP-0001                      # record files you added by hand
make list                                     # all papers
python3 tools/library.py list --stage audited --tag hurwitz
python3 tools/library.py set RP-0001 --stage transcribed --tag hurwitz
make check                                    # validate everything + run tests
```

CI runs `make -C Research_IDE check` on Python 3.10–3.12 ([workflow](../.github/workflows/research-ide.yml)).

## Relationship to the rest of the repository

* `docs/papers/core/` and `docs/papers/series/` hold the **canonical** paper set that `src/geometric_labs/` and `verification/` cite. A transcription that reaches `verified` here can be promoted there by copying its Markdown (see [WALKTHROUGH.md, Step 14](WALKTHROUGH.md#step-14-promote-and-commit)).
* The IDE's `canonical_registry.json` and audit rules are reference data inside the page. They are not the repository's executable conformance suite. Run `make verify-all` at the repository root for that.
* Epistemic tags (`[PROVEN]`, `[COMPUTED]`, `[CORRESPONDENCE]`, …) follow the same meaning as in `Cryptographic_Research/` and the master guide §3.4.
