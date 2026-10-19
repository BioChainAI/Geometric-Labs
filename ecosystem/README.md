# Geometric-Labs ecosystem reference environment

Seven independent BioChainAI repositories plus this eighth integration lab.
The existing exact-math package, root tooling and golden vectors are unchanged.
See [implementation plan](docs/IMPLEMENTATION_PLAN.md) and
[Wave 01 report](docs/status/W01_INTEGRATION.md).

## Reproduce

Python 3.10+, Git and a C11 compiler (`cc`) are required. All Python runtime
imports use the standard library and actual source checkouts; no pip packages,
Docker daemon, database server or production credentials are needed.

```sh
python3 ecosystem/tools/glab.py list
make -C ecosystem test                    # offline tests, no external clones needed
python3 ecosystem/tools/glab.py sync --require-lock
make -C ecosystem doctor
make -C ecosystem check-lock
make -C ecosystem geometry                # unchanged five-pillar baseline
make -C ecosystem protocol-compatibility   # C11 two-u32 + Python byte fixtures
make -C ecosystem integration             # 4 real-checkout acceptance tests
make -C ecosystem demo                    # 3-agent loopback HTTP, exact TQF 576
make -C ecosystem acceptance              # logs + JSON in evidence/wave01/
```

`sync` clones missing checkouts at reviewed locked commits. Existing checkouts
are validated, never pulled, reset or checked out automatically. Dirty files,
wrong origins, unknown directories, symlinks, or changed SHAs fail closed.
Nested sources stay ignored in `ecosystem/workspaces/`; ownership remains
upstream. `lock` is repeatable without rewriting an identical file. To propose
new compatible SHAs, independently choose/test those upstream commits and use
`python3 ecosystem/tools/glab.py lock --refresh-lock` in a reviewable branch.
No refresh command is part of CI or ordinary sync.

## Contracts and evidence

* Manifest v1: exact URLs, roles, dependency DAG and optional legacy BioChain-AI.
* Lock v1: exact seven SHAs, URLs and canonical-manifest SHA-256.
* Profile gate v1: `einstein-tile/1`, `glab-local-v1` (explicit alias for existing
  fixture label `geometric-labs-reference-v1`), and `shdccp-proposed-v1`.
* [Compatibility matrix](docs/PROTOCOL_COMPATIBILITY.md): fixed-bit agreement is
  tested separately from unresolved Form 0/1/2/4–15 semantic differences.
* [Machine-readable evidence](evidence/wave01/acceptance.json) preserves actual
  command return codes and counts. Use `--output-dir /tmp/ecosystem-evidence`
  on `tools/run_acceptance.py` to avoid modifying committed reports.

Imports are checked against independently cloned source locations; source files
are never copied into this lab. The harness disables bytecode writes to keep
those inputs clean. Upstream READMEs contain obsolete umbrella commands; the
commands above replace that workspace assumption for this integration only.

## Scope and limits

The demo starts an ephemeral loopback-only server, sends three authorized
reference observations, tests 11 actual HTTP refusals, checks private RAG does
not appear in exported events, then closes the server and local databases.
Clock/frame are explicitly simulated/pre-agreed; HMAC keys are ephemeral and
never logged. Upstream replay state and accepted events are in memory. Current
handshake has a protocol ID but no semantic-profile negotiation; profile
validation here is a separate integration gate, not an upstream security upgrade.

CubiLoom is README-only; FractalOS is a hosted-interface design. No durable causal
store, partition recovery, certificate expiry/revocation, production identity,
Firebase access, GPU/H100, Loihi 2 or QEMU result is claimed. Docker/devcontainer/
deployment candidates were deliberately excluded from this first tested CPU lane.
The legacy BioChain-AI adapter is opt-in and was neither cloned nor connected.
