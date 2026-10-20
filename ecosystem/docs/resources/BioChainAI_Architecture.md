# BioChain AI — Polycentric Fractal Computing Architecture
## Cubic SHD-CCP • Distributed PolyShard Agents • Polycentric Orchestrator • Manifold Mind's Eye

**Design revision:** 0.1.0 | **Date:** 2026-10-18 | **Maturity:** proposed end-to-end architecture + locally runnable reference scaffold, NOT a production autonomous system, bootable OS, certified security implementation, or hardware-validated H100/Loihi2 accelerator.

**Central design thesis.** Build a network of autonomous, separately governed **PolyShard Agents** that retain their local data, models, retrieval systems, and optionally AI-DNA reconstruction manifests. An independently deployable **Polycentric Orchestrator** admits purpose-bound, authenticated 64-bit SHD-CCP observations; registers their spatial and temporal frames; preserves multiple views; performs exact geometric checks and provenance replay; and projects a shared cubic scene into a permissioned **Mind's Eye** visualization/compute system. **FractalOS** provides the portable compute/OS substrate, not the semantic authority. The **kernel ontology** certifies codec layouts and compute modules separately from governance policies.

## 0. Terms and physically important boundaries

- **PolyShard Agent:** a process or node with sovereign local RAG/LLM, sensors, policies, SHD-CCP encoder, timeline and an AI-DNA content-addressed manifest ledger. It can act locally within its authority; only selected claims cross the network.
- **Polycentric Orchestrator:** centralized coordination and shared-perspective indexing *for a federation*, not owner of all source memory. Hierarchical regional orchestrators and replication are allowed; no fundamental single global machine is required.
- **Mind's Eye:** an explicitly computed, versioned **scene graph and memory index** of observations, frame transforms, uncertainty, contradictory claims, cubic/toroidal relationships and shader projections. It is a software visualization and planning abstraction, not a literally shared subjective visual field.
- **Non-local handshake:** distant agents reach a shared reference using authenticated network messages, invariants, calibration anchors, versioned codecs and clock windows. **This does not claim faster-than-light signaling, quantum nonlocal communication, or spatial alignment without calibration.**
- **Geometric clock:** an optional exact 40-Hz phase/closure index based on the research time engine. It does not replace UTC/PTP/NTP; absolute timebase, monotonic sequencing and uncertainty must be negotiated independently.
- **Fractal folding:** hierarchical operator DAG with fixed local invariants. Some transforms are exact (bit parity, integer TQF, ordered quaternion block products within their number domain); others are lossy or only interpolated (quantization, shader projection, SLERP without fine residuals, embedding seeds). The architecture never claims arbitrary information can be compressed losslessly below entropy limits.
- **Kernel:** distinguish OS microkernel, GPU compute kernel, SHD-CCP tile layout, and ontology-certified transform. They have different authorities, threat models and update mechanisms.

## 1. Topology: control, data and visualization planes

