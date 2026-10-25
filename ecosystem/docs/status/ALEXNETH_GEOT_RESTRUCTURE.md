# AlexNet-H/GEOT RFC 0.2 restructure — completed CPU reference review

Branch: codex/alexnet-get-framework. Base: d8c92a4997b73dfe401b005c914a1be3f5709347.
The proposal and CPU implementation are prepared for the user-requested commit
and feature-branch push. Main is not merged or modified; no deployment or upstream
source change is performed. The commit containing this report identifies the release.
The workspace disconnected during final documentation, then reconnected. Existing
code/evidence/environment survived; the missing documentation and dependency
snapshot are now saved and validation rerun after the semantic zero-limit fix.

## Deliverables

- `ecosystem/experiments/alexneth_geot/`: actual multiscale stem, fold/mixer,
  64-cell routers and separate semantic head; 2,506,558 parameters by default.
- Preserved verbatim RFC/prototype and supplied six tests in research/.
- Float/runtime primitives distinct from bounded exact rational oracle.
- Typed visual descriptor preflight and actual independent agent/control HTTP
  harness; no new normative Tile form and no private image/RAG publication.
- Python3.12 CPU dependency snapshot, editable package, pip/NumPy/Torch checks.
- README, migration rationale, interop capability matrix, architecture flowchart,
  file-hash source inventory and machine-readable validation evidence.
- Older `alexnet_get/` proposal retained with a pointer to the current implementation.

## Executed evidence

| Check | Actual result |
|---|---|
| Root make verify-all | PASS: five pillars, 40 test methods, five vector files |
| Ecosystem offline tests | PASS: 20 methods, including baseline byte preservation |
| Pinned ecosystem integration | PASS: 4 methods |
| Original supplied math tests | PASS: 6 methods, original archive bytes unchanged |
| New neural/reference/interop tests | PASS: 16 methods, including zero-origin gradient regression |
| Unique unittest methods | 86, no zero-test suite counted as passing |
| C/Python packet compatibility | PASS: 183 packets |
| Seven-repository lock | PASS: all expected clean SHAs |
| Synthetic vision interop | PASS: 3 sidecars; 16,384-byte local descriptors; replay/tamper rejection |
| Dependency/package checks | PASS: pip check, editable install, outside-checkout import and NumPy/Torch roundtrip |

Reports: `ecosystem/experiments/alexneth_geot/evidence/validation.json`,
`environment.json`, `interop.json`, `protocol.json` and corresponding command logs.
The fixture TQF is 576 for supplied synthetic coordinates, not inferred camera pose.

## Outstanding capabilities

The network is untrained; no recognition accuracy or speedup claim. Original
v0.1 baseline source/weights and some source papers cited by the RFC are absent.
Remote visual-schema/purpose enforcement needs an upstream contract; local
preflight does not supply that authority. CubiLoom persistence and FractalOS tensor
execution are absent. Video/keyframe/residual training and GPU/Loihi/QEMU are
unrun. Normative forms and original golden vectors remain unchanged.

Next implementation PR: remote VisualObservation contract and controlled dataset
baseline, with multi-seed Euclidean/Lorentz comparison. Persistence/backend work
belongs in separate owning-repository PRs. No automatic certification or deployment.
