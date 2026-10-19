# 03: Frame profile `cr-0001.otp-frame.v0`

| | |
| :--- | :--- |
| **Status** | Draft, `[HEURISTIC]`. The layout is not frozen. |
| **Base profile** | `geometric-labs-reference-v1` ([spec_sync/einstein_tile_64bit_rfc.md](../../../../spec_sync/einstein_tile_64bit_rfc.md)) |
| **Reference code** | `src/geometric_lamport/tile_frame.py` |
| **Vectors** | `vectors/cr0001_v0.json`, key `frames_in_login_order` |

The key words MUST, MUST NOT and SHOULD follow RFC 2119.

## Frame

A frame is an ordered sequence of exactly **9** uint64 tiles, each serialized big-endian, as in the base profile.

| Position | `form_id` | `step_mux` | Payload |
| ---: | ---: | ---: | :--- |
| 0 | 2 | 0 | Chain index k as Form-2 CRT residues (x1 bits 20–29, x2 bits 10–19, x3 bits 0–9, moduli 881, 883, 887), 0 ≤ k ≤ 690,017,700 |
| 1–8 | 0 | 1–8 | Password bytes `4(pos-1) … 4pos-1`, as a big-endian uint32 |

**Routing fields**: `cycle_step`, `wheel_idx`, `struct_sel`, `gate_byte`, `stream_slot`, `scale_reg`. These are chosen by the sender and MUST be identical on all nine tiles. Their meaning comes from the base profile. This profile gives them no authentication role.

## Encoder rules

* The password MUST be exactly 32 bytes. Because the final login presents `h0`, **the seed MUST be 32 bytes**.
* The index MUST be the server's current challenge.

## Decoder and verifier rules

A verifier MUST reject a frame, and leave the server state unchanged, if any of these hold:

1. It does not contain exactly 9 tiles, or a tile is not a uint64.
2. Some tile at position p has `step_mux ≠ p`, or a form ID different from the table above.
3. The routing fields differ between tiles, or differ from the verifier's configured route.
4. The Form-2 payload is not canonical, as defined by the base profile.
5. The decoded index differs from the server challenge.
6. `H(password)` differs from the stored anchor, compared in constant time.

Step 6 is the only authentication step. Steps 1–5 are cheap pre-filters and MUST NOT replace step 6. Every rule has a negative test in `tests/test_tile_frame.py`.

## Size

A frame is 72 bytes on the wire. A raw 32-byte password plus a 4-byte counter would be 36 bytes. The extra cost buys L1 routing on every tile and alignment with the SHD-CCP word size.

## Known conflicts and dependencies

* **Form ID position.** The base profile puts `form_id` at bits 40–43. Draft RFC 01 in `SHD-CCP/geometric-engine-spec` uses bits 36–39, and the SHD-CCP Kernel Ontology uses bits 60–63. This profile goes through `geometric_labs.tile_codec`, so it will follow whichever position is chosen, but the vectors will change and a minor version of this profile will be needed. See Q1.
* **Form semantics.** Form 0 is "opaque uint32" and Form 2 is a "documented local choice" in the base profile. If the canonical Layer 0 RFC assigns them other meanings, this profile has to move to forms the ontology allocates for it (Q2).

## Kernel Ontology proposal (not yet submitted)

If adopted, the fragment and index tiles would be proposed to `SHD-CCP_Kernel_Ontology/01_Incubator_Experimental/` as `[OPEN]` kernels with full `Bit_Allocation` maps. That submission waits on Q1, because the ontology requires the Form ID at bits 60–63, which conflicts with the base profile used here.
