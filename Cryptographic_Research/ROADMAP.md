# Roadmap

These are candidates for research items after CR-0001. Order and scope are proposals. An item gets an ID only when someone opens it with `make new`.

| Candidate | Origin | Why it fits | First geometric question |
| :--- | :--- | :--- | :--- |
| Lamport one-time signatures | Lamport 1979 | Hash-based like CR-0001, and the root of post-quantum hash signatures | Can a 64-bit tile frame carry key and signature fragments efficiently? |
| Winternitz OTS / WOTS+ | Merkle 1989; Hülsing 2013 | Hash chains per digit, a direct extension of CR-0001 | Can chain-length / digit trade-offs map onto the 4-bit `step_mux` / 16-form space? |
| Merkle trees and XMSS | Merkle 1979; RFC 8391 | The repository already has a 12-layer Merkle certifier | Map tree addresses onto the 64-stream / 12-engine routing models |
| Shamir secret sharing | Shamir 1979 | Polynomial geometry over finite fields | Relate shares to cuboctahedral 12-engine erasure recovery |
| Diffie–Hellman | Diffie–Hellman 1976 | A classical key exchange to compare against | Would a group built on Hurwitz quaternions be safe? (Expect a negative result, as with E1.) |
| Garner CRT / RSA-CRT | Garner 1959; Quisquater–Couvreur 1982 | `garner_crt` is already a core module | Fault-attack and timing implications of CRT recombination on tiles |
| Isogeny-graph hash (CGL) | Charles–Goren–Lauter 2009 | The surviving geometric hash candidate from CR-0001 E2 | Is it feasible within the exact-integer core? |

CR-0001's open questions Q1 (Form ID position) and Q2 (Form allocation) apply to every item that binds to tiles, so resolving them upstream comes first.
