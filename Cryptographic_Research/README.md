# Cryptographic Research

This is the Geometric-Labs research line for **adapting classical cryptographic algorithms to geometric computation** and integrating them with the BioChain ecosystem over **64-bit SHD-CCP cubic data protocols** (Einstein Tiles).

Every algorithm enters as an experimental research item. It is studied against a pinned upstream reference, re-implemented clean-room, tried in geometric variants, bound to SHD-CCP tiles, and promoted to `published/` only once its evidence and specification are frozen.

## Principle

A geometric adaptation must **not weaken the security assumption it inherits**. Each item keeps three layers apart and records which layer every geometric idea touches:

| Layer | Example | May be geometric? | Carries security? |
| :--- | :--- | :--- | :--- |
| One-way / hard core | hash, signature, KDF | Only if it survives cryptanalysis | **Yes** |
| Representation | quaternion or lattice views of values | Yes | No |
| Transport | SHD-CCP tile frames, South Halo routing | Yes | No |

Negative results count as results. CR-0001 shows that an exact quaternion walk is invertible, and it ships that walk as a tested negative control.

## Layout

```text
Cryptographic_Research/
├── README.md              this file
├── VERSIONING.md          IDs, semver, stages, tags, changelogs, git tags
├── CONTRIBUTING.md        research workflow and promotion checklist
├── ROADMAP.md             candidate algorithms after CR-0001
├── CHANGELOG.md           changes to this folder's structure and tooling
├── REGISTRY.json          machine-readable index of every research item
├── Makefile               check | registry | test | check-vectors | list | new
├── tools/registry.py      validates the registry and scaffolds new items
├── tests/                 tests for the tooling
├── templates/experiment/  skeleton copied by `make new`
├── experimental/          active research (versions 0.x)
│   └── CR-0001_lamport-otp/
├── published/             frozen, specified algorithms (versions ≥ 1.0.0)
└── archived/              failed or superseded items, kept as evidence
```

## Research items

| ID | Item | Stage | Status | Version |
| :--- | :--- | :--- | :--- | :--- |
| [CR-0001](experimental/CR-0001_lamport-otp/) | Lamport one-time passwords: geometric adaptation | experimental | `[HEURISTIC]` | 0.1.0 |

`REGISTRY.json` is the source of truth for this table, and `make list` prints it.

## Quick start

These commands use Python 3.10+, the standard library, and the repository's `src/geometric_labs`:

```sh
make -C Cryptographic_Research check        # registry + all tests + vector drift
make -C Cryptographic_Research list
make -C Cryptographic_Research demo-cr0001
make -C Cryptographic_Research new SLUG=merkle-signature TITLE="Merkle signatures"
```

CI runs `make check` in [`.github/workflows/cryptographic-research.yml`](../.github/workflows/cryptographic-research.yml) on Python 3.10–3.12.

## Relationship to the rest of the ecosystem

* **Tile layer**: items bind to the local profile `geometric-labs-reference-v1` through `geometric_labs.tile_codec`, and they name every profile they depend on. The Form ID position is still unreconciled across Geometric-Labs, SHD-CCP RFC 01 and the SHD-CCP Kernel Ontology. Each item records that dependency as an open question rather than resolving it locally.
* **Kernel Ontology**: published tile layouts are proposed to `SHD-CCP_Kernel_Ontology/01_Incubator_Experimental` as `[OPEN]` kernels. Research promotion here is not ontology certification.
* **Authentication rule** (from `AGENTS.md`): the South Halo, gate byte, CRC and TQF results are never authenticators. Authentication lives in the cryptographic core.

Nothing in this folder is production authentication. Read each item's threat model before reusing it.
