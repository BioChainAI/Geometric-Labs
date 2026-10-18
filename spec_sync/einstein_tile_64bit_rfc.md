# Einstein Tile reference profile v1

Status: local implementation profile derived from the attached blueprint and
Python runner, pending the canonical Layer 0 RFC. This is not an upstream spec
snapshot or a claim of cross-language conformance.

All wire words are unsigned 64-bit integers, serialized big-endian. Header:

| Bits | Field | Width |
|---|---|---|
| 61–63 | cycle_step | 3 |
| 58–60 | wheel_idx (index, not wheel residue) | 3 |
| 56–57 | struct_sel | 2 |
| 48–55 | gate_byte | 8 |
| 44–47 | step_mux | 4 |
| 40–43 | form_id | 4 |
| 36–39 | stream_slot | 4 |
| 32–35 | scale_reg | 4 |
| 0–31 | payload | 32 |

The South Halo is bits 56–63, an eight-bit routing label, never an authenticator.
Stream IDs combine `(struct_sel << 4) | stream_slot`.
Out-of-range values raise ValueError rather than silently masking.

## Payload forms

* Form 0: opaque uint32; semantics not specified in the supplied artifacts.
* Form 1: doubled Hurwitz coordinates in bytes dw, dx, dy, dz, most significant
  first. The runner masks dw to seven bits, so this profile requires 0 <= dw <=
  127 and -127 <= dx,dy,dz <= 127, with uniform parity. Bit 31 and coordinate
  -128 are reserved. Negative scalar inputs are rejected, never silently
  changed to another quaternion. The original runner's negative-scalar mask is
  lossy; its hash example is retained only as a historical reference fixture.
* Form 2: x1 at bits 20–29, x2 at 10–19, x3 at 0–9. Top two payload bits zero.
  Residues must be canonical for (881,883,887). This packing is a documented
  local choice: the attachments give widths but no complete Form-2 wire layout.
* Form 3: raw IEEE-754 binary32 bits, network byte order. Generic payload access
  preserves all NaN bit patterns; Python float conversion need not do so.
* Forms 4–15: opaque uint32, round-trippable, pending Codex shape schemas.
  Encoding/decoding these envelopes does not validate a shape.

## Golden vectors

Run `make vectors`; use `make check-vectors` to detect drift without writing.
JSON uses exact decimal integers; wire tiles are fixed-width hex strings to
avoid JavaScript's 53-bit integer limit. Other arbitrary-width integer fields
must likewise be parsed with a bigint-capable reader. Rational rectangle bounds
are strings `numerator/denominator` (integers may appear without `/1`). JSON
ordering and indentation are fixed; no timestamps or random unseeded data occur.
The package multiplication table uses doubled coordinates; S5 addresses use
ordinary coordinates and are explicitly labeled.

Canonical associates use lexicographic minimum over the 24 LEFT unit associates.
This local convention awaits the absent Proposition 4.3 text. The tile codec
does not implicitly canonicalize: normalization can change stream orientation.
