# Versioning and development tracking

`tools/registry.py check` enforces every rule on this page that a machine can check, and CI runs it.

## 1. Research IDs

* Format `CR-NNNN`, assigned sequentially from `REGISTRY.json:next_id`.
* An ID is **permanent**. It is never reused or renumbered, and it survives promotion and archiving.
* Folder name: `<stage>/CR-NNNN_<slug>`, where the slug is kebab-case and starts with a letter.

## 2. Stages

| Stage | Folder | Allowed status | Version range | Meaning |
| :--- | :--- | :--- | :--- | :--- |
| experimental | `experimental/` | `[OPEN]`, `[HEURISTIC]`, `[COMPUTED]` | 0.x.y | Active research. Anything may change. |
| published | `published/` | `[COMPUTED]`, `[PROVEN]` | ≥ 1.0.0 | Frozen spec, reference code and vectors |
| archived | `archived/` | `[FAILED]`, `[SUPERSEDED]` | any | Kept as evidence. Never deleted. |

Status tags reuse the SHD-CCP Kernel Ontology vocabulary (`SHD-CCP_Kernel_Ontology/00_Ontology_Core/epistemic_tags.md`) with the same meanings:

* `[OPEN]`: untested idea.
* `[HEURISTIC]`: complete design, justified by reasoning and tested in-repo.
* `[COMPUTED]`: every defined check passes, including vectors, negative fixtures and any external conformance.
* `[PROVEN]`: `[COMPUTED]`, and the security-relevant claims are machine-checked (Lean 4) or reduce to a cited standard assumption.

Individual tracks inside an item carry their own tags in `manifest.json:tracks`. A `[FAILED]` track does not fail its item.

## 3. Semantic versions per item

Each item has its own `MAJOR.MINOR.PATCH` in `manifest.json`, mirrored in `REGISTRY.json`.

| Change | Experimental (0.x) | Published (≥ 1.0) |
| :--- | :--- | :--- |
| Wire layout, vector bytes or hash definition | MINOR | **MAJOR** |
| New track, new API, new vectors added | MINOR | MINOR |
| Docs, tests, refactors with byte-identical vectors | PATCH | PATCH |

Frame and wire profiles carry their own version in their ID, for example `cr-0001.otp-frame.v0`. A profile ID is bumped whenever its bytes change, independently of the item version.

## 4. Required tracking files

| File | Rule |
| :--- | :--- |
| `manifest.json` | Keys `schema_version id slug title stage status version created updated`. An upstream reference needs a full 40-hex `commit` and a recorded `license`. |
| `CHANGELOG.md` | [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). It must contain `## [<current version>]`. |
| `RESEARCH_LOG.md` | Append-only, dated lab notebook (done, found, decided). Corrections are new entries. |
| `README.md` | Status table, findings table, layout, run commands. |
| `vectors/` | Deterministic generator with `--check`, if the item has wire bytes |

## 5. Git conventions

* Branches: `research/CR-NNNN-<topic>` for item work. Session branches are fine for agents.
* Commits: prefix the subject with the item ID, for example `CR-0001: add E3 frame verifier`. Folder-wide changes use `cryptographic-research:`.
* Tags: once a version is merged to `main`, tag it `cr-NNNN/vX.Y.Z`. Published releases may also get a GitHub release whose notes are the CHANGELOG section.
* Upstream code is never vendored without a compatible license. Pin it by commit in the manifest instead.

## 6. Promotion: experimental → published

Promotion is a reviewed PR that does all of the following:

1. Moves the folder with `git mv experimental/CR-NNNN_x published/CR-NNNN_x`, keeping the ID.
2. Sets `stage: published`, a status of `[COMPUTED]` or `[PROVEN]`, and version `1.0.0`.
3. Freezes every wire profile, removing `Draft` from the binding spec, and closes or explicitly defers every open question.
4. Adds a research-log entry that summarizes the evidence, and a CHANGELOG `1.0.0` section.
5. Passes the checklist in [CONTRIBUTING.md](CONTRIBUTING.md#promotion-checklist).

Archiving follows the same pattern into `archived/`, with a post-mortem entry in the research log.
