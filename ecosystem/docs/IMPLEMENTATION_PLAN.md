# Reviewable ecosystem implementation plan

## Current PR: Wave 01 — additive reference environment

Branch: codex/geometric-labs-ecosystem-integration, target main.
Audit before editing: see status/W00_BASELINE.md and preservation.v1.json.

1. Preserve all existing tracked bytes. Add root AGENTS.md (operator requested),
   ecosystem/ and one independent CI workflow; no root Makefile/README rewrites.
2. Select candidate manifest, ownership/contracts, reference harness, architecture
   tests and workspace manager. Review every destination; exclude pyc, Docker,
   devcontainers and deployment configuration from this CPU-only deliverable.
3. Harden clone-missing and SHA locks: validate exact origins/root locations,
   dirty/unrecognized checkouts, lock schema, URL identities and set membership;
   new clones restore pinned commits; existing refs never advance automatically.
4. Negotiate distinct wire/semantic profiles in integration adapters. Compare
   live JSON fields and both frozen vector sets with native C two-u32 and Python;
   report semantic gaps without relabeling or rewriting upstream/local fixtures.
5. Exercise real independently imported upstream modules through loopback HTTP:
   three agents, exact TQF 576, wrong protocol/form, tamper, replay, denied purpose,
   consent and uncertain clock fixtures. Record actual limits and import origins.
6. Run baseline, offline manifest/manager tests, pinned integration tests, geometry,
   demo, compatibility, upstream C checks, and lock check. Retain JSON evidence and
   logs. Commit additive integration, push feature branch, open draft PR if API
   permits; otherwise supply a compare link and ready PR description. Never merge.

## Subsequent PRs (not implemented in this PR)

| Wave | Owner / proposed branch | Contract and acceptance |
|---|---|---|
| 02 | SHD-CCP-core codex/versioned-profile; registry review | Explicit provisional profile IDs; canonical form RFC and cross-language fixtures; human approval before normative change |
| 03 | agent/orchestrator separate codex/federation-contract branches | Durable negotiation metadata, clock/frame lineage; independent owning-repo tests |
| 04 | CubiLoom codex/causal-event-store | SQLite append/query/heads/replay, duplicate/orphan/conflict and partition/restart tests |
| 05 | Registry, CubiLoom, agent/control separate branches | SealThread canonical signature bytes, revocation/expiry/replay, independent human promotion |
| 06 | Projection/FractalOS separate CPU branches | Exact CPU oracle, hosted ABI and capability detection; hardware lanes remain optional |

No upstream code changes are needed for the first harness; it pins tested current
SHAs. Lock advancement is an explicit review operation, not a sync side effect.
Rollback via feature PR revert/previous reviewed lock; never reset user changes,
overwrite research, delete dependency checkouts, or migrate stored data destructively.
