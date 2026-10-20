# 00: Upstream analysis

**Subject**: [`Hanzxc/lamport-otp`](https://github.com/Hanzxc/lamport-otp), commit `e658632c850f63aeb5c14accc5d5b9fb94248e78` (2026-06-01, "Initial commit of Lamport OTP hash-chain scheme"). The repository is about 11.7 kB: `lamport.py`, `main.py`, `tests/test_lamport.py`, `README.md`.

## Licensing

The repository has **no LICENSE file**. Without a license, the default is all rights reserved, so this project does not copy, vendor or adapt its code. The algorithm itself is Lamport's 1981 published scheme, and `src/geometric_lamport/lamport.py` implements it from the paper and RFC 2289. The upstream is used only as a behavioural oracle: `tests/test_lamport.py::TestUpstreamEquivalence` checks our values against the hash prefixes printed in the upstream README.

If the upstream later adds a license, record it in `manifest.json` and the research log before reusing anything.

## What it implements

* `H = SHA-256` over raw bytes. The chain is `h0 = seed`, `h(k+1) = H(h(k))`, and the anchor is `h(n)`.
* The client precomputes and stores the whole chain, then releases `h(n-1)`, `h(n-2)`, …, `h0` using an internal counter.
* The server stores one anchor and a remaining count. It accepts `p` when `hmac.compare_digest(H(p), anchor)` holds, then sets `anchor = p`.
* Tests cover chain links, a full session, exhaustion, replay, forgery and out-of-order rejection.

## Observations

| # | Observation | Consequence | CR-0001 response |
| :--- | :--- | :--- | :--- |
| U1 | The client counter advances in `next_password()` before the server accepts. | If a login message is lost, the client skips `h(k)` and later sends `h(k-1)`, which can never verify against `h(k+1)`. The account is locked out for good. | Challenge model as in S/KEY: the server announces index k, and the client derives `h(k)` from the seed. Covered by `test_lost_message_does_not_desynchronize`. |
| U2 | The full chain is stored on the client. | O(n) memory. | v0.1.0 stores only the seed, at O(n) hashes per login. Fractal traversal is an open item (Q5). |
| U3 | The final password is `h0`, the seed itself. | Seed reuse across chains or servers is catastrophic once `h0` is public. With `--seed`, the seed is `sha256(text)`, a guessable low-entropy secret. | Documented in the threat model. Per-context seed derivation is an open item (Q4). Frame profile v0 requires 32-byte seeds because `h0` is framed. |
| U4 | `verify()` raises `TypeError` on non-bytes input. | Minor, but it lets a caller probe type handling. | Our `verify()` returns `False` instead. |
| U5 | No domain separation, no hash agility, no persistence. | It is a teaching project and says so. | `hash_fn` is pluggable. Domain separation is Q4. |

None of these is a flaw in Lamport's scheme. U1 and U3 are integration issues that SHD-CCP framing has to handle explicitly.

## Behavioural equivalence

For `--length 5 --seed demo`, the upstream README prints anchor `b2e07a478cd7467f…` and passwords `c9e347df…`, `e27454af…`, `5e2a90a8…`, `17593901…`, `2a97516c…`. The CR-0001 baseline reproduces all six (`TestUpstreamEquivalence`), so the clean-room implementation computes the same chain.
