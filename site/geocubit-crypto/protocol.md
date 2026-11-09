# GCC-EXP-001: Geometric Cubit Cryptography — explainer protocol RFC

**Document status:** experimental, non-normative design scaffold  
**Date:** 2026-11-09  
**Repository:** BioChainAI/Geometric-Labs  
**Scope:** conceptual post-quantum cryptographic ecosystem, geometric context, logical clock and optional waveform transport  
**Security status:** **NOT FOR PRODUCTION SECURITY.** No new encryption primitive, geometric one-way function, PQ security reduction or validated network handshake is implemented here.

## 1. Executive architecture

The proposed **Geometric Cubit Cryptography (GCC)** ecosystem separates the functions of geometry, cryptography and network operations:

| Layer | Responsibility | Source of assurance |
|---|---|---|
| Geometric metrology | Local acoustic cubit C₀ = v/(16 fcal) | Instrument traceability, uncertainty and calibration evidence |
| Canonical representation | Algebraic, hyperbolic and quaternionic frame descriptors | Deterministic encoding and cross-platform golden vectors |
| PQ authentication and secrets | Ephemeral key encapsulation, signatures, key derivation, AEAD | NIST-standardized security assumptions, protocol analysis and vetted implementations |
| Geometric intrinsic clock | Deterministic phase labeling, logical epoch and geometric checkpoint indices | Exact modular arithmetic; freshness separately enforced |
| Hyperbolic addressing | Compact hierarchical path and group/graph topological labels | Structural correctness, not preimage hardness |
| Wave embedding | Optional acoustic/EM data transport and environmental measurements | Channel coding and cryptographic authentication, not inherent physical secrecy |
| Audit / storage | Signed evidence and chained integrity checks | Digital signatures, keyed MACs, append-only transparency or authenticated tree roots |

**Governing rule:** *geometry proposes, arithmetic certifies, cryptography authenticates.*

The existing repository specifies that South Halo, gate byte, CRC and Triple-Quad tests are never authenticators. Its Einstein Tile is a 64-bit **routing/representation** word, not a substitute for 128-/256-bit security material. The repository's CR-0001 negative control demonstrates that an exact quaternion walk can be inverted.

## 2. Claims ledger and source fidelity

| Claim | Evaluation | Action |
|---|---|---|
| Local acoustic cubit C₀ = v/(16 fcal) | A useful engineering **definition** | Keep explicit environment and calibration uncertainty |
| Equal acoustic cubits across remote sites | Not physically implied: sound speed varies | Exchange signed normalization and transformation statements |
| Eight-step spinor phase / threefold schedule | Finite modular arithmetic; period lcm(8,3)=24 | Use as publicly known metadata only |
| 720/72/10 time aggregation | Meaningful for structured ordered sequences and declared frame conventions | Verify order, precision, boundary state and recoverability |
| Clifford-torus embedding | Valid for points chosen on a 2-torus in S³; not every unit quaternion belongs to one chosen torus | Treat as a constrained representation |
| Quaternion group noncommutativity | Mathematically correct but multiplication/inversion are efficient | Do not claim a noncommutative trapdoor |
| Hyperbolic curvature | Useful for hierarchical representation, not an established hardness assumption | Attach conventional authenticated commitments |
| 64-bit SHD-CCP payload | Good as compact state/routing metadata | Attach separate signatures, AEAD tags and hash digests |
| Geometric prime solitons / physical non-local holonomy | Unconfirmed model hypotheses | Research-only, no cryptographic dependency |
| “Geometric forced-simulation hash” | No established collision/preimage resistance or sequentiality proof | Benchmark as an optional workload; not a cryptographic hash |
| Geometric Engine conditional P=NP | The supplied papers explicitly restrict to procedural integrable cases | Do not infer unrestricted P=NP or O(1) complexity |
| OpenAI ETH-refutation research, October 2026 | Public, independently reviewed **claim** of subexponential SAT/#SAT; formal Lean sources published, independent audit still important | Separate from Geometric Engine theorems and from PQC security |

**Relevant uploaded manuscripts:** *A Proposal for a Standardization of the Cubit*; *The Geometric Engine of Time: Rigorous Formulation of Conditional P=NP*; *The Zero-Point Eight-Step Cycle*; *Unified Dual-Helix Framework for Geometrically-Guided Pollard’s Rho*; *Quaternionic Delta Encoding on Golden Strassen-Clifford Toroids*; *From Linear Ledgers to Toroidal Matrices*; *The Triple Quad 4×4×4 System*. Those documents support the architecture concepts above but **not** a proof of GCC security. The Pollard’s Rho dual-helix paper explicitly labels its oracle-bias acceleration hypothesis unproven and reclassifies exact jump-ahead as open.