```text
┌────────────────────── POLYSHARD SITE A ────────────────────────┐
│ Local user & consent │ Local RAG/LLM │ AI-DNA seed ledger     │
│ Sensors/skills       │ Privacy filter│ SHD-CCP packetizer    │
│ Local clock+frames   │ Agent manager │ local spatial cache   │
└─────────────────────────┬──────────────────────────────────────┘
                          │ signed, scoped, versioned packets
┌────────────────────── POLYSHARD SITES B...N ──────────────────┐
│ Independent agents; different machines, privileges & clocks   │
└─────────────────────────┬──────────────────────────────────────┘
                          │ mutual-auth encrypted transport
                          ▼
┌───────────── POLYCENTRIC ORCHESTRATOR REPOSITORY ──────────────┐
│ Ingress / federated identity / rate limits / replay windows   │
│ Consent + authority policy / calibrated frames / clock broker │
│ SHD-CCP schema + proof/ontology registry verifier             │
│ Multi-perspective Event-Relation Graph + provenance ledger    │
│                                                               │
│  ┌────────── Geometric computation plane ──────────────────┐  │
│  │ exact TQF & quadrance │ voxel address │ folding DAG      │  │
│  │ quaternion aggregation │ 12-engine parity │ confidence   │  │
│  │ ambiguity / contradictions / human review gates         │  │
│  └───────────────────────────────────────────────────────────┘ │
│  ┌────────── MIND'S EYE / CENTRAL MANIFOLD MEMORY ─────────┐ │
│  │ Scene snapshots / anchors / time windows / signed roots  │ │
│  │ Cubic lattice LOD / projection graph / query services   │ │
│  │ WGSL/GLSL/CUDA shader submission to trusted device HAL  │ │
│  └───────────────────────────────────────────────────────────┘ │
└───────────────────────────┬────────────────────────────────────┘
                            │ certified compute backend interface
             ┌──────────────┼───────────────┬────────────────┐
             ▼              ▼               ▼                ▼
       CPU32/CPU64     CUDA SM90       Lava/Loihi2       WebGPU/Vulkan
       exact TQF       TMA/DSMEM       spike adapters    projected scene
             └──────────────┴───────────────┴────────────────┘
```

Two-level deployability is central: (a) the **minimal hosted demonstration** has three agents and one localhost orchestrator, and (b) the **target federation** has signed identities, regional brokers, decentralized private stores, optional edge accelerators and auditable governance. The trusted OS code stays small, while the highly changeable AI, governance, ontology and geometry logic executes in isolated user services.

## 2. Separate, independently versioned repositories

| Repository / ownership | Main responsibilities | Languages | Release independence |
|---|---|---|---|
| `biochain-shdccp-core` — protocol team | Canonical Einstein Tile, 32/64-bit codecs, signed envelope format, schema, exact geometry, cross-language vectors | C11, Rust, Python, C#, TypeScript | Semantic-versioned ABI/wire standard |
| `biochain-polyshard-agent` — agent team | Local LLM inference bridge, SQLite/vector RAG, local skills, AI-DNA manifest/seed ledger, spatial observations, consent egress, local clock | Python now; Rust core later; TS UI | Distributed deployment per agent |
| `biochain-polycentric-orchestrator` — orchestration team | Federation admission, scheduling, policy, calibration authority, event provenance, scene DAG, Mind's Eye memory, regional consensus/human review | Python now, Rust or Go services later | Separate deployment and admin domain |
| `biochain-manifold-projection` — geometry/render team | CPU scene projection, cubic voxel tiling, shader compilation, WGSL/GLSL view, GPU spatial-tile kernels | Python, WGSL, GLSL, CUDA C++ | GPU/renderer updates cannot change protocol |
| `biochain-kernel-registry` — standardization team | Ontology incubator, form manifest linting, mathematical status, build attestation, review approvals, revocations | JSON, Python, CI, eventually formal methods | Independent certification root |
| `biochain-fractalos-runtime` — systems team | Microkernel boot track, user service IPC, hardware abstraction, scheduling, CPU/GPU/Loihi backends, memory transport | C, Rust, CUDA, architecture assembly | Hardware-specific builds and drivers |

**Repository governance.** The orchestrator must never be checked into an agent repo as a hidden central daemon. Shared contracts and golden vectors are published from `biochain-shdccp-core`; orchestrator and agents pin the same version and negotiate it explicitly. Dependencies are one-directional: agent and orchestrator depend on protocol + projection interfaces; the protocol does not depend on them. The full workspace in this ZIP is a development aggregation of separable repositories, not a single forced deployment.

### Main components inside the Polycentric Orchestrator repository

