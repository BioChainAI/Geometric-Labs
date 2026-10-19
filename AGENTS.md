# AGENTS.md — Geometric-Labs ecosystem integration guidance

Scope: applies to work in `BioChainAI/Geometric-Labs` if placed in the repository root. Component repositories retain their own instructions. More-specific in-repository AGENTS.md files override these only where they do not violate cross-system security and conformance requirements.

## Mission

Preserve the existing Geometric-Labs exact-arithmetic reference project; add an `ecosystem/` integration workspace referencing seven separately versioned BioChain AI repositories. Build an auditable decentralized cubic-geometric data platform with optional hosted accelerator adapters, not a monolithic rewritten application.

## Before any write

- Run `git status --short`, `git rev-parse HEAD`, inspect existing instructions and CI; never discard changes.
- Run `make verify-all` and save baseline logs; note if tools/dependencies prevent the run.
- Read `spec_sync/einstein_tile_64bit_rfc.md`, `docs/specification_status.md`, `README.md`, and all new compatibility and acceptance docs.
- Keep `src/geometric_labs/`, `verification/`, `spec_sync/golden_vectors/`, the original Makefile, and the existing workflow intact unless a proposed change has an explicit compatibility rationale and tests.

## Source of truth

- Canonical core layout lives in `BioChainAI/SHD-CCP-core`; Geometric-Labs local vectors are conformance references with provisional semantics. Do not silently collapse profiles.
- Registry approval is not mathematical proof or authorization to use an AI tool.
- Authentication belongs to signed envelopes and explicit policy controls, never a South Halo/CRC/TQF result.
- Causal, frame, calibration and time uncertainty metadata must survive transformations. Do not invent a common clock or frame.
- `CubiLoom` owns replica/event storage, `PolyShard-Agent` local/private data, and `Polycentric-Orchestrator` coordination and derived views.
- No production Firestore/Firebase access; `BioChain-AI` is optional and isolated.

## Implementation safety

- Additive `ecosystem/` path first. Use `integration-overlay/` as a reviewable candidate, not a blind overlay patch.
- Use explicit profile IDs, schema versions, golden vectors and SHA release locks.
- Tests: positive and negative fixtures (wrong profile/form, expired frame calibration, replay, denied consent, clock uncertainty, offline, duplicate, out-of-order/orphan, shader difference).
- No secrets in repo, logs, test fixtures or prompts; dev authentication is never labeled production.
- Feature gates for GPU SM90/H100, Loihi2/Lava, QEMU and experimental compression; no blanket portability claim.
- End every wave with an `ecosystem/docs/status/<wave>.md` report and reviewable PR. Do not auto-merge `main`.

## Convenient commands

```bash
make verify-all
make test-pillars
make check-vectors
python3 ecosystem/tools/glab.py list
python3 ecosystem/tools/glab.py doctor
make -C ecosystem test
make -C ecosystem demo
make -C ecosystem geometry
make -C ecosystem lock
```

Only use commands actually present after confirming the overlay has been integrated. If `Makefile` targets or paths changed, read current sources rather than assuming.
