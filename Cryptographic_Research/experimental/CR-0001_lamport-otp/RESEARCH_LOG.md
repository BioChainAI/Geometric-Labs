# CR-0001 research log

This log is append-only. Each entry has a date, an author, the version under test, and what was done, found and decided. Never rewrite an earlier entry. Add a correction entry instead.

---

## 2026-10-19: Item opened (v0.1.0)

**Author**: Claude Code session, at the request of the repository owner.

**Done**
* Pinned the upstream `Hanzxc/lamport-otp` at `e658632`. It has no LICENSE, so it is used as a behavioural reference only and no code was copied.
* Wrote a clean-room challenge-style baseline. It reproduces all six hash prefixes in the upstream README.
* E1: implemented the norm-5 Lipschitz quaternion walk and its factorization inverse.
* E3: designed and implemented the nine-tile frame `cr-0001.otp-frame.v0` on `geometric-labs-reference-v1`.
* Generated golden vectors `vectors/cr0001_v0.json`. 29 tests pass on Python 3.13, and also as standalone scripts.

**Found**
* Upstream U1: the client counter advances before the server accepts, so one lost login message locks the account out. Fixed by the challenge model.
* E1 refuted: the walk is a bijection. All 100 random 256-bit inputs were recovered from the product, each in about 3 ms.
* The final login presents `h0` (the seed), so the 32-byte frame requires a 32-byte seed. This was caught by a failing test and is now a profile rule.
* There are three conflicting Form ID positions across the ecosystem (Q1).

**Decided**
* The security core stays SHA-256. Geometry is used for representation and transport only.
* E2 (reduced LPS-type walks) will not be implemented as `H`, because published preimage attacks exist.
* Overall status `[HEURISTIC]`. Next steps: Q1, Q2 and Q4.
