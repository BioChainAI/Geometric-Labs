# Provisional profile compatibility

The gate executes both independent upstream C11 and Python codecs and the
unchanged local codec. It reads the live locked JSON spec and both fixture sets;
183 packet cases cover upstream examples, all local forms, every one-hot bit
and 100 seeded words. Upstream C tests compile with warnings as errors.
`two-u32` is tested on this native 64-bit host, not a claimed i686 execution.

| Category | Result / scope |
|---|---|
| fixed_header_match | PASS: aliases mapped explicitly; complete 64-bit field coverage |
| byte_order | PASS: eight-byte big-endian round trips through C/Python/local codec |
| Form ID | PASS: bits 40–43, valid values and C rejection of form 16 |
| supported_form_round_trip | PASS: local Form 1/2/3 semantic fixtures; upstream raw envelopes and Form 3 only |
| reserved_bits | PASS: local Form 1 bit31/parity/-128 and Form 2 top bits reject |
| unsupported_form_fails_closed | PASS: opaque forwarding explicit; semantic decode unavailable forms rejected |
| wrong profile/version/endian | PASS: integration metadata validation rejects mismatches |
| legacy_word_adapter_compat | REJECTED/UNIMPLEMENTED: explicit legacy ID never reinterpret-cast as Tile |

Raw bytes cannot reveal their producer's semantic profile or declared endianness.
The gate validates metadata plus known fixtures; it does not claim universal
recognition of incorrectly labeled packets. Structural success is reported as
`status: PASS` with **`semantic_compatible: false`** and machine-readable gaps.

| Forms | Local semantics | Upstream state | Action |
|---|---|---|---|
| 0 | opaque core | named lossy quaternion; no full codec | keep separate |
| 1 | doubled parity/sign/range checks | raw envelope accepts noncanonical sample | local semantic decoder only under local ID |
| 2 | explicit local 10/10/10 CRT | name without normative packing | no cross-profile conversion |
| 3 | raw binary32 | raw payload usable as binary32 | shared representation, explicit profile still required |
| 4–15 | opaque envelopes | named Codex shapes without codecs | forward only as unresolved opaque bytes |

`contracts/protocol_profiles.v1.json` defines the new integration labels and an
explicit alias to the original local fixture label; no fixture bytes or existing
profile files were rewritten. `receive()` is integration validation, not a new
competing core codec. Normative profile promotion belongs in a separate reviewed
SHD-CCP-core RFC/PR with human sign-off. The current upstream HTTP demo does not
yet negotiate these semantic-profile labels; that transport change is deferred.
