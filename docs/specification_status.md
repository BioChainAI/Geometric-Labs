# Scope, corrections, and pending specification details

The three supplied artifacts are preserved as the architecture blueprint,
interactive walkthrough, and `verification/reference/original_master_suite.py`.
No research PDFs or full Layer 0 tile RFC were attached. Blueprint theorem
references are provisional citations, not independently checked proofs.

## Reference runner corrections

The executable master differs from the original in three documented ways:

1. For the specified vertices CPython 3.12 returns **-4294967296.0**, not zero,
   for the float64 triple-quadrance expression. The exact Gram result is still
   **4**. The corrected assertion tests loss of accuracy against 4, and its
   output says cancellation error rather than false collinearity.
2. Anchor signatures contain a list inside a dictionary key. Converting the
   distance list to a tuple fixes the resulting TypeError without changing
   distances or matching.
3. There are **16** test groups (3+3+3+3+4), not 14. All 16 requested modular
   files are implemented; unittest reports individual test-method counts.

The master remains standalone and retains its reference formulas. Modular tests
exercise the extracted production-facing APIs separately. The original master
is archival and intentionally fails; it is not a CI target.

## Implemented and bounded

* Exact arbitrary-width integer Hurwitz ring, all 24 units, Gram quadrea, S5
  right steps/reduced-word recovery, CRT, prime bitmap and unsigned-64 MR12.
  Python integers prevent overflow; this is not a benchmark of hardware int128.
* Unit-Hurwitz QCC and right-acting 720-state holonomy, inclusive Blelloch prefix
  scan with linear work and logarithmic dependency depth. Python runs sequentially.
* Exact Fibonacci/Lucas checkpoints and discrete two-sided i-axis unit updates.
  These are not a general rational S3 codec or a complete compressed ledger.
* Four-structure 64-stream routing model with component projection streams,
  cyclic erasure recovery, supported parity cascade and tier inversion. A common
  balancer frame per group is required for reverse closure. Norm preservation
  does not imply preservation of each coordinate's bit width: for example
  h*(1,1,1,1) has doubled coordinates (0,0,2,0), increasing the maximum magnitude.
* Exact integer Eisenstein-basis phase splitting, rational separated auxiliary
  rectangles, graph coloring, covering determinants, lossless pruning. Rectangles
  are allocated on the auxiliary torus. A full physical soliton solver and
  pulled-back conflict geometry are not specified by the artifacts.
* Cramer model, local cubit, temperature-cancelled room modes, caller-supplied
  independent six-term GUM budget; sign-invariant coherence via convergent
  symmetric Jacobi diagonalization; 3D Horn rotation fit and exact 24-Hurwitz
  unit snap, plus the full 24-element octahedral matrix snap and certified
  origin-centered anchor alignment. A 4-component Horn eigenvector describes
  an SO(3) rotation, not an arbitrary SO(4) rotation. The octahedral O group
  and the Hurwitz unit group 2T are represented separately.

## Details requiring canonical input

* Forms 0 and 4–15 Codex shape semantics, exact Form-2 packing, Form-1 canonical
  normalization rule and reserved-bit meaning: see the local tile profile.
* Six numerical instrument uncertainties/covariances: the blueprint's ±0.22 mm
  cannot be certified without these. No artificial default budget is supplied.
* Complete paper manifest, Proposition 4.3, full general SO(4) frame handshake specification, physical soliton rectangle pullbacks and Fokker–Planck
  generator/boundaries for the claimed 1.402 spectral convergence rate.

The wheel bias test establishes a proposal density ratio, not a prime oracle,
cryptographic security proof, throughput guarantee, or convergence theorem.
The 12-layer construction is a SHA-256 hash chain and detects changed fixtures;
it does not establish distributed consensus or a complete authentication protocol.
The CRC demonstration exhibits the equal-length affine XOR identity and a
four-byte chosen-checksum forgery using GF(2) elimination; it is not a SHA-256
attack. Golden vectors certify this local profile, not an absent RFC.

## Validation

`make verify-all` runs the corrected master, modular tests, and a byte-for-byte
vector drift check. Every modular script also runs directly without installation.
CI requests Python 3.10, 3.11, and 3.12; local versions actually exercised are
reported separately. Interactive HTML was supplied unchanged and loads external
browser assets; it is not part of the zero-dependency Python verification target.