| Component | Input → output | Implementation invariant |
|---|---|---|
| Federation Registry | signed agent identity → permitted scopes | explicit revocation, rotation, device/agent identity separation |
| Handshake Broker | nonce, protocol, time, frame → negotiated session | no guessing of legacy word layout; anti-replay persistence |
| Purpose/Consent Policy | event + declared purpose → allow/quarantine | no expanding authority from LLM-suggested content |
| Frame Calibration Registry | local frame, anchor evidence → world frame transform | calibration requires authorized evidence, version and uncertainty |
| Geometric Governance | accepted claims → candidate alignments, proofs, disagreements | exact invariant ≠ truthful claims or permission to act |
| Fractal Scheduler | operator DAG → CPU/GPU/event backend tasks | deterministic CPU correctness oracle; deadlines/quotas |
| Central Manifold Memory | append events → content-addressed scene snapshots | retain distinct perspectives and source provenance |
| Intrinsic Clock Broker | time offsets+uncertainty+tick → phase windows | no false equivalence of 40-Hz phase with wall-time synchronization |
| Shader/Projection Service | authorized scene → device shader and raster output | no untrusted compiled shader in privileged OS |
| Action Governance | proposals+evidence+policy → human-approved action receipt | no automatic real-world interventions by default |

## 3. SHD-CCP canonical Einstein Tile (unchanged fixed bit positions)

The later research uses the **Einstein Tile**: 8 octets big-endian; `bit0` denotes the least significant bit of the 64-bit logical value. On a 32-bit CPU a tile is `(u32 hi, u32 lo)` and is serialized as exactly eight big-endian octets. The top byte (South Halo) is a fast filter, **not** a signature or MAC.

```text
 63        61 60    58 57   56 55          48 47    44 43     40
 ┌───────────┬────────┬───────┬─────────────┬────────┬─────────┐
 │ cycle[3]  │wheel[3]│str[2] │  gate[8]    │step[4] │form[4]  │
 └───────────┴────────┴───────┴─────────────┴────────┴─────────┘
 39       36 35       32 31                                     0
 ┌──────────┬────────────┬───────────────────────────────────────┐
 │stream[4] │ scale[4]   │  32-bit form-dependent core           │
 └──────────┴────────────┴───────────────────────────────────────┘
```

Fields: `cycle_step 61..63`, `wheel_unit 58..60`, `structure 56..57`, `gate 48..55`, `step_index 44..47`, `form_id 40..43`, `stream_slot 36..39`, `scale 32..35`, `core 0..31`. Form `1` denotes exact doubled Hurwitz core subject to the source's canonical constraints; Form `3` is a raw IEEE-754 binary32 value; Form `15` supports separately identified external codex extension. Forms 4–14 have their research-defined shape semantics.

**A tile alone is insufficient for distributed truth/security.** The separate transport envelope carries `{protocol_id, schema_version, tenant, agent identity, sequence, timestamp, clock uncertainty, frame reference, evidence hash, registry manifest hash, content digest, authentication signature, optional loss/residual sidecar}`. Never place all of these inside Form-ID bits or claim the South Halo provides cryptography.

Legacy `ZONE/TYPE/SEQ/PAYLOAD` and `FP8*4+metadata` designs receive named gateways outside the canonical data plane. Unknown or incompatible layouts must be rejected, not guessed by inspecting upper bits. Envelope signing covers the exact canonical serialization and all scope/time/frame metadata.

### Three streams and the implied fourth

Define three independently labeled packet streams for a chosen transform: `primary`, `inverse` and `phase_shifted`. A fourth may be **derived** by a specified XOR parity or noncommutative quaternion closure. These are **different operations**: XOR parity of three full 64-bit words allows one missing word to be recovered; quaternion closure `H4=(H1*H2*H3)^(-1)` recovers one missing *aggregate quaternion holonomy* under precise group assumptions, not arbitrary complete agent data. Do not conflate XOR telemetry redundancy with source-history reconstruction.

## 4. Spatial-temporal geometric handshake

**Handshake stages:**

