# Development Environments and Start Commands

| Profile | Runs where | Core dependencies | Entry point | Status |
|---|---|---|---|---|
| Math reference | local Python 3.10+ or devcontainer | existing Geometric-Labs `verification/`, `spec_sync/` | `make -C ecosystem geometry` | repository already provides verification |
| Workspace/doctor | local Python 3.10+, Git | 7 GitHub repo checkouts | `make -C ecosystem doctor` | implemented |
| Manifest CI | local Python 3.10+ | none | `make -C ecosystem test` | implemented |
| Federation reference | local Python 3.10+ | four repo source directories | `make -C ecosystem demo` | uses existing development-only service |
| Container reference | Docker Compose | four checkouts | `docker compose -f ecosystem/deploy/compose.yaml --profile reference run --rm reference-mesh` | optional, local-only |
| Replica chaos | local containers and mock clocks | CubiLoom storage service TBD | `docs/MILESTONES.md` | not yet implemented |
| Trust/certification | isolated Python validators + keys | Kernel-Registry and SealThread | milestone R3 | unimplemented security validation |
| GPU/Hopper | NVIDIA host/container with CUDA toolkit | Manifold-Projection, FractalOS HAL | milestone R5 | backend specification only |
| Neuromorphic | Intel-supported Lava/Loihi lab | FractalOS host bridge | milestone R6 | backend specification only |
| Bare metal | QEMU + cross compiler | FractalOS runtime | milestone R7 | OS research only |
| BioMesh legacy | optional isolated Firebase emulator | BioChain-AI checkout | `glab.py sync --include-optional` | adapter not implemented |

## Safety and secret handling

Do not attach production tokens or mount private databases into developer containers. The geometry container disables networking. The reference-mesh container uses container-local loopback for its development server but publishes no host ports; it is not a production-security boundary. GPU privileges and Docker socket are not shared with reference containers. No production ports are exposed.

## Platform matrix and toolchains

- Windows: VS Code Dev Containers / WSL2 recommended for Make/Git/C and QEMU; script also runs with Python on Windows if Git exists.
- Linux: primary CPU and Docker/CI development target.
- macOS: Python reference and cross-architecture builds; H100/Loihi testing elsewhere.
- 32-bit: C two-u32 codec conformance via i686 toolchain/QEMU where available; no need for separate tile version.
- CPU portability: amd64, arm64, RV64, i686 conditional; explicit feature discovery for AVX2/AVX512/NEON/RVV.
- CUDA/H100 SM90 TMA and DSMEM only when GPU/device/runtime support them and when benchmark shows meaningful benefit.

## Repo version lock

`glab.py lock` writes `ecosystem/locks/commits.lock.json`, which records exact checked-out commits. Review the lockfile before committing. To update an integration release, use explicit `git fetch`/branch updates in the **upstream checkout**, rerun conformance, then re-lock. The provided sync command never pulls or resets a cloned project.
