# geometric-clock 0.1.0

A standalone Python 3.10+ package implementing the requested tier laws, exact
Cs-cycle bookkeeping, projective spinor cycle, 720/72/10 orientation history,
complete 64-bit envelope and local parity handshake. Runtime dependencies: none.
`pytest` is an optional development dependency, not a runtime import.

```sh
# From the repository root, in your chosen virtual environment:
python -m pip install -e './ecosystem/experiments/geometric_clock[test]'
python -m pytest ecosystem/experiments/geometric_clock/tests -q
geometric-clock --pulses 30
geometric-clock --verify-sync
geometric-clock --pulses 8 --stream
```

The CLI is a finite logical ticker service. It emits an exact final JSON snapshot,
or JSONL for individual ticks with `--stream`. It uses no sleep, network listener,
OS framerate or background daemon. `--verify-sync` exchanges actual eight-byte
words between two independent in-process clock instances at both handshake windows.

```python
from geometric_clock import IntrinsicClock, ParityHandshakeTest

clock = IntrinsicClock()
state, tile = clock.advance(30)
assert state.accumulated_cycles == 4_596_315_885
assert state.remainder == 0.0
assert state.node == 0 and state.spinor_step == 6
assert tile.unpack(tile.pack()) == tile

report = ParityHandshakeTest.verify_cross_node_sync(IntrinsicClock(), IntrinsicClock())
assert report.phase_drift == 0 and report.holonomy1.is_identity()
```

## Seven requested modules

| Module | Public API | Exact scope |
| --- | --- | --- |
| `core.invariants` | `StatorTier`, `GeometricEngineInvariants` | Five tier laws, winding sum 60, integer Cs frequency and Fraction pulse ratio |
| `core.parity` | `Channel`, `ParityMap` | All six C3 × C2 elements, group composition, half-cycle residual |
| `core.spinor` | `SpinorClock` | GCD-reduced Gaussian powers with preserved signs, windows k=2/6 |
| `core.holonomy` | `QuaternionDelta`, `TorsionalMarkovPump` | Rational Hamilton products, inverses, ordered 720/72/10 telescoping |
| `engine.tile` | `EinsteinTile` | All 64 header/payload bits, big-endian bytes and strict bounds |
| `engine.clock` | `ClockState`, `IntrinsicClock` | Immutable exact snapshots; atomic counter/tile updates under an RLock |
| `sync.handshake` | `ParityHandshakeTest`, `HandshakeReport` | Local phase/parity/history verification with transport-tamper injection |

## Mathematical and indexing conventions

The model adopts one 60-pulse cycle as **one SI second by definition**. Its logical
pulse generator does not measure the SI second or establish a physical frequency
from dimensionless geometry. Elapsed model time is `Fraction(pulses, 60)`; real
timing and physical oscillator synchronization need an external reference.

Atomic cycles are computed as `p * Fraction(306421059, 2)`, never by accumulating
float `153210529.5`. The remainder is 1/2 for odd pulses and zero for every even
pulse. Thirty pulses give exactly 4,596,315,885 cycles and a 30-node traversal;
two pulses already close the atomic fractional residual. The node index is 0..29,
so pulse 30 returns to node 0, not node 30.
At pulse 30 the spinor is at k=6; simultaneous node/spinor phase return requires
lcm(30,8)=120 pulses. This is distinct from atomic fractional closure and from
the ever-increasing absolute pulse counter.

Gaussian state is `(1+i)^k` with k=0..7 and positive GCD reduction. The states are
`(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)`. They are exact
**projective integer representatives**, not normalized rational unit spinors at
odd steps. The envelope is a display float, with exact 1.0 at k=2 and k=6.

The pump takes **720 orientation frames**, with open boundary delta[0]=1 and
delta[k]=q[k] q[k−1]⁻¹ for k=1..719. Each ten-delta block is multiplied latest
on the left; its inverse becomes a middle delta. Middle inverses multiply on the
right in chronological order. The 72-to-10 partition uses floor(10m/72), so
groups have seven or eight entries and cover all middle indices once.
`holonomy` and `open_holonomy` are full exact quaternions equal to q0 q719⁻¹;
closed history means **positive identity** `(1,0,0,0)`, not merely norm one or
an SO(3) rotation equivalent to identity. General history is never forced closed.

Coarse rotations preserve block net products, not arbitrary individual history.
No Markov transition kernel, stationary-current result or lossless history
compression is claimed by this hierarchy implementation. The default clock pump
is an explicitly declared closed identity fixture; callers may supply a tested
nontrivial history. Pulse advancement does not invent measured orientation history.

## Wire profile and interoperability

See [the local pulse profile](docs/protocol-profile.md). The wire structure matches
the existing fixed Einstein Tile header, including all fields in bits 32–47.
Generic packing preserves any valid 64-bit envelope and does not decode payload
form semantics. No original codec, upstream profile or frozen vector is changed.

The clock's **local** semantic profile is `geometric-clock-pulse-v1`, wire
`einstein-tile/1`. Form 0 is opaque clock data: gate byte is node 0..29; payload
is the low 32 pulse bits; wheel is an index p mod 8; structure selector remains
a two-bit routing field. All six channels are derived from the node, with phase
index p mod 3 and braid (−1)^p. Six channels are never truncated into two bits.
The full counter and rational time remain in `ClockState`/JSON, beyond wire rollover.

The local handshake compares full counters, declared epoch/frame, zero simulation
uncertainty, channel parity, routing fields and actual supplied open holonomies.
It rejects skew, incompatible references, malformed/tampered/replayed words,
nonidentity histories and intervals missing either window. It advances both
clocks and never silently resynchronizes on failure. A transport callback makes
the exchanged serialized words observable and permits negative test injection.

Epoch/frame, full counter, uncertainty and orientation history are **out-of-band
observations of this local harness**. Eight bytes alone cannot attest them,
establish physical zero drift or authenticate a remote peer. Production event
envelopes, replay policy and measured uncertainty remain owned by the ecosystem
components. This profile is a review candidate, not a canonical SHD-CCP update.

`[PROVEN]` docstrings apply to stated arithmetic identities under their inputs;
passing tests do not prove the broader physical claims of the source papers.
Related official papers: RP-0010 (orbital model), RP-0018 (Cubit), RP-0020 (Fifteen
Lemmas), RP-0004/RP-0009 (pump). Existing reference material remains unchanged.