The October 2026 OpenAI preprint claims a deterministic subexponential #k-SAT algorithm; its publicly described formalization has a different/possibly weaker exponent than its headline manuscript, and third-party independent verification remains a distinct question. A claim that ETH is false, even if established, does **not** imply P=NP or a practical SAT attack against standardized PQ KEMs.

## 3. Threat model

The attacker controls the network, can record/replay/delay/drop/reorder packets, modify unauthenticated contexts, inject acoustic waveforms, attempt downgrade, conduct extensive precomputation, and may later acquire a cryptographically relevant quantum computer. Separate attacker profiles address stolen device keys, compromised update infrastructure, broken CSPRNG/QRNG, fault injection, side channels, malformed encodings, cosmic synchronization assumptions, and colluding gateways. We do not assume trusted clocks or that two peers inhabit the same coordinate frame.

Claims outside the design's scope include guaranteed resistance to an adversary who already controls an endpoint, guaranteed physical location verification from a single transducer, and unconditional security of untested geometric hardness assumptions.

## 4. Canonical geometric context format (draft v0)

Define a **byte string**, not a floating-point object:

\[
G=\operatorname{ENC}(\mathrm{magic},\mathrm{version},\mathrm{profile},\mathrm{manifold},\mathrm{atlas},\mathrm{frame},\mathrm{calibration},\mathrm{uncertainty},\mathrm{epoch},\mathrm{geometry}).
\]

Requirements for the formal profile:

1. Use fixed-width canonical unsigned/signed integer encodings, explicit signedness and big-endian ordering; rationals are reduced numerator/positive-denominator pairs.
2. Canonicalize equivalent orientation representations only under a declared mathematically valid equivalence, including the \(q\sim -q\) antipodal identification where appropriate.
3. Record dimensional units, coordinate-frame transforms, calibration issuer, uncertainty bound, expiry and a profile/version ID. Do not pretend the local cubit is immutable across temperatures.
4. Reject out-of-range values, negative zero where prohibited, ambiguous rationals, noncanonical NaN bit patterns and unrecognized forms. The **local** 64-bit tile codec may carry an authenticated reference to \(G\), not \(G\) itself.
5. Establish a byte-exact cross-language test suite for canonicalization: Python, Rust, JavaScript (BigInt for 64-bit integers), and the actual deployment hardware.
6. Use a standard domain-separated hash: \(h_G=\mathrm{SHA3\mbox{-}256}(\mathrm{ENC}("GCC-CONTEXT-v1",G))\) or standardized TupleHash with its formally defined byte encoding.
7. For an authenticated statement use a signature on the canonical transcript or \(\mathrm{KMAC256}\) with a genuine independent secret key. A public hash is not sender authentication.

### Quantization is not entropy

If a parameter has only \(2^{64}\) possible encodings, its exhaustive representation search space cannot exceed 64 bits even if drawn as a very complex 4D shape. A 64-bit routing tile is public and frequently redundant. Treat neither environmental measurement noise nor nonlinear geometry as a CSPRNG without entropy assessment and rigorous conditioning.

## 5. Geometric intrinsic clock

Define a *logical* phase, not a physical time base:

\[
p_8(n)=n\bmod 8,\qquad p_3(n)=n\bmod 3,\qquad p_{24}(n)=n\bmod24.
\]

The three values agree because \(8\) and \(3\) are coprime: the pair \((p_8,p_3)\) encodes \(p_{24}\). They repeat every 24 steps, so they are not freshness secrets. Epoch identity must be bound to independently generated session randomness and a persistent sequence-counter context:

\[
\mathrm{ClockContext} = \mathrm{ENC}(\mathrm{sessionID},\mathrm{epoch},\mathrm{seq},p_8,p_3,\mathrm{calibrationID},\Delta t,\sigma_t).
\]

\(\sigma_t\) is the claimed uncertainty and \(\Delta t\) an explicitly labeled measured clock offset. If no trusted time reference is present, use sequence-number replay checks and label clock measurements as unavailable.

Clock validity is **not** a prerequisite for key establishment if a transport can use random nonces/counters. If applications require expiring authorization windows, check trust of the time source and uncertainty margins separately; do not make cyclic phase closure a validity proof.

## 6. Proposed authenticated PQ handshake (abstract)

This flow is a *requirements sketch*, not a cryptographically reviewed wire protocol. For initial deployment, favor established and actively maintained TLS 1.3/HPKE/MLS integrations using profiles that specify supported PQ KEM/signature suites and their negotiation, rather than implementing these stages directly.

A role-specific transcript must cover all exact bytes of every message, the participant credentials, protocol version, suites, both context commitments, both random nonces and every anti-replay marker. A conceptual message sequence:

