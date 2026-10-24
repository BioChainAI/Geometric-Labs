# {{ID}}: {{TITLE}}

> Stage and Lean status live in `manifest.json` and in the library [catalog](../../CATALOG.md).

## Source

* **Citation**: TODO (authors, title, venue, year)
* **Where the original lives**: `source/` (PDF), or a URL if the file is too large or not ours to redistribute
* **License / redistribution**: TODO

## Summary

TODO: two or three sentences on what the paper claims and why we are working through it.

## Artifact map

| Folder | Holds | Produced by |
| :--- | :--- | :--- |
| `source/` | Original PDF, `.tex` or `.txt` | You |
| `markdown/` | Markdown + LaTeX transcription | IDE **Save to Repo** |
| `audits/` | Audit prompt, `canonical_registry.json`, audit notes and external LLM audit replies | IDE **Audit** tab |
| `lean/` | `GeometricLabs_<paper>.lean` and hand-edited Lean modules | IDE **Export Lean 4 (.lean)** |
| `flowcharts/` | `Flowchart-Lean4-Bundle-*.json`, `Guided-Flowchart-Lean4-Walkthrough-*.md` | IDE **Flowchart & Lean 4** |
| `cosmo/` | `CosmoID-Ledger-*.json`, `SHD-CCP-CosmoID-*.png` | IDE **Cosmo-ID** tab |
| `workflows/` | Agent run logs, prompts, step-by-step procedures used on this paper | You / agents |
| `postprocessing/` | Anything derived later: tables, plots, Python checks, datasets | You / agents |

## Key results

| Claim (paper ref) | Epistemic tag | Where checked |
| :--- | :--- | :--- |
| TODO | `[OPEN]` | - |

## Open questions

* TODO
