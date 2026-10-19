# Seven Repository Blueprints — Implementation Contracts

This file proposes *future* internals for the seven existing repositories. It does not assert that these directories are already present. Each repository owns its normative schemas and publishes compatible releases; Geometric-Labs only tests their interfaces.

## 1. SHD-CCP-core — packet and exact mathematics

```text
spec/{einstein-tile-v1,compatibility,form-profiles}/
src/{codec,geometry,fold}/
bindings/{c,rust,python,csharp,typescript}/
tests/{wire-vectors,quadrance,tqf,32bit-crosscheck}/
```

Deliver immutable 8-byte packet core, fixed Form ID at bits 40–43, explicit structure selector, big-endian serialization, two-u32 representation, stable golden vectors, exact integer/rational algorithms, and overflow behavior. No auth decisions encoded in a header byte; no unreviewed encoder version rewrite.

## 2. Kernel-Registry — certification and ontology

```text
00_Ontology_Core/
01_Incubator_Experimental/
02_Validation_Matrix/
03_Certified_Standard/
04_Deprecated_Archive/
src/registry/{linter,publisher,proofs,revocation}/
```

Keep four separate statuses: mathematical status, implementation test status, security review status, and deployment authorization. Enforce compatible Einstein Tile form profiles, review-signature thresholds, revocations, and immutable release identifiers. Registry approval does not authorize an agent's tool actions.

## 3. CubiLoom — independent decentralized geometric database

```text
src/{warpgrid,deltaweft,chronoshuttle,loomledger,sealthread}/
src/storage/{sqlite,postgres,object-store}/
src/replication/{anti-entropy,partition,causal-clock}/
contracts/{append,handshake,attestation,frame}/
tests/{partition,duplicates,replay,clock-skew,consent}/
```

CubiLoom is the system of record for replicated, *authorized* geometric observations. Local agents may publish a filtered projection rather than raw content. Adopt per-author monotonic sequences, immutable parents and causal DAG, eventual authorized convergence and configurable read staleness. Never assume universal clock sync; treat calibration and attestation as evidence with validity intervals and uncertainty.

## 4. PolyShard-Agent — agent autonomy and PolySpindle

```text
src/polyshard/{runtime,llm,rag,aidna,spindle,clock,frame,policy}/
plugins/{inference,retrieval,telemetry,skills}/
tests/{offline,private-rag,authorized-egress,restart-replay}/
```

Separate system prompt from data, apply tools only through narrow capabilities, persist local data under local ownership, and require explicit opt-in for summaries or evidence disclosures. AI-DNA seed manifests identify decoder/model/dictionary and residuals, not arbitrary lossless reconstruction from a short pointer.

## 5. Polycentric-Orchestrator — federated governance and Mind's Eye

```text
src/polycentric/{identity,ingress,policy,clock,calibration,event_graph,
                 scheduler,scenes,review,query,export}/
contracts/{admission,scene-snapshot,frame-transform}/
tests/{admission,multi-perspective,reconciliation,manual-approval}/
```

Own coordination, not source RAG. Store source hash, author, signed frame transform, relative-clock confidence, contradictory claims and audit receipts; issue candidate alignments but not unearned assertions of truth. Agent-governance consent and remote operations require independent authorization.

## 6. Manifold-Projection — evidence-preserving visual and GPU projector

```text
src/{cpu_reference,voxel_lod,scene_serializer}/
shaders/{wgsl,glsl,cuda_sm90}/
backends/{cpu,webgpu,cuda}/
tests/{reference-parity,precision-bounds,render-sandbox}/
```

All float shader paths are derived visualization/computation artifacts, not identity or calibration certifiers. CUDA Hopper TMA stages multidimensional arrays, DSMEM is limited to thread-block clusters, and CPU math remains the exact reference.

## 7. FractalOS-runtime — hardware execution abstraction

```text
kernel/{boot,vm,capabilities,ipc,scheduler}/
interfaces/{compute_job,buffer,device_capabilities}/
backends/{cpu32,cpu64,simd,cuda_sm90,loihi2_lava,fpga_future}/
emulation/{x86_64,i686}/
tests/{abi,determinism,backend-fallback,capability-isolation}/
```

Initially ship hosted dispatch interfaces and an x86-64 QEMU track, not a claim of bootable OS status. Then add i686 and further targets; separate privileged kernel code from sandboxed agent runtime. Loihi 2 integration is event-based via a host conversion/sidecar rather than a claim that raw 64-bit Tiles execute as spikes.

## Conformance contract for Geometric-Labs

Cross-repo integration must test **both success and deliberate failure cases**: wrong protocol version, mismatched Form ID, replayed event, stale calibration, unresolved frame, clock uncertainty exceeded, unapproved kernel, revoked signer, unsigned sidecar, privacy scope violation, numeric overflows, GPU approximate disagreement, fabric partition/rejoin and orphaned causal parent. A green conformance suite is test evidence, not mathematical proof or an independent security audit.
