# AlexNet-H/GEOT RFC 0.2 — CPU reference integration

**Working, untrained reference implementation.** New work uses this directory;
the older alexnet_get planning scaffold remains preserved for provenance.
No original core mathematics, vectors, upstream code or existing CI was changed.

Implemented: multiscale five-convolution stem, reversible H–W–H fold3, declared
four-fiber quadratic mixer, 64-cell periodic local routing, bounded spinors,
matched Euclidean/Lorentz scorers, separate 64D Poincare semantic embedding,
classification logits, exact rational oracle and versioned visual sidecars.
Default 10-class model: **2,506,558 parameters**. A forward/backward optimizer-step
test checks execution, not recognition capability. No dataset training occurred.

## Reproduce

From the Geometric-Labs root on a tested Linux/Python3.12 CPU machine:

```sh
python3 -m venv /workspace/.venvs/alexneth-geot
/workspace/.venvs/alexneth-geot/bin/python -m pip install -r ecosystem/experiments/alexneth_geot/requirements-cpu-py312.txt
/workspace/.venvs/alexneth-geot/bin/python -m pip install --no-deps --no-build-isolation -e ecosystem/experiments/alexneth_geot
python3 ecosystem/tools/glab.py sync --require-lock
make -C ecosystem/experiments/alexneth_geot PYTHON=/workspace/.venvs/alexneth-geot/bin/python verify
```

The dependency snapshot records installed versions, including Torch 2.9.1+cpu and
NumPy 2.3.5. It is **not** a cross-platform, hash-locked dependency release.
PyPI and the official PyTorch CPU index supply dependencies with normal TLS and
package-index verification. No data or pretrained weights download automatically.
The root stdlib package stays independent of this optional ML environment.

Other targets: `test` (16 new tests), `research-tests` (6 original supplied tests),
`interop` (real synthetic-image descriptor flow). `verify` also runs the original
40 tests, 20 ecosystem tests, 4 pinned integration tests, 183 C/Python packet
cases and release-lock validation. Missing prerequisites fail rather than pass
as skipped checks. Evidence is saved in [validation.json](evidence/validation.json).
Use `tools/verify.py --output-dir /tmp/geot-evidence` for a non-writing report run.

[Mermaid architecture diagram](docs/architecture.mmd) · [Completion report](../../docs/status/ALEXNETH_GEOT_RESTRUCTURE.md)

## Architecture

Image → multiscale maps → 16×16 alignment → fold3 → folded quadratic mixer →
64 latent cells → local Euclidean/Lorentz sparsemax → class/semantic heads.
Output descriptors → explicit local consent gate → existing Form-3 confidence
Tile plus versioned sidecar → independent agents/orchestrator → CPU projection.

A 64×64 float32 descriptor is **16,384 bytes**. It stays in a local temporary
artifact store during interop; transport carries a hash and typed metadata.
The Tile is eight big-endian bytes and carries confidence, not the tensor.
Tensor bytes are separately declared little-endian. Source images and private
RAG are not exported. Fixture triangle coordinates are supplied synthetic points,
not physical XYZ inferred from the network. Its TQF576 is a fixture check only.

## Scope

The generic upstream receiver preserves the signed experimental sidecar but does
not validate its new visual schema/purpose. Local validation is not remote
policy enforcement. Identity is ephemeral development HMAC over loopback, not
production authentication. CubiLoom persistence, FractalOS tensor jobs, temporal
training and GPU/Loihi/QEMU are unavailable or unrun. The claimed original
2,486,913-parameter v0.1 source/weights were not supplied, so no accuracy comparison
is claimed. See [restructure decisions](docs/RESTRUCTURE.md),
[interop matrix](docs/INTEROPERABILITY.md) and [supplied RFC](research/ALEXNETH_GEOT_ARCHITECTURE_RFC.md).
