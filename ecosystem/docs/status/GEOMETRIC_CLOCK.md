# Geometric clock reference implementation

Date: 2026-10-28 (America/Chicago). Base: `69624113091e` (official publication
collection merged through PR #9). Branch: `codex/geometric-clock`.

## Implemented

The standalone [geometric-clock package](../../experiments/geometric_clock/README.md)
implements all seven requested modules: tier invariants; the six C3 × C2 channels;
the exact projective Gaussian cycle; rational quaternion deltas and 720/72/10
ordered history; complete uint64 Einstein Tile envelopes; exact logical pulse
snapshots; and a two-clock local byte-exchange verifier. It has no third-party
runtime dependencies. Pytest is an optional test dependency. Public code passes
strict mypy and includes a packaged `py.typed` marker.

The finite CLI service emits one exact final JSON snapshot or JSONL tick records.
It also runs the local simulated handshake. At pulse 30 it returns node 0,
spinor k=6, exactly 4,596,315,885 atomic cycles, elapsed model time 1/2 second,
and zero atomic remainder. The default handshake performs eight bidirectional
window exchanges (sixteen actual eight-byte transfers) over 30 logical pulses.

## Specification decisions made explicit

- The 60 Hz SI anchoring is a model convention. This code does not measure a
  physical second, oscillator drift or remote clock synchronization.
- Fractions preserve exact integer/half-integer cycles, including counters above
  floating-point and 64-bit limits. Zero remainder occurs on every even pulse;
  30 pulses close the structural traversal. Joint node/spinor phase return needs
  120 pulses; the absolute counter continues increasing.
- GCD-reduced Gaussian representatives preserve spinor signs. Odd-step integer
  representatives are projective, not normalized rational unit quaternions.
- The pump retains 720 orientation frames and an identity first boundary delta,
  hence 719 transitions. Fine deltas multiply latest on the left; inverse middle
  blocks multiply chronologically on the right. The 72-to-10 partition includes
  all indices exactly once, using groups of seven or eight. Full quaternion
  holonomy equals q0 q719⁻¹; nonidentity endpoints and negative identity are not
  mislabeled closed. No Markov transition kernel or lossless-history compression
  is inferred from the hierarchy.
- Existing wire bit positions remain unchanged. The clock uses an explicitly
  local `geometric-clock-pulse-v1` profile: Form 0 is opaque pulse-counter data,
  gate byte contains node 0..29, and structure selector retains its two-bit
  routing meaning. All six channels derive from node parity/phase; they are not
  truncated into two bits. The complete fields in bits 32–47 are preserved.
- Raw payload uses low32 pulse bits deliberately. The verifier compares full
  snapshots and supplied epoch/frame/uncertainty/history observations in-process;
  identical raw words alone do not establish epoch, replay safety or physical
  alignment. Unknown profiles, mismatched references, skew, bad states, tampering,
  replay and nonidentity histories fail without silent resynchronization.

The [profile document](../../experiments/geometric_clock/docs/protocol-profile.md)
and preserved source request distinguish implementation choices from normative
protocol semantics. No existing core math, golden vector, root tooling or upstream
repository is modified. Default orientation history is an explicit closed identity
fixture; callers can provide nontrivial histories. Pulse advancement does not
invent measured orientation samples. `[PROVEN]` docstrings concern their stated
finite arithmetic identities, not broader physical claims or a formal Lean audit.

## Executed validation

- Pytest: **72 passed** on Python **3.10.22** and **3.12.14**, including the five
  requested acceptance cases, every wire bit, sixteen existing golden envelopes,
  seeded words, noncommutative/open histories, phase drift, replay, malformed
  packets, incompatible references/profiles, wrong peer states and concurrent ticks.
- Strict mypy: **no issues in 12 source files**.
- Wheel built and installed with `--no-deps` into a fresh virtual environment.
  Import and both CLI modes run outside the repository with `python -I`;
  pytest is absent from that environment.
- Original `make verify-all` and full pinned ecosystem acceptance pass: 40 core
  methods, 23 offline ecosystem methods, four integration methods, five vector
  files, 183 packet cases, lock validation and exact reference demo TQF 576.
- Pages: 15 tests pass, and the existing desktop/mobile/project-subpath browser
  check passes with the new clock section. Historical checkpoint evidence remains
  frozen and is not relabeled as a test pass for this change.

A dedicated new CI lane tests Python 3.10/3.11/3.12 and runs the installed CLI
outside the checkout. The existing scientific workflows and conformance profiles
remain unchanged. [Machine-readable evidence](geometric-clock-validation.json)
records source/request hashes and test reports. Local logs are under
`/tmp/geometric-clock-*`; no real hardware or authenticated network timing test
is asserted. The earlier five untracked architecture-investigation files remain
separate. Publication uses a review branch, with no automatic merge or deployment.
