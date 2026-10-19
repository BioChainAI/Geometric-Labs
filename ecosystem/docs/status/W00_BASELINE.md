# Wave 00 baseline

Base: `6361440517c4954a3e65b182851510082703c213` (current origin/main).
Initial checkout: `a6e39e56b7738c5ec941cfe0625dbc7f76a21a2e`, branch `work`, clean.
Fetched main has two later upload/deletion commits whose combined tree matches
our initial tree. Feature branch: `codex/geometric-labs-ecosystem-integration`.
No pre-existing AGENTS.md, ecosystem/, devcontainer or ecosystem workflow.

Before edits: make verify-all PASS (5 pillars, 40 unittest methods);
make test-pillars PASS (40); make check-vectors PASS (5 files).
Rechecked verify-all on current main: PASS. Logs copied to evidence/wave01/.

## Independent repositories (live Git inspection)

- `CubiLoom`: `9abafa43ce4a2fd61c35e2d05479a706e83118c9`
- `FractalOS-runtime`: `e4e1d520631bdcc443428ca6abce719082f5dd02`
- `Kernel-Registry`: `c94efcd43f690fadce8b4be33126bdb699dadbde`
- `Manifold-Projection`: `32a8bed5ce5a9ef4409ee9150f6f9911c3fa3c6d`
- `PolyShard-Agent`: `094c2856abaac02cdbef64c848fccea6e13cb95f`
- `Polycentric-Orchestrator`: `bc0bbad6d28ebc54dee36b440be2b1db92898805`
- `SHD-CCP-core`: `154685b2cc65ed5120e36ad733c03f550760a09b`

CubiLoom: README/LICENSE only; no store or replication yet. FractalOS: ABI header,
backend notes, no executable runtime. Core: C11 two-u32 codec, Python fixed fields,
proposed spec and three byte fixtures. Registry: mechanical linter. Agent/control/
projection: stdlib Python references; their README umbrella commands refer to
missing external paths, so integration must supply standalone orchestration.
No component AGENTS.md found. All seven checkouts clean, native HTTPS Git reads
work. gh API read returned Forbidden; GitHub PR API capability needs diagnosis.

## Profile audit

Field positions and big-endian bytes agree. Form 0 conflicts (opaque vs named
lossy quaternion); Form 1 upstream raw sample is noncanonical; Form 2 upstream
packing undefined; Forms 4–15 named without codecs. Keep local vectors unchanged
and negotiate separate semantic IDs. No normative migration in this wave.

## Handoff validation

Compact and full ZIP CRC checks passed; compact CONTENTS_SHA256 checker passed.
Use proposed overlay selectively; exclude bundled bytecode, copy instructions,
optional Docker/devcontainer/deploy profiles. Candidate architecture notes remain
proposals, not claims of executed milestones.