1. **Identity and protocol:** Agent proves its registered key, exchanges signed challenges, negotiates Einstein Tile major version and current signed ontology root.
2. **Purpose and privacy:** Agent declares which observation types, RAG-derived statements, personal data and spatial coordinates may leave its private store. The orchestrator returns the permitted, expiring capability.
3. **Time negotiation:** Exchange event UTC, monotonic counter, quality/uncertainty, clock-offset estimate, and a 40-Hz geometric phase epoch. `tick=floor((t-t0)/25ms)`, `step=tick mod 8`, `phase=tick mod 3`; joint cycles can be modeled on `lcm(8,3)=24` steps. *This periodic index is an application convention, not a measured physical clock guarantee.*
4. **Reference-frame binding:** Agent identifies local lattice, unit scale, calibration anchors, handedness, versioned transform and covariance/error. The orchestrator admits only recognized approved transform references (the working demo supports integer isometries and translations).
5. **SHD-CCP observation:** Encoder writes 64-bit tile and sidecar. Optional `Triple Quad Formula` evidence compares the shared triangles or tetrahedra when agents have corresponding points.
6. **Integrity and provenance:** Verify signature, replay counter, manifest hash, evidence digest and content root before adding an immutable event. Store rejected attempts in a separate quarantine/audit system.
7. **Fusion without collapsing views:** Transform individual coordinates into a shared frame, check temporal overlap, compute exact quadrances and TQF, record contradictions and confidence per source. Evidence remains attributed; shared spatial geometry does not imply agreement on semantics.
8. **Mind's Eye projection:** Emit a permissioned scene snapshot with voxel coordinates, clocks, uncertainties, evidence pointers and potential shader output. Agents receive only the scene subsets authorized by the purpose policy.

### Exact Triple Quad Formula (TQF) and cubic spatial references

For three integer-coordinate points `P1,P2,P3` after frame calibration, let `a=|P1-P2|²`, `b=|P2-P3|²`, and `c=|P1-P3|²`. Define

`A16 = 4ab - (a+b-c)² = 16 · (Euclidean triangle area)²`.

This can be evaluated with integers (arbitrary precision for large inputs; bounded integer arithmetic on device backends only with overflow proofs). Example: points `(0,0,0)`, `(4,0,0)`, `(0,3,0)` yield `a=16`, `b=25`, `c=9`, and `A16=576`. Their area is 6 square lattice units. Relative quadrances are invariant under common rigid rotations/translations; if each agent supplies data in a different frame, a **calibrated common reference or independently verified correspondences** is required first. In practical deployment, collect at least 3 noncollinear correspondences for 3D rotation and translation (and validate handedness, scale and uncertainties).

A cubic node is addressed as `(floor(x/edge), floor(y/edge), floor(z/edge))` with immutable frame ID and `edge`/scale identifier. Higher fractal levels repeatedly group 2×2×2 or 4×4×4 children under a parent Morton/octree-style address; **the parent is a lossy LOD summary unless it also stores children and residuals.** Preserve original exact coordinate records and source links for reconstruction.

## 5. Central Manifold Memory — the Mind's Eye

The central manifold is **not** one giant mutable global tensor. Its canonical representation is an append-only, time-addressable **Event–Relation Graph** with materialized geometric views:

- **Entity:** observed object, agent, shape, voxel, time segment, anchored frame, proof, codex manifest or AI-DNA seed.
- **Event:** provenance-bound observation/action/update; idempotent event ID; agent sequence; clock uncertainty; confidence and consent.
- **Relation:** `observed_from`, `corresponds_to`, `contradicts`, `derived_by`, `aligned_with`, `authorizes`, `revoked_by`, `parent_voxel`, `same_physical_anchor_as`.
- **Projection:** view-specific scene snapshots; GPU buffers + shader results; TQF/quaternion summaries; uncertainty cones.
- **History:** segmented WAL and periodically authenticated content-addressed checkpoint roots; object storage keeps residuals and provenance as required.

Persist two complementary representations: (1) **exact source and event DAG** for deterministic replay and auditing, and (2) **compressed manifold indices** for fast 3D/time queries. A scene projection is disposable: it can be regenerated from input events and algorithm/version hashes. Do not delete source data based solely on a pleasing shader visualization or a coherent score.

### Multi-perspective geometric governance