\`\`\`text
Alice -> Bob: GCC_ClientHello
    version, offered_suites, ctxHashA, fresh_nonceA, policyA

Bob -> Alice: GCC_ServerHello
    selected_suite, ctxHashB, fresh_nonceB,
    ephemeral_ML-KEM_public_key, credentialB,
    signatureB(transcript_so_far)

Alice -> Bob: GCC_ClientKey
    kem_ciphertext, credentialA?, signatureA?,
    finishedA = KMAC256(confirmA, transcriptHash, ...)

Bob -> Alice: GCC_ServerFinished
    finishedB = KMAC256(confirmB, transcriptHash + epoch + startCounter, ...)

Alice <-> Bob: GCC_Record
    epoch, seq, ctxRef, AEAD(ciphertext, authenticated_metadata)
\`\`\`

The transcript/key schedule must be formally specified with distinct input/output domains and secret lengths before an implementation exists. Do not use MAC-then-sign ambiguities, reuse finished keys as data keys or silently derive the session from context alone. Prove or test certificate and public-key validation, encapsulation failures, channel binding, downgrade prevention, nonces, replay storage, crash recovery and rekeying.

With an authenticated KEM transcript:

\[
K_{\mathrm{root}} = \mathrm{KMAC256}(K_{\mathrm{kem}},\operatorname{ENC}(\text{transcriptHash},h_{G_A},h_{G_B},\text{epoch}),256,\text{"GCC-ROOT-v1"}).
\]

This expression illustrates *what belongs in the derivation*, not a standards-compliant KEM combiner or complete protocol. Session keys, nonce bases, exporter secrets and Finished keys require separate domain labels and a vetted key schedule. Post-compromise recovery depends on periodic fresh cryptographic key material. An authenticated session cannot protect against a compromised endpoint's own memory.

## 7. Hashing and the “geometric hash” security boundary

A projectable geometric hash can mean either:

- **Safe and useful:** \(H=\mathrm{SHA3\mbox{-}256}(\operatorname{ENC}(\mathrm{profile},\mathrm{frame},\mathrm{coordinate},\mathrm{payload}))\), or KMAC using an independent key. This is a standard hash or MAC **over** geometric context.
- **Research-only:** design a new one-way map from iterative hyperbolic/quaternionic/toroidal dynamics. This needs extensive public cryptanalysis, exact implementation, collision search and reductions. It does not acquire hardness from noncommutativity or curvature.

Analyze the second case for equivalent-state collisions (\(q,-q\)), short cycles, conjugacy/easy word problem, structural symmetries, representation truncation, malleability, distinguished points, related-input attacks, birthday search, chosen-prefix collision, memory-time tradeoffs, precomputation and quantum search. Do not promote it until independent attack evaluation exceeds standardized controls.

An \(n\)-bit ideal hash has classical generic birthday collision resistance approximately \(2^{n/2}\) and classical preimage cost approximately \(2^n\); a quantum adversary can reduce some generic search exponents. These bounds are about a strong idealized hash model—not proofs for a novel geometric compression map.

## 8. Hyperbolic addresses and 64-bit packets

Represent hierarchy via a canonical graph path or group element, embedded into \(\mathbb H^3\) for distance-based routing. Keep the exact discrete path identifier alongside any numerical embedding. Hyperbolic coordinates or quaternion delta chains may be lossy and require explicit checkpoint/frame reconstruction.

Never accept the claim that a 64-bit packet can contain arbitrary lossless unlimited history. Output bits and structure impose information-theoretic limits. Explicitly bind the selected SHD-CCP tile profile to the network transcript. The project's current local Einstein Tile profile is not the canonical Layer-0 profile and has unresolved form specifications.

A frame transport sketch:

\`\`\`text
outer frame: protocolVersion | authenticatedSessionID | epoch | seq |
             geometryProfileID | tile[] | payloadLen | ciphertext | AEADtag
\`\`\`

The AEAD associated data must include all header fields that affect routing, interpretation, authorization or freshness. Fields outside AEAD must be treated as untrusted hints until authenticated.

## 9. Longitudinal wave embedding

Acoustic/EM physical signals are optional, lossy transport and auxiliary measurement channels, not a quantum-secure communications channel. Modulate an authenticated ciphertext or MACed challenge into symbols; use preamble, channel estimation, equalization, FEC and a specified retransmission/sequence policy. Record frequency, sample rate, sensor geometry, humidity/temperature, SNR, multipath, BER, claimed precision and eavesdropper geometry.

Attack tests: replayed recordings, relay/wormhole, synthetic waveform injection, acoustic reflections, transducer clipping, jamming, ultrasound/inaudible exposure and privacy leakage. Binding signal delay to presence requires a separate distance-bounding threat model; it cannot be inferred from a single time offset when there is no trusted clock.

Avoid claims of faster-than-light signaling, QKD or information-theoretic secrecy without a separately verified physical protocol.

## 10. Product ecosystem

Identity uses signed credentials, trust stores, rotation, revocation and transparency. Messaging uses an authenticated PQ-capable session/MLS protocol and AEAD; geometry serves as optional authenticated metadata. Storage uses envelope encryption, object digests, authenticated indexes and deletion/recovery policies. Ledgers use signatures and consensus rules independently of optional toroidal compression. Secure boot requires a dedicated verified signature chain. SHD-CCP tiles remain routing/codec metadata. AI/visual embeddings and human governance need explicit data-consent and purpose-bound provenance controls. All components have downgrade and compromised-node paths.

## 11. Acceptance tests, roadmap and rejection gates

**P0, byte convention:** publish fixed binary schema and at least 100 positive and 100 negative canonicalization vectors; compare Python/Rust/JS bit-for-bit; test 64-bit edge cases, noncanonical equivalent quaternions, no NaNs and non-bypassable version checks.

**P1, primitive integration:** select maintained FIPS-compatible crypto libraries; pass NIST known-answer tests; validate certificate and key handling; use library APIs, never homegrown ML-KEM or AES; specify explicit cryptographic failure behavior.

**P2, authenticated exchange:** produce a machine-readable state machine, secret/identity event annotations and ProVerif/Tamarin model or equivalent; attempt replay, MITM, downgrade, unknown key share and concurrency/race tests.

**P3, comparative geometry:** benchmark performance and message size against identical cryptography *without* geometric metadata. Publish real confidence intervals, hardware, memory budget, acceptance thresholds and overhead, not theoretical constant-time claims.

**P4, physical channel:** test at least one reproducible wired baseline and one acoustic experiment with adversarial injected recordings and jamming; report sensitivity to temperature, room mode and calibration.

**Reject or demote** any proposal that derives entropy solely from public geometric state, claims signature strength from an 8-bit Halo, cannot pin its byte encoding, admits efficient geometric inversion, lacks independent security analysis, or degrades standard protocol properties.

## 12. Repository integration

- Preserve \`Geometric-Labs/src\`, \`verification/\`, golden vectors and existing workflows.
- Keep explainer sources under \`site/geocubit-crypto/\`; its source-independent pages must use first-party scripts/styles and a strict Content Security Policy.
- Treat \`Cryptographic_Research/\` as the experimental cryptography gate and obtain CR IDs before proposing an actual novel primitive.
- Use \`ecosystem/experiments/geometric_clock/\` only as a **logical** clock simulation, not a physical synchronization oracle.
- Deploy through a reviewed PR and existing Pages build; no direct main-branch publication or auto-merge.
- For implementation, separate code ownership between SHD-CCP-core (codec), Geometric-Labs (math/tests), PolyShard-Agent (device), CubiLoom (events) and Polycentric-Orchestrator (coordination).

## 13. Primary and local references

1. Geometric-Labs local reference profile: [Einstein Tile reference profile v1](../../spec_sync/einstein_tile_64bit_rfc.md).
2. Geometric-Labs: [specification status](../../docs/specification_status.md), [cryptographic research](../../Cryptographic_Research/README.md), and [geometric clock](../../ecosystem/experiments/geometric_clock/README.md).
3. NIST: [FIPS 203, ML-KEM](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204, ML-DSA](https://csrc.nist.gov/pubs/fips/204/final), [FIPS 205, SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final), [SP 800-185, KMAC/TupleHash](https://csrc.nist.gov/pubs/sp/800/185/final), [FIPS 202 SHA-3](https://csrc.nist.gov/pubs/fips/202/final).
4. IETF: [RFC 8446 TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446), [RFC 9180 HPKE](https://www.rfc-editor.org/rfc/rfc9180), [RFC 9420 MLS](https://www.rfc-editor.org/rfc/rfc9420). These generic RFCs do not themselves establish support for any particular hybrid/PQ wire suite: select an actually approved profile.
5. OpenAI: [ETH preprint repository, dated October 2026](https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026), [Lean scope note](https://github.com/openai/math/blob/main/lean/docs/378.md); independent analysis: [Dias/Lima](https://arxiv.org/abs/2611.00517).
6. The uploaded **Geometric Engine of Time** and **cubit** manuscripts are the motivating primary project texts. Their conjectural physical interpretation remains separate from public standards.

---

*This RFC is designed to be superseded by versioned, reviewed technical specifications and reproducible cryptographic evidence—not to declare a new cryptosystem secure by terminology or by geometric analogy.*
