# BioChain AI — Eight-Repository Polycentric Ecosystem Architecture

**Status:** architectural specification / development environment overlay v1.0, 2026-10-18. Not a security audit, OS release, verified compression breakthrough or hardware acceleration benchmark.

## A. Definitive identities and ownership

**BioChain AI** is the company and GitHub organization. The seven core repositories are components of a distributed system and own their respective source code. **Geometric-Labs is the eighth repository**, a research and integration control point whose pre-existing purpose is exact-arithmetic Hurwitz/quaternion and spatial calibration verification. That purpose is preserved and expanded with compatibility, federated testing, development environments and release-lock management.

`BioChainAI/BioChain-AI` already exists as a distinct BioMesh/Firebase product. Its Firebase data, keys, rules, and governance are NOT assumed to be part of the Polycentric ecosystem. Treat it as a **separate, optional consumer**: no silent replication, no shared production credentials and no import of unrelated Owl Academy resources.

| Repository | API products | Data ownership | May NOT do |
|---|---|---|---|
| `SHD-CCP-core` | Einstein Tile v1, exact quadrance/TQF, two-u32 codec, language bindings, golden vectors | Protocol and test vectors | Perform governance, device trust, or automatic authorization |
| `Kernel-Registry` | Versioned layout manifests, signed approval metadata, certification decisions | Ontology and certification records | Allow an agent to self-certify or mutate fixed Einstein Tile bits |
| `CubiLoom` | WarpGrid cubic address, DeltaWeft event DAG, ChronoShuttle handshake, LoomLedger storage, SealThread attestation sidecar | Federated event replication and projection references | Require global synchronous time, own private agent RAG, use quaternion product as a signature |
| `PolyShard-Agent` | PolySpindle runtime, RAG/AI-DNA manifests, signed observation envelope, local clock and frame ids | Local source documents, model secrets, policies | Leak private RAG by default, accept arbitrary remote tool privileges |
| `Polycentric-Orchestrator` | Federation membership, admission, policy, certified frame transforms, Mind's Eye scene snapshots | Derived perspective index, coordination log, human approval workflows | Rewrite source observations, equate geometric consensus with factual truth |
| `Manifold-Projection` | CPU projection oracle, shader/render adapters, voxel LOD, optional GPU tile operators | Derived views and reproducible render metadata | Treat shader floating-point output as geometric/security proof |
| `FractalOS-runtime` | Hardware dispatch ABI, IPC, scheduling, CPU32/CPU64, CUDA SM90/Loihi adapters, QEMU OS track | HAL and execution runtime | Embed LLM governance in privileged OS code |
| `Geometric-Labs` | Conformance harness, multi-repo development environments, integration tests, CI gates, locked ecosystem bill of materials | Test reports, compatibility locks, simulations | Fork product logic into shadow copies of upstream projects |

## B. System planes and dependence

```text
    Agent side (PolyShard-Agent + PolySpindle)      Control side (Polycentric-Orchestrator)
       private RAG / AI DNA / local policy             governance / Mind's Eye snapshots
          | evidence-filtered observations                        ^
          v                                                       |
  SHD-CCP-core canonical tiles                 Manifold-Projection projected view
          |                                                       ^
          v                                                       |
  CubiLoom  <--- ChronoShuttle + SealThread ---> CubiLoom replicas and scene event DAG
           (asynchronous, source-stamped, versioned, uncertainty annotated)
              ^                            ^
              |                            |
           Kernel-Registry            FractalOS-runtime adapters
           verified codecs            hosted CPU/GPU/Loihi/QEMU
                         \            /
                     Geometric-Labs
              conformance + integration + release locks
```

Dependency rule: data source --> core contracts; service --> fabric client and projection API where needed; kernel-registry depends on core protocol definitions, not on agent policy; hardware backends execute typed jobs but cannot rewrite canonical packet or governance policy.

**Data plane:** authenticated canonical tile plus separately serialized, versioned envelope. **Control plane:** authority, federation negotiation, registry roots, clock/frame epochs, quotas, privacy purpose. **Memory plane:** append-only causal observations, evidence hashes, optional AI-DNA manifests. **Projection plane:** reproducible scene snapshots / non-authoritative shader display. **Certification plane:** mathematical claims vs implementation tests vs security reviews vs deployment authorization.

## C. CubiLoom model

**WarpGrid:** dyadic cubic lattice addressing and frame registry. Frame transforms have signed provenance, validity intervals, error/uncertainty metadata, and replayable versions. Invariant computations such as exact integer quadrance and TQF compare frames only after an accepted transform or when using actual transform-independent invariants.

**DeltaWeft:** a sequence of immutable events containing `{event_hash, author, stream_id, sequence, prev_hash, parents[], frame_id, clock_domain, packet_refs, semantic_claim, evidence_ref}`. Quaternion deltas are ordered and sign conventions fixed. Ordered aggregate products generally do not preserve their constituent histories; fine-detail reconstruction is permitted only with retained residuals or the original fine chain.

**ChronoShuttle:** network handshake negotiates compatible Einstein Tile version/form, certified kernel profile, nonces, keys and purposes, frame calibration, clock quality (offset, drift, error bound), and event causal heads. Prefer UTC+monotonic clocks with measured error and an optional 40-Hz geometric phase index for windowing. A 40-Hz phase is not proof of wall-time agreement or instantaneous non-local signaling.