An agent's assertion is an **attributed claim**, not a vote about objective reality. A policy and evidence broker separately decide: whether it may be shared, whether the signatures and frames are valid, whether its measurement can be merged mathematically, whether a downstream human action is authorized, and whether other perspectives disagree. Maintain per-source uncertainty and persistent contradictions. Use W3C PROV concepts (`Entity`, `Activity`, `Agent`, `used`, `wasGeneratedBy`, `wasAssociatedWith`) in the exported provenance view; W3C PROV is an interoperability model, not proof that an underlying claim is truthful.

### 12-engine memory option

From the uploaded *Memory in the Twelve-Engine Hierarchy*, build a research-mode 3×(3 data holonomies + 1 implied-fourth holonomy) hierarchy. At the defined group level, one erased holonomy per group can be reconstructed and 25% of slots are redundant; this does **not** recover the individual original histories from an aggregate product. An optional 13th parity engine has a specific extra failure-case benefit, not arbitrary 2-erasure protection. Keep that subsystem separate from the basic 3+1 XOR parity of raw 64-bit packet words.

From the *Torsional Markov Memory-Offload Pump*, create an ordered 720→72→10 quaternion delta reduction: every 10 fine deltas form one coarse ordered product, then each of the 10 final blocks has 7 or 8 middle frames. The inverse middle layer preserves the aggregate rotation, while a SLERP lift produces interpolated fine rotations. Lossless recovery of discarded original fine deltas requires retained residuals; the paper itself labels global reconstruction behavior a design boundary.

## 6. PolyShard Agent internal layout

A PolyShard must remain useful with no coordinator connection. Proposed internal services:

```text
agentd                   capability and user policy supervisor
runtime/llm             local/remote LLM adapters, inference driver, prompt sandbox
memory/rag              SQLite FTS/vector index, encrypted documents, access control
memory/ai_dna           procedural seed registry, decoder versions, optional residuals
memory/eventlog         agent-local durable event+signature history
spatial/sensors         device adapters, pose frames, calibration, state estimator
spatial/shdccp          canonical 64-bit packet sender, triple stream and tile batching
spatial/clock           monotonic+UTC quality, geometric phase, epoch correlation
net/federation          authenticated handshake, reconnect, ack, dedupe
policy                  purpose, consent, retention, revocation, data minimization
apps/skills             LLM tools, RAG retrieval, task execution, human confirmation
```

**Legacy LLM compatibility:** Provide a stable `generate(messages, retrieved_context, tools, policy)` adapter. Do not require an LLM at all for raw telemetry or exact TQF: deterministic transforms should be deterministic. Local RAG never exits the agent by default; only a derived evidence statement, source digest and authorized citation reference may be shared. Embedding vectors, private documents and user text require separate explicit egress scopes.

### AI DNA and quaternion chain of custody

“AI DNA” is a design term for a compact, reproducible **reconstruction manifest**: `{model_digest, codec_id, seed_kind, seed_digest, decoder_digest, dependency_hashes, residual_digest, error_budget, version, purpose, privacy_class}`. A procedural seed can be extremely small **only when the receiver already has the algorithm and required model/dictionary**. A pointer can represent a large object by its hash only if the receiver can retrieve that object. Quantized embedding memory is lossy according to its stated error budget. These distinctions are mandatory for honest compression measurements.

Link AI-DNA manifests via append-only content-addressed hash edges. Quaternion transforms can annotate each block's exact or approximate spatial state, but quaternion multiplication is not a replacement for cryptographic hashes, digital signatures or decentralized consensus. A blockchain/replication layer is an **optional** distributed commitment mechanism, not a requirement to read local AI DNA.

## 7. Shader, fractal tiling and accelerator architecture

**GPU shader purpose:** project geometric/semantic state into a visual and GPU-computable manifold representation. Shader colors, opacity or clustering are display semantics, never evidence attestation. Distinct pipelines are needed for exact computation and real-time rendering.

