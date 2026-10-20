# 02: Geometric adaptation

The only property Lamport needs from `H` is **preimage resistance**, and the strong form of it: given `H(x)`, find `x`. A geometric adaptation can touch three layers:

1. the **one-way function** itself (E1, E2);
2. the **representation** of chain values as geometric objects;
3. the **transport** of OTP presentations on SHD-CCP tiles (E3).

## E1: an exact Hurwitz quaternion walk as `H` (`[FAILED]`)

**Construction** (`src/geometric_lamport/hurwitz_walk.py`). The generators are the six Lipschitz quaternions of norm 5 used by LPS for p = 5:

```
1+2i, 1-2i, 1+2j, 1-2j, 1+2k, 1-2k      (doubled: (2,±4,0,0), ...)
```

A 32-byte digest becomes a base-5 numeral of L = 111 digits (5^111 ≥ 2^256). Each digit picks one of the five generators that do not undo the previous step. The output is the product quaternion, which has norm 5^111 and doubled coordinates of about 130 bits.

**Hypothesis**: the product is a compact geometric commitment from which the path, and so the digest, is hard to recover.

**Result**: refuted. Primitive Lipschitz quaternions of norm p^k factor uniquely into norm-p factors, up to unit migration (Conway and Smith 2003, ch. 5). The six generators lie in six distinct left-unit classes (`test_generators`), so at each step exactly one generator `g` satisfies `Q · conj(g) ≡ 0 (mod 5)`. Dividing it out and repeating recovers the whole path. `invert_walk` does this in L exact divisions, about 3 ms for a 256-bit input in CPython. `test_random_walks_invert_uniquely` and `test_walk_anchor_leaks_the_next_password` show that a server storing a walk anchor would hand out the client's next password.

**Lesson**: an exact (unreduced) walk in a free group is an *encoding*, not a hash. The norm grows with the input, and the group structure provides a perfect inverse. This is why the walk ships as a **negative control** in the golden vectors.

## E2: reduced walks (`[OPEN]`, LPS closed)

Reducing the walk modulo a prime q, into PSL2(F_q), gives the Lubotzky–Phillips–Sarnak expander hash studied by Charles, Goren and Lauter (2009). That family has been broken:

* Tillich and Zémor (2008) found collisions for the LPS hash.
* Petit, Lauter and Quisquater (2008) gave full cryptanalysis of the LPS and Morgenstern hashes, preimages included.
* Earlier Cayley hashes over SL2(F_2^n) (Tillich and Zémor 1994) have also seen collision and preimage attacks.

A Lamport `H` built on these would fail the one property it needs. The surviving geometric candidate is the supersingular isogeny-graph hash from the same Charles–Goren–Lauter paper. Path finding in that graph is still believed hard, but it needs elliptic-curve arithmetic over F_p², which is far outside this repository's exact-integer core. It is recorded as Q3 and would be a separate research item if pursued.

## Representation layer

Chain values are 256-bit strings. Geometric views of them are allowed, but only as views:

* A walk encoding is lossless. Applied to a password, it is exactly as secret as the password (E1).
* A Hurwitz-unit fingerprint, for example the product of 24-unit labels taken from digest bytes, falls into a group of order 24. A forger matches it with probability 1/24, so it may serve only as a routing or visualization label, never an authenticator.

No v0.1.0 component derives authority from a geometric view.

## E3: SHD-CCP transport (`[HEURISTIC]`)

A 64-bit tile has a 32-bit payload in the Geometric-Labs local profile, or 52 bits in draft RFC 01. Either way, one tile cannot carry a password. RFC 2289's 64-bit folded OTP would already be marginal, and a 32-bit OTP falls to brute force. The binding therefore spreads one presentation across a **nine-tile frame**:

* Tile 0 (Form 2) carries the chain index as Garner CRT residues mod (881, 883, 887). This reuses `geometric_labs.tile_codec.encode_form2`, and the index range of 0 to 690,017,700 is far above any practical chain length.
* Tiles 1–8 (Form 0) carry the password as eight big-endian 32-bit words.

`step_mux` gives the position of each tile in the frame. The routing fields (cycle_step, wheel_idx, struct_sel, gate_byte, stream_slot, scale_reg) must be identical on all nine tiles. This gives the L1 South Halo pre-filter one value per frame and makes splicing tiles from two streams detectable. The full normative draft is [03_shd_ccp_tile_binding.md](03_shd_ccp_tile_binding.md).

**Why `[HEURISTIC]` and not `[COMPUTED]`**: the layout is complete and tested, but it is built on a tile profile whose Form ID position is not yet reconciled across the ecosystem (Q1). Forms 0 and 2 are also provisional semantics in that profile.

## Overall assessment

| Layer | Geometric? | Security-bearing? | v0.1.0 decision |
| :--- | :--- | :--- | :--- |
| One-way function | E1 failed, E2 broken or out of scope | Yes | SHA-256 (pluggable) |
| Representation | Optional views | No | Allowed, labelled non-authenticating |
| Transport | SHD-CCP tile frame | No | `cr-0001.otp-frame.v0` |

The research outcome is therefore a **hybrid**: a classical hash supplies the security, and the SHD-CCP geometric protocol supplies addressing, framing and routing.
