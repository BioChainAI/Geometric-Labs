# 01: Threat model

## Assets

* **Seed `h0`**: the client secret. Whoever holds it holds every password in the chain.
* **Unused passwords `h(0) … h(k)`**: each one is a single login.
* **Server state `(anchor, remaining)`**: public in principle. Its integrity matters, its confidentiality does not.

## Adversaries

| Adversary | Capability | Expected outcome |
| :--- | :--- | :--- |
| Passive eavesdropper | Sees every frame and every used password | Cannot log in. The next password is a preimage of the last one seen. |
| Database reader | Reads the server anchor | Cannot log in, as long as `H` is preimage resistant. Track E1 shows this fails for a quaternion walk. |
| Replayer | Re-sends a captured frame | Rejected, because the anchor has already moved on. |
| Splicer | Combines tiles from two frames or streams | Rejected by the frame decoder (same routing headers, positions 0–8). |
| Active man-in-the-middle | Intercepts a password before it reaches the server | **Not defended.** This is the race attack in RFC 2289 §9.0. Lamport OTP needs a protected channel or channel binding. |
| Client compromise | Steals the seed | **Not defended.** Re-registration is required. |
| Quantum adversary | Grover search | About 2^128 work for a SHA-256 preimage. Acceptable for now. |

## Properties CR-0001 must keep

1. **One-time use**: an accepted password never verifies again (replay tests).
2. **Forward secrecy of the chain**: seeing `h(k)` does not reveal `h(k-1)`.
3. **Server holds no secret**: the anchor is a commitment, not a password.
4. **No silent truncation**: the full 256-bit password crosses the wire. A 32-bit tile payload alone would fall to a 2^32 brute-force preimage search in seconds.
5. **Transport adds nothing to authentication**: the South Halo, gate byte, routing headers and frame index are labels. This follows the Geometric-Labs `AGENTS.md` rule that authentication never rests on a South Halo, CRC or TQF result.

## Non-goals for v0.1.0

Accounts, persistence, rate limiting, lockout, channel security, recovery and multi-device use. These belong to the BioChain layers that consume this primitive, and they are listed in Q6.