| Execution strategy | Workloads | Restrictions |
|---|---|---|
| CPU scalar / two-limb 32-bit | reference Tile codec, exact TQF, policy, hashing, data structures | default correctness oracle on all architectures |
| CPU SIMD (AVX2/AVX-512/NEON/RVV) | batch tile decode, Morton indexing, sampled trefoil and quaternion normalization | vector math and precision specified per operator; portable fallback |
| CUDA H100 / SM90, Hopper | tensored batch projection, tile neighbor gather, 3D cubic reduction, matrix operators | TMA stages multidimensional global↔shared data; DSMEM shares blocks **within a thread-block cluster**; explicit cluster synchronization; cannot authenticate data implicitly |
| WGSL/WebGPU | interactive Mind's Eye browser projection, voxel LOD, ray/point shaders | no assumption of native `u64` WebGPU shader support; encode as 2×u32 or pre-decode |
| GLSL/Vulkan | cross-vendor 3D viewer / GPU compute | hardware features detected; native integer64 only where supported |
| Intel Loihi 2 / Lava | event-driven sensor coordination, sparse event routing, spiking state machine prototypes | host adapters translate 64-bit tile sidecars into event/spike representations; neuromorphic outputs are not exact integer proof or secure packet decoding |
| SYCL / HIP / FPGA | future broad compute interoperability | conformance and performance must be validated independently |
| network workers | hierarchical batch folding, RAG inference, geospatial memory shards | distributed consistency is not hardware shared memory; data locality and privacy govern placement |

### H100 split-system design

1. **Ingress/identity lane on CPU:** parse, authenticate, authorize and sequence observations before DMA.
2. **Tiling/staging lane:** group tiles by scene, voxel region, operator, and source frame; make contiguous SoA tensor buffers with sizes benefiting TMA. Baseline direct global-memory CUDA kernels first.
3. **SM90 compute lane:** batch geometric transforms with bounded precision and block-cluster scheduling. Use TMA with asynchronous completion/barriers where justified; use DSMEM only inside the participating cluster with correct `cluster.sync()` lifecycle.
4. **Exact certification lane on CPU or proven GPU integer kernels:** re-check sampled/exhaustive invariants as appropriate; never treat FP32 display transforms as proofs.
5. **Merge lane:** append resulting reference hashes and precision/error metadata to the manifold DAG; fallback to CPU if the accelerator fails or is unavailable.

**Loihi 2 layout:** `Tile ingest -> exact host decode -> event binning / quantization -> Lava Process graph -> event-state prediction -> explicit host readback -> timestamped SHD-CCP result envelope`. Preserve a CPU reference model and compare transfer/host overhead, quality, energy and event latency. Device access/SDK availability is not assumed.

## 8. Kernel ontology and agent certification

Keep the original repository lifecycle:

`00_Ontology_Core -> 01_Incubator_Experimental -> 02_Validation_Matrix -> 03_Certified_Standard -> 04_Deprecated_Archive`.

Improve certification with **four independent authorities**: `math_claim_status` ([PROVEN], [HEURISTIC], [OPEN], etc.), `implementation_status` (TESTED/REVIEWED/RELEASED), `security_status` (UNAUDITED/AUDITED), and `deployment_authorization` (HUMAN_APPROVED/REVOKED). No agent self-declaration of “[PROVEN]” can elevate production privileges. A cryptographically signed release manifest should bind bit layout, code digest, proof digest, golden vectors, compiler flags, ABI version, and affected forms. Any change of fixed Einstein Tile positions is a protocol-version change, not a schema hotfix. The included linter demonstrates a small portion of these rules; full proofs/reviews are future work.

## 9. Governance and security model

**Threats:** agent impersonation, replay/rollback, telemetry poisoning, forged calibration frames, malicious RAG content, prompt injection in certified kernel descriptions, tool escalation, fake AI-DNA seeds, model exfiltration, long-lived key theft, GPU shader denial of service, federated timeline skew, majority-of-agents collusion, and forced central shutdown.

