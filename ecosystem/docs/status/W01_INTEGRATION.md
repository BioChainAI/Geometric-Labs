# Wave 01 — additive ecosystem integration

## Metadata

- Branch: `codex/geometric-labs-ecosystem-integration`; PR target: `main`.
- Validation base: `6361440517c4954a3e65b182851510082703c213`; final integration
  commit is the commit containing this report (no self-referential SHA).
- Initial working tree: clean. Result: additive feature branch; no changes to
  upstream repositories or existing tracked mathematical/research files.
- Draft PR: API access blocked by proxy HTTP 403 CONNECT to api.github.com;
  review-ready body in `ecosystem/docs/PR_DESCRIPTION.md`. Feature branch push
  is attempted separately; use its GitHub compare link to create the draft PR.

## Baseline and changes

Baseline `make verify-all`: all five pillars, 40 tests, five vector checks PASS.
Initial separate test-pillars (40) and check-vectors (5 files) PASS; baseline logs
are under `ecosystem/evidence/wave01/baseline-*.log`.

Added ecosystem/manifest, hardened checkout/lock manager, independently imported
loopback harness, protocol compatibility adapter/tests, CI and validation reports.
Outside ecosystem/: root AGENTS.md is the supplied persistent guidance;
`.github/workflows/ecosystem-integration.yml` is independent read-only CI.
Root README/Makefile/existing CI, src/, verification/, docs/ and golden vectors
retain their exact baseline bytes (automated SHA-256 preservation test).
Candidate .pyc, Docker, devcontainer and deployment profiles were excluded.

Contracts: manifest v1, URL/SHA/manifest-digest lock v1, protocol-compatibility v1,
reference-mesh-report v1, acceptance-report v1. Semantic profiles remain distinct;
no schema promotion or source-fixture migration. Original local fixture profile
label is preserved through an explicit integration alias.

## Exact dependency commits

| Repository | Tested SHA |
|---|---|
| CubiLoom | `9abafa43ce4a2fd61c35e2d05479a706e83118c9` |
| FractalOS-runtime | `e4e1d520631bdcc443428ca6abce719082f5dd02` |
| Kernel-Registry | `c94efcd43f690fadce8b4be33126bdb699dadbde` |
| Manifold-Projection | `32a8bed5ce5a9ef4409ee9150f6f9911c3fa3c6d` |
| PolyShard-Agent | `094c2856abaac02cdbef64c848fccea6e13cb95f` |
| Polycentric-Orchestrator | `bc0bbad6d28ebc54dee36b440be2b1db92898805` |
| SHD-CCP-core | `154685b2cc65ed5120e36ad733c03f550760a09b` |

## Evidence table

| Command / fixture | Result | Evidence |
|---|---|---|
| make verify-all | PASS: five pillars, 40 tests, 5 files | evidence/wave01/baseline.log |
| make test-pillars | PASS: 40 tests | evidence/wave01/pillars.log |
| make check-vectors | PASS: 5 byte-identical files; no generation performed | evidence/wave01/vectors.log |
| make -C ecosystem test | PASS: 20 tests (6 candidate + 14 new) | evidence/wave01/ecosystem-unit.log |
| make -C ecosystem geometry | PASS: unchanged baseline | evidence/wave01/geometry.log |
| make -C ecosystem integration | PASS: 4 tests against independent pinned clones | evidence/wave01/integration.log |
| protocol compatibility | PASS structural: 183 C/Python/local packets; semantics remain incompatible | evidence/wave01/protocol-compatibility.json |
| make -C ecosystem demo | PASS: 3 perspectives, exact TQF 576; 11 HTTP rejection fixtures | evidence/wave01/reference-mesh.json |
| doctor/sync-repeat/lock | PASS: 7 clean clones; existing refs unchanged | evidence/wave01/{doctor,sync-repeat,check-lock}.log |
| lock failure injection | PASS: dirty/unknown/origin/symlink/SHA/schema/URL rejection, pinned restoration, idempotence | ecosystem-unit.log |
| original-file preservation | PASS: all original tracked SHA-256 digests match | tests/test_protocol_profiles.py |

Machine-readable aggregate: `ecosystem/evidence/wave01/acceptance.json`.
Total unique unittest methods: existing 40 + ecosystem offline 20 + integration 4
= **64**. Repeated baseline commands are not additional unique tests. Protocol
packet cases and 11 negative HTTP fixtures are subchecks, not extra test methods.

## Safety and pending work

- Implemented/tested: pinned dev environment, independent imports, structural
  conformance, local semantic fail-closed adapter, reference HTTP integration.
- Not production-ready: HMAC/HTTP and replay counters are development-only and
  in-memory. Simulated common clock/world frame, not real remote calibration.
- Semantic negotiation is not implemented in upstream handshake; current adapter
  reports/validates integration profiles without claiming transport upgrades.
- Expired frame certs, durable replay, source-payload immutability and uncertain
  malformed-event hardening need owning-repo contracts/tests in later PRs.
- CubiLoom causal SQLite storage and replica anti-entropy are not implemented.
- FractalOS is an ABI/design scaffold; H100, Loihi2, QEMU and actual CPU32 are
  unrun. Python 3.12 tested locally; 3.10 CI configured, not locally executed.
- No production secrets, Firebase, RAG export, deployments, auto-merge or force push.

Next wave: separate SHD-CCP profile/handshake RFC and CubiLoom SQLite append/replay
PRs, preserving current fallback. Normative form migration and production access
require explicit approval; no such approval is requested for this additive PR.