**LoomLedger:** append-only content-hash DAG indexed by tenant/stream/clock/frame. Causal ordering per-author, vector/hybrid logical timestamps for conflict handling, duplicate suppression, anti-entropy Merkle range comparison. Local writes remain possible offline; remote reads may be stale. Global convergence is conditional on eventual connectivity, matching policy and reconciliation—not an absolute consistency promise.

**SealThread:** separately authenticated, canonical sidecar record bound to a stream root / tile byte hash and explicit scope. Compose `BaseThread` (structural), `TraceThread` (cryptographic provenance), `CalThread` (unit/reference/uncertainty/expiry), `GovernThread` (consent, policy, delegation) and `SecureThread` (transport encryption and anti-replay). Cryptographic assurance must not rely on CRC32, the 8-bit South Halo, a quaternion closure, or a mathematical coherence score.

**Trust domains:** PolyShard identity; local user/tenant; CubiLoom replica operator; Polycentric orchestrator; registry issuer; independent calibration authority; GPU/Loihi worker; external BioMesh. The default policy is **no central access to agent-local RAG** without scoped explicit disclosure.

## D. Core end-to-end contract

1. Agent derives an observation, filters local RAG content, references AI-DNA manifests and evidence, and canonicalizes an Einstein Tile.
2. Agent records private original event + optional sensor calibration and signs a transport envelope over canonical bytes and dependencies.
3. ChronoShuttle verifies identity, nonce/replay history, protocol/form compatibility, clock uncertainty and frame declarations. Missing calibration is labeled unresolved, not guessed.
4. CubiLoom accepts authorized immutable observations, returns content hash + causal receipt; partitioned agents queue until reconnect.
5. Kernel-Registry checks selected layout/transform certificate and independent approval state; pass/fail never automatically grants governance authority.
6. Orchestrator evaluates purpose-bound policy, transforms coordinates with authorized calibration, retains contradictory observations and computes exact geometric invariants where representable.
7. Manifold-Projection builds a versioned scene and renders non-authoritative shader tiles. CPU exact reference path certifies only the declared mathematics.
8. Orchestrator offers scene snapshots and proposals. Consequential actions require separately granted capability and (where specified) human approval.

## E. Relative-time handshake draft (version 2 target)

Canonical Einstein Tile bytes are fixed to versioned protocol; the envelope is independent:

```json
{
  "handshake_version": 2,
  "agent_id": "polyshard:example",
  "nonce": "base64-cryptographically-random",
  "tile_protocols": ["SHDCCP-EINSTEIN-1"],
  "certified_kernel_digests": ["sha256:..."],
  "clock": {"domain": "node-monotonic-1", "epoch": "e42", "uncertainty_ns": 500000},
  "geometry": {"frame_id": "sensor-A", "calibration_digest": "sha256:..."},
  "causal_heads": ["sha256:..."],
  "requested_scopes": ["observation.write"],
  "authentication": {"method": "mutual-authenticated-channel-and-signed-proof"}
}
```

This is a *contract sketch*, not a deployed authenticated protocol. Finalize nonce exchange and transcript binding, clock offset estimation, canonical encoding, replay/expiry storage, key identity/rotation, and failure response taxonomy before network exposure.

## F. Deployment topologies

- **`math-reference`**: existing exact reference suites and cross-language byte vectors, no services or network needed.
- **`federation-reference`**: three agent instances and one localhost orchestrator, real four-repo imports. No CubiLoom implementation presumed.
- **`federation-fabric`**: three CubiLoom replicas and regional orchestrators with simulated partition/clock skew/conflicting perspective, when database engine exists.
- **`gpu-hopper`**: CUDA SM90 TMA staging, DSMEM cluster-limited cooperation, bounded buffers, CPU exact-check baseline. Hardware-dependent.
- **`neuromorphic`**: Lava Process graph + host sidecar encode/decode; not direct u64-on-spike transport. Hardware/SDK-dependent.
- **`os-emulation`**: QEMU x86-64 microkernel then i686; hosted service ABI precedes bare-metal driver work.
- **`legacy-biomesh`**: opt-in local Firebase emulator or isolated adapter, separate from Polycentric membership.

## G. Multi-language interoperability

`SHD-CCP-core` holds golden vectors. Match wire output on C11 (including two-limb u32), Rust, Python, C#, TypeScript (BigInt/two-u32), and device/reference adapters. A 32-bit processor still emits the same eight-byte logical packet. Do not assume WebGPU native 64-bit integers. Service APIs use explicit versioned typed envelope/protobuf/CBOR *after* canonicalization and compatibility negotiation. Never independently redefine tile bit ranges inside each repository.

## H. Release promotion

For each version pair: check bit-identical codec vectors, type and schema gates, SHD-CCP registration rules, replay and causal convergence, clock uncertainty and calibration quarantine, privacy/consent checks, output parity for exact CPU math, shader-is-not-authority separation, and hardware-specific benchmark reproducibility. Geometric-Labs writes provenance-attached test reports and a reviewed SHA lock; upstream repositories publish their independently signed releases. Test suite success is **implementation evidence**, not a theorem or security certification.