**Target controls:** mTLS and asymmetric node/agent identities, signed challenge nonces, rotating session keys, per-tenant key vaults, monotonic anti-replay log persisted durably, quotas and backpressure, signed transforms with calibration residuals, purpose-bound capability tokens, per-field retention labels, encrypted local-at-rest stores, human authorization for consequential acts, signed artifact/SBOM, deterministic reproducible codecs, sandboxed LLM tools and GPU shader validation, alerting and incident revocation. Avoid claiming that CRC32, South Halo or coherence scores provide these controls.

**Central vs polycentric tension:** Treat the orchestrator as the *coordination locus and derived state index*, not ultimate governor of local agents. Agents must be able to reject commands, revoke consent, leave the federation and continue local inference. Multi-orchestrator federation and quorum governance can be implemented above the basic version once authority delegation, reconciliation and partition handling are specified. Agent “consensus” is not statistical evidence that the assertion is correct.

## 10. Runtime and deployment modes

**Mode A — local reference (implemented):** Three Python agents, local SQLite RAG, reference AI-DNA ledger, 64-bit Einstein Tile packets, HTTP loopback handshake, HMAC development signatures, registered integer-isometry frames, exact integer triple-quad, content-addressed append chain and CPU scene projection. This demonstrates contracts, **not secure distributed deployment**.

**Mode B — hosted federation (next):** Rust `ingressd`, durable PostgreSQL/SQLite WAL, per-agent data vault, mTLS QUIC/gRPC streaming, signed registry root, WebGPU viewer, optional model servers, regional broker; deploy in containers or ordinary VMs.

**Mode C — accelerated cluster (later):** GPU worker queues + SM90 kernels on H100 host, Loihi2 event bridge on supported lab nodes, RDMA within explicitly secured domains, backend capability negotiation, per-tenant execution limits and production benchmarks.

**Mode D — bare-metal FractalOS (research track):** QEMU x86-64 then i686, memory protection/IPC/capabilities/process scheduler/interrupts first; agent services and geometry stay unprivileged. ARM64, RV64 and 32-bit embedded support are subsequent. GPU support is via supported host adapters, not an assumed in-kernel CUDA driver.

## 11. End-to-end data contracts and quality gates

Contracts live in `/contracts`: a JSON observation schema, AI-DNA manifest schema, gRPC/protobuf future wire sketch, and backend operator ABI proposal. Production must additionally freeze: signature canonicalization, device attestation, nonce and sequence persistence, signed ontology root, calibration authority schema, privacy retention semantics, object-storage proof format, error budgets, and replay/version migrations.

**Proposed SLOs** (not measured): 100% bit-identical 64-bit codec roundtrip; 100% rejection of fixed-field overwrite attempts in registry structural tests; exact integer TQF parity across CPU32/CPU64; P99 ingress under 100 ms within one region at a defined event rate; scene availability under a chosen quorum and recovery policy; frame calibration error and scene clock uncertainty reported per observation; GPU speedups reported against CPU on equal workload including transfers. High-risk observations must fail closed on identity, clock, policy or frame uncertainty, with quarantine and human-readable reason.

### First build gates (acceptance tests)

| Gate | Work | Acceptance |
|---|---|---|
| G0 (implemented reference) | 3 local agents; Tile decode; HMAC dev mode; registry lint; exact TQF; local HTTP; RAG and AI DNA | demo runs; Python and C codec tests pass; tampering/replay/consent/frame rejections pass |
| G1 | production agent identity, encrypted transport, durable events | replay after restart rejected; reissued keys/revocations enforced; replayable scene state |
| G2 | independent frame registration + sensor uncertainty | 3D transforms/correspondences under measurement error; merge blocked without approved calibration |
| G3 | 12-engine & 720→72→10 memory plugin | exactly recover permitted single holonomy erasure, no false history reconstruction, residual-aware exact/approx reports |
| G4 | shader and Mind's Eye web viewer | scene DAG and GPU rendering parity; viewer never changes source evidence |
| G5 | SM90 and Lava simulation/hardware plugins | measured fallback, accuracy and reproducibility; H100/Loihi results verified on the actual hardware |
| G6 | QEMU kernel + 32-bit ABI | privilege separation, IPC and tile conformance on both x86_64/i686; independent OS vs kernel-layout certification |
| G7 | regional orchestrators / federated policy | partition tolerance design, consent revocation propagation, conflict preservation, audited command authority |

