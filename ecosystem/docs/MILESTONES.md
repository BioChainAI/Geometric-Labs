# Implementable engineering roadmap and acceptance gates

## R0 — freeze ownership and contracts
- Every repository uses the actual existing BioChainAI slug. Seven repos are independent; Geometric-Labs owns integration only.
- Central Einstein Tile documentation, field positions, variants and tested canonical bytes in SHD-CCP-core.
- Geometric-Labs manifests dependencies and exact commit SHA locks. No source vendoring.

## R1 — repeatable localhost federation
- 3 PolyShard Agents and 1 Polycentric Orchestrator exchange canonical tiles via existing reference APIs; exact TQF 576 on the sample 3-4-5 triangle.
- Launch from checkout of actual four core repos via `make -C ecosystem demo`; master math suite remains intact.
- Replay and malformed tile tests expanded in agent and orchestrator repos; deterministic local fixtures.

## R2 — CubiLoom replicated event store
- Implement ChronoShuttle authenticated contract, WarpGrid frames, DeltaWeft causal DAG, LoomLedger roots.
- Offline write queue, reconnect anti-entropy, partition/conflict test with 3 replicas and 2 orchestrators; explicit consistency contract.
- Preserve source owner, parent edges, clock uncertainty, frame versions and revoked consent behavior.

## R3 — SealThread and ontology certification
- Canonical signature/envelope, nonce transcript binding, expiry/replay DB, cert issuer + revocation, security review. No South Halo/CRC authenticity claims.
- Distinct mathematical, implementation, security, and deployment statuses; independent review keys.
- CalThread includes uncertainty budgets and calibration authority; impossible transforms rejected or quarantined.

## R4 — Polycentric Mind's Eye and real local RAG
- Tenant-isolated RAG and AI-DNA manifest import/export; remote shared summaries only by declared scope.
- Scene graph with conflicting agent perspectives, calibrated frame transforms, snapshot hashes and interactive viewer.
- Geometry certified separately from rendering and semantic authority.

## R5 — hardware acceleration
- CPU scalar reference and reproducibility baseline; CPU SIMD then CUDA SM90 TMA/DSMEM only where hardware supports it.
- WGSL two-u32 visualization and semantic shader metadata; memory-transfer-inclusive benchmarking; no unverified speed claims.

## R6 — neuromorphic event adapter
- Define mapping between canonical tile sidecar and Lava/Loihi spike event state; compare accuracy/energy/latency including host overhead.
- No requirement for direct 64-bit spike encoding on chip.

## R7 — FractalOS bare-metal and distributed deployment
- QEMU x86-64, memory protection, capabilities, IPC, timer/interrupts, process isolation; later i686 architecture-specific boot.
- Hosted agent system preserved as reference deployment; no mandatory bare-metal OS before product iteration.

## Product bridge — BioChain-AI / BioMesh
- Design explicit opt-in adapter only after consent and ownership mapping; Firebase-emulator integration tests and dedicated access identities.
- Do not silently merge BioMesh transfer logs into Polycentric observation DAG or store plaintext shared secrets.
