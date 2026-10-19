## Add a pinned seven-repository reference integration environment

Geometric-Labs currently validates its local geometry package but cannot reproduce
the independently versioned BioChainAI agent/control/projection workflow. This PR
adds an isolated ecosystem/ workspace with exact repository URLs, dependency DAG,
reviewable SHA lock, clone-missing manager, C/Python compatibility gate and a
three-agent loopback reference demo.

The original math package, all existing tracked files, five golden-vector files,
root Makefile and existing workflow remain byte-for-byte unchanged. Outside
ecosystem/, only the supplied AGENTS.md and a separate read-only CI workflow are
added. Independent upstream sources remain in ignored checkout directories.

- Reject dirty/unrecognized/wrong-origin/symlink workspaces and changed locks.
  Restore missing dependencies at locked SHAs; never advance existing refs.
- Test 183 C two-u32/Python/local packet cases. Keep glab-local-v1 and
  shdccp-proposed-v1 semantic differences explicit; no fixture migration.
- Import actual upstream modules, obtain exact TQF 576 from three agents, and
  verify 11 HTTP rejection cases plus private-RAG non-export.

Validation on Python 3.12: original 40 tests + 20 offline ecosystem tests +
4 pinned integration tests pass (64 unique unittest methods). `make verify-all`,
`make -C ecosystem geometry`, demo, protocol gate and clean lock checks pass.
Evidence and before/after counts: ecosystem/docs/status/W01_INTEGRATION.md and
machine-readable ecosystem/evidence/wave01/acceptance.json.

CubiLoom is still README-only; FractalOS is an interface scaffold. Current upstream
handshake has no semantic-profile negotiation and HTTP/HMAC/replay state remain
development-only/in-memory. Persistence, partition recovery, signed frame expiry,
production identity and accelerator lanes belong to subsequent owning-repo PRs.
No auto-merge, production access or normative protocol promotion is requested.
