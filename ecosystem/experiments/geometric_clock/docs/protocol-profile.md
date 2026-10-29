# geometric-clock-pulse-v1 (local candidate)

Wire format: `einstein-tile/1`, eight big-endian bytes. A semantic profile ID must
be supplied alongside the raw word; it cannot be inferred from the bits.

| Bits | Field | Clock meaning |
| --- | --- | --- |
| 61–63 | cycle_step | p mod 8 |
| 58–60 | wheel_unit | Index p mod 8; not a prime residue or certificate |
| 56–57 | structure_selector | Explicit routing selector 0..3; default 0 |
| 48–55 | gate_byte | Node p mod 30; valid clock nodes 0..29 |
| 44–47 | step_mux | Zero |
| 40–43 | form_id | Zero; opaque local pulse-counter payload |
| 36–39 | stream_slot | Explicit slot 0..15; default 0 |
| 32–35 | scale_reg | Zero |
| 0–31 | core_word | p mod 2³²; deliberate wire rollover |

The general `EinsteinTile` API covers all fields and supports raw round trips of
all form IDs. The pulse semantics above apply only to this local clock profile.
In particular, Form 0 is not reinterpreted as an upstream lossy quaternion, and
Form 1/2 packing is not a semantic encoder for a Hurwitz/CRT payload.

Phase index is node mod 3; braid is +1 for an even node and −1 otherwise. The
gate node therefore determines all six C3 × C2 channels without repurposing the
structure field. Tier index is node//6. Handshakes require compatible structure
and stream values and occur at cycle steps 2 and 6, with envelope exactly 1.0.

Counter, node and step eventually alias after 15·2³² pulses; even identical raw
tiles do not imply matching absolute counters, epochs or elapsed time. The
reference verifier uses full snapshots supplied independently in-process, checks
the declared common epoch/frame and exact model uncertainty, and compares the
received bytes to the expected current snapshot. This is not authenticated
network synchronization or anti-replay protection for an untrusted sender.
