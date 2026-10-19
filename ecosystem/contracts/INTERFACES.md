# Cross-Repository Contract Matrix (draft v1)

| Producer | Consumer | Versioned interface | Minimum observable acceptance |
|---|---|---|---|
| SHD-CCP-core | All | `TileCodecV1`, exact `Quadrance/TQF`, immutable eight-byte vectors | identical byte output CPU32/CPU64/Python/C/Rust (when implemented) |
| Kernel-Registry | CubiLoom, Orchestrator, Agents | `KernelManifestV1`, `RegistryRootV1` | reject fixed-field collision, stale/revoked layouts, agent self-approval |
| PolyShard-Agent | CubiLoom | `ObservationEnvelopeV1`, `AI-DNAManifestV1`, scoped evidence refs | valid source auth + clock domain + replay prevention |
| CubiLoom | PolyShard-Agent, Orchestrator | `ChronoShuttleV2`, `EventAppendV1`, `CausalHeadsV1`, `SealThreadV1` | idempotent append, bounded partition replay, privacy-preserving replication |
| Orchestrator | Manifold-Projection | `SceneSnapshotV1`, `CubicFrameTransformV1` | signed/approved transforms, exact metric checks, separate rendering uncertainty |
| Manifold-Projection | FractalOS-runtime | `ComputeJobV1`, `GpuBufferV1` | capability negotiation; CPU reference reproduction; device fence lifecycle |
| FractalOS-runtime | all compute clients | `DeviceCapabilitiesV1`, `BackendDispatchV1` | deterministic CPU fallback; no hardware vendor dependency in protocol |
| Geometric-Labs | all | `ConformanceReportV1`, `EcosystemLockV1`, scenario fixtures | reproducible SHA lock; independent verification; no source duplication |
| BioChain-AI (optional) | CubiLoom/Orchestrator | `BioMeshAdapterV1` | explicit delegated scopes, schema mapping, no shared Firebase privileged keys |

## Core invariants

- Wire Tile v1 contains 64 logical bits, network order, fixed Einstein Tile positions. Extra security data remains in bound sidecars; unregistered layouts fail closed.
- Use exact integer/rational geometry whenever a mathematical certificate depends on exactness. Projector float approximations carry explicit error metadata.
- Preserve full parent event links. Quaternionic aggregation and AI-DNA seed pointers do not losslessly imply individual histories.
- The orchestrator is a **governed index and coordinator**, not a global authority over all source documents.
- Logical clock/geometric phase provide relative indexing but physical event simultaneity requires bounded clock error and anchoring.
- All model and RAG content is untrusted data; no tool elevation from a string/embedding or semantic coherence score.

## Publication decision

Put message/schema source of truth in `SHD-CCP-core` or the repository producing the interface. Geometric-Labs holds derived compatibility checks and the lockfile, not an independent fork. Version with semver + format version + hashes. An incompatible wire change requires protocol negotiation and a migration path.