## 12. Research traceability and epistemic status

**Uploaded source mapping:**

- `FRACTAL_PROCESSOR_SHDCCP_IMPLEMENTATION_PLAN.md` provides triple streams, trefoil, CPU SIMD, Rust/host validation, CRC/WAL and GPU offload baseline; its original top-byte crypto interpretation and exact throughput projections need correction/measurement.
- `shd_ccp_kernel_certification_ontology_architecture.md` supplies the four-stage agent lifecycle and ontological families; its example Form-ID position is not the latest Einstein Tile layout and cannot be deployed unchanged.
- `The_Geometric_Engine_of_Time_Fifteen_Lemmas.pdf`, especially §6.1, supplies the canonical 64-bit Einstein Tile and fixed Form IDs; the supplied PDF is rendered/image-based, so authoritative original page images were used in the prior integrated research.
- `Memory in the Twelve-Engine Hierarchy.pdf` supplies the 9-data/3-parity holonomy hierarchy, inverse-tier property and 24-step open synchronization question.
- `The_Torsional_Markov_Memory_Offload_Pump.pdf` supplies 720→72→10 ordered reductions, inverse compensation and restrictions on reconstructing discarded details.
- `The_Geometric_Engine_of_Time_Fokker-Planck_Prime_Sieve_Release.pdf` supplies lattice/Hurwitz/TQF exact operators and describes alignment as a **proposed** AI application, not an established mechanism of agent governance.
- `The_Geometric_Engine_of_Time_Fokker-Planck_Prime_Sieve_Companion.pdf` audits superseded bit fields and the South Halo, warning against treating them as integrity checks.
- `The Geometric Engine of Time A Proposal for a Standardization of the Cubit.pdf` supplies a state-dependent optional acoustic spatial scale and empirical-status tagging; the local cubit is not a universal fixed unit and may not replace SI traceability.
- `FractalOS_SHDCCP_Integrated_Implementation_Framework.md` (previous architecture) resolves wire conflicts, explains exact/approx limits and plans the multi-backend microkernel roadmap. This document layers PolyShard/Polycentric components on top of those constraints.

**Externally established hardware/standards context, not source-research findings:** NVIDIA Hopper Tuning Guide, CUDA programming guide (TMA and DSMEM), Intel Loihi 2/Lava overview, and the W3C PROV data model. Reference URLs are in `docs/REFERENCES.md`.

### Decisions still explicitly open

1. Which identities (individual, organization, device, model clone) may sign an observation? Which identities can approve a physical frame calibration?
2. Does the 40-Hz geometric phase label the event packet itself, a transport schedule, or a device sensor sampling contract? How does the 24-step supercycle relate to actual synchronized hardware?
3. Are raw 64-bit tiles used as semantic **payloads**, spatial indices, or just anchors to larger tensors? This decides compression and information-loss guarantees.
4. Which AI-DNA seed formats are actually reproducible across LLM backends, and which require full weights, adapters or dictionary models? Measurements and patents must distinguish these.
5. What evidence and human approvals are needed before the orchestrator issues a consequential action instead of a scene suggestion?
6. Which world/local frame conventions, uncertainty ellipsoids, timestamps, epoch semantics, retention policies and regional quorum rules form the first ratified release?

**Architecture recommendation:** Freeze the Einstein Tile ABI and frame/clock/consent envelope in a protocol RFC; finish production identity, durable event replay and calibrated local-frame alignment before deploying autonomous governance actions or accelerator-specific optimized kernels. This produces a verifiable engineering system while retaining the geometric research as configurable, auditable operators.
