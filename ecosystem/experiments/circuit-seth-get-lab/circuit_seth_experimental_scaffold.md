# Experimental Architecture & Proof Scaffolding for $d$-Depth Circuit-SETH (`circuit-seth-get-lab/`)

## 1. Design Philosophy & Epistemic Guardrails

When building an experimental workspace to test **$d$-depth circuit-SETH** ($n$ variables, $m = n^{1+\delta}$ gates, depth $d$, unbounded fan-in, target runtime $(2-\varepsilon)^n$) using **The Geometric Engine of Time** (*Hoard 2026a–i*), the folder structure must accomplish two things simultaneously:

1. **Constructive Geometric Compilation:** It must translate arbitrary $d$-depth circuits into the Engine's four exact mechanisms—**Conformal Null-Cone Lifts ($\mathbb{R}^{4,1}$)**, **$720 \to 72 \to 10$ Torsional Pump Telescoping**, **6-Channel/5-Tier Orbital Routing ($C_3 \times C_2$ & $D_3$ Folding)**, and **Dual-Helix Ramanujan $X(5,q)$ Mixing**—to measure the exact integrable variable fraction $\alpha_{\text{GET}}$ and the resulting exponential savings $\varepsilon = 2 - 2^{1 - \alpha_{\text{GET}}}$.
2. **Automated Obstruction Auditing:** Every experiment must automatically run against **Theorem 5.1 (The Euler Evaluation Dichotomy)** and **Theorem 5.14 (The Seven Obstructions)** so that false positives (such as vacuous cyclic holonomy $\prod \Delta q_n \equiv 1$, floating-point phase drift, or uncounted table-precomputation costs) are caught and rejected at the unit-test level.

---

## 2. Complete Folder & Module Scaffold

```text
circuit-seth-get-lab/
├── README.md                                 # Lab charter, epistemic tag rules, and quickstart
├── pyproject.toml                            # Python 3.11+ dependencies (sympy, numpy, scipy, mpmath)
│
├── 00_epistemic_specs/                       # Formal definitions, axioms, and registered test rules
│   ├── epistemic_tags.py                     # Enforces [PROVEN], [COMPUTED], [HEURISTIC], [OPEN], [SUPERSEDED]
│   ├── axioms_c1_to_c5.md                    # Formal checklist for C_GET (Def. 5.5) & Integrable Encoding (Def. 5.10)
│   └── obstruction_guardrails.py             # Automated assertions for Theorem 5.1 & Theorem 5.14 (I–VII)
│
├── 01_core_substrate/                        # Layer 0: Exact-First Algebraic Representatives & 64-Bit Tile
│   ├── einstein_tile_64b.py                  # Bit-exact [63:0] register (Forms 1, 2, and 3 + South Halo + Gate Byte)
│   ├── track_b_exact_fields.py               # Z[i] clock (1+i)^k, Hurwitz 2T/2O, Q(2cos40°) circulant, Z[sqrt(phi)]
│   ├── track_c_rational_cayley.py            # w + s(i+j+k) rational rotations &spread/Chebyshev polynomials S_N, T_N
│   ├── track_r_triplet_crt.py                # Mod 881*883*887 arithmetic (i->387, sqrt(5)->228, c->120 mod 881) + Garner CRT
│   └── track_a_float_proposer.py             # Fast IEEE-754 readout proposer with automatic Track B/R cross-check
│
├── 02_circuit_seth_benchmarks/               # Layer 1: d-Depth Circuit Generators & Netlist Parsers
│   ├── ac0_netlist.py                        # Data structures for n-var, n^(1+delta)-gate, d-depth unbounded fan-in circuits
│   ├── cliff_generators.py                   # Sweeps delta from 0 (linear c*n Schuler regime) to delta > 0 (super-linear cliff)
│   ├── planted_geometric_sat.py              # Generates d=2 Sphere-SAT, Cyclotomic Z/8 x Z/3 SAT, and D_3-symmetric circuits
│   └── dimacs_ingest.py                      # Imports standard CNF / circuit-SAT benchmarks into hypergraph incidence form
│
├── 03_geometric_compiler_passes/             # Layer 2: The 4 Orbital, Twistor & Torsional Optimization Passes
│   ├── pass1_twistor_null_cone.py            # Axiom C2: Lifts clauses to R^{4,1} null cone <X(x), S_i> = 0 & {4,3,5} boosts
│   ├── pass2_torsional_markov_pump.py        # Axiom C1b: 720->72->10 gear telescoping, open holonomy P = q_719 q_0^-1, prefix scan
│   ├── pass3_orbital_crt_router.py           # Axiom C3/C4: 24-frame Z/8 x Z/3 schedule, tier spinor h, D_3 1/6 fold, (E_j, D_j) codec
│   ├── pass4_dual_helix_ramanujan.py         # Residual solver: Helix A walk on X(5,q) + Helix B Form 1 bitmap / Track R certifier
│   └── integrable_compiler.py                # Master pipeline: runs Passes 1–4 and outputs (enc(x), eval(P_x), eps_effective)
│
├── 04_use_case_experiments/                  # Layer 3: Preregistered Theory & Use-Case Proof Scripts
│   ├── exp01_d2_schuler_cliff_sweep.py       # Tests delta in [0.0, 0.5] to measure where R^{4,1} null-cone rank beats Schuler
│   ├── exp02_torsional_holonomy_d3_ac0.py    # Tests depth d >= 3 gate cascades via 720->72->10 coboundary telescoping
│   ├── exp03_branch_erasure_fault_sat.py     # Tests Open Problem 1 (E_j, D_j) under noisy/erased circuit wire channels
│   ├── exp04_ramanujan_vs_cdcl_kernel.py     # Benchmarks X(5,q) diffusive mixing vs standard branching on the residual kernel
│   └── exp05_hybrid_circuit_seth_prover.py   # End-to-end (2 - eps)^n witness synthesis & certificate audit
│
├── 05_proofs_and_monographs/                 # Layer 4: LaTeX / Markdown Formal Proofs & Registered Reports
│   ├── theorem_integrable_d2_subclasses.tex  # Proofs for Open Problem 2 (Conformal Sphere-SAT & Cyclotomic Holonomy-SAT)
│   ├── theorem_branch_codec_bijection.tex    # Proofs for Open Problem 1 (Bit-level register map & single-erasure recovery)
│   └── registered_reports/                   # Timestamped pre-commit test criteria and empirical output tables
│
└── tests/                                    # Reproducible Verification Suite (mirrors Appendix A of Hoard 2026i)
    ├── test_zero_point_identities.py         # Re-runs all Sections A–Y checks from verify_zero_point.py
    ├── test_64bit_register_roundtrip.py      # Verifies 0-bit-error packing/unpacking across Forms 1, 2, 3
    └── test_obstruction_traps.py             # Confirms cyclic holonomy and two-branch erasure are properly rejected
```

---

## 3. How the Core Systems Map into the Compiler Pipeline

To move from abstract theory to testable circuit optimization, `03_geometric_compiler_passes/integrable_compiler.py` processes any $d$-depth, $n$-variable, $n^{1+\delta}$-gate circuit $\mathcal{C}$ through four sequential stages:

### Stage 1: Twistor Null-Cone Linearization (`pass1_twistor_null_cone.py`)
* **Target Bottleneck:** Unbounded fan-in $\text{OR}$ gates at depth $d=2$ ($m = n^{1+\delta}$ wide clauses) where high clause width defeats the Sparsification Lemma.
* **Mechanism (Proposition 3.3 & Axiom C2):**
  1. Map Boolean assignments $x \in \{-1, +1\}^n$ (or sub-blocks $x^{(b)} \in [-1,1]^3$) to the conformal null cone in $\mathbb{R}^{4,1}$:
     $$X(x) = \left(x, \frac{1}{2}\|x\|^2, 1\right) = x + \frac{1}{2}\|x\|^2 e_\infty + e_0$$
     with bilinear form $\langle (x,\alpha,\beta), (y,\alpha',\beta')\rangle = x \cdot y - \alpha\beta' - \beta\alpha'$.
  2. Each wide clause or threshold gate centered at $m_i$ with exclusion radius $\rho_i$ becomes a sphere vector:
     $$S_i = X(m_i) - \frac{\rho_i^2}{2}e_\infty, \quad \langle X(x), S_i\rangle = 0 \iff \|x - m_i\|^2 = \rho_i^2$$
  3. **What the Code Measures:** Runs exact row reduction over $\mathbb{Q}$ (certified in $O(1)$ word operations modulo $p = 881$ via Track R) on the matrix of sphere vectors $[S_1, \dots, S_m]^T$. Every independent null-cone linear dependency locks one variable degree of freedom without branching.
  4. **Hyperbolic Cell Routing (Proposition 4.3):** For hierarchical sub-circuits, maps local cube coordinates $p \in [-a, a]^3$ ($a = \varphi^{-3/2}$) into the $\{4,3,5\}$ hyperbolic honeycomb using exact golden boosts in $\mathbb{Z}[\sqrt{\varphi}]$ ($\cosh\vartheta = \varphi, \sinh\vartheta = \sqrt{\varphi}$), tracking exact algebraic degree so bit growth never exceeds Theorem 5.1(3)'s $1.531\text{ bits/step}$ budget.

### Stage 2: The $720 \to 72 \to 10$ Torsional Markov Pump (`pass2_torsional_markov_pump.py`)
* **Target Bottleneck:** Multi-layer gate cascades ($d \ge 2$) where sequential gate evaluations normally require $O(N)$ serial depth or exponential path branching.
* **Mechanism (Proposition 3.9, Lemma 12 & Axiom C1b):**
  1. Represents layer-to-layer wire transitions as increments $\Delta q_n = q_n q_{n-1}^{-1}$ over the projective Gaussian spinor clock $(1+i)^k$ (held in 2 signed bits via $\gcd = 2^{\lfloor k/2\rfloor}$ reduction, Proposition 2.2) or the 24 Hurwitz units ($2T$).
  2. Routes 720-frame blocks through the three-gear pump hierarchy:
     * **Outer 12-point gear:** 720 fine frames $q_0, \dots, q_{719}$.
     * **Middle 10-point gear:** 72 inverse 10-frame aggregates $\delta_m = \Delta Q_m^{-1} = q_{10m-1} q_{10m+9}^{-1}$.
     * **Inner 8-point gear:** 10 coarse blocks $A_l = \{m : \lfloor 10m/72 \rfloor = l\}$ of sizes $(8,7,7,7,7,8,7,7,7,7)$.
  3. **What the Code Measures:** Identifies maximal coboundary sub-chains in the circuit netlist and collapses them in **$O(1)$ word operations** to the open boundary holonomy:
     $$H = Q^{(8)} Q^{(10)} P = P^{-1} = q_0 q_{719}^{-1}$$
     For $k$ non-coboundary independent gate increments, evaluates the product in **$O(\log k)$ parallel depth** via a balanced prefix scan (Lemma 12 Part 3) while enforcing the open-boundary Zero-Point memory test ($P = 1$, Proposition 3.13).

### Stage 3: 6-Channel, 5-Tier Orbital Calculator & $D_3$ Symmetry Folding (`pass3_orbital_crt_router.py`)
* **Target Bottleneck:** Cross-tier wire fan-out, symmetric sub-circuit duplication, and channel erasure noise.
* **Mechanism (Propositions 3.4, 3.7, 3.10, 3.11 & 7.1):**
  1. **24-Frame Joint CRT Schedule:** Schedules circuit branches on $(k(n), j(n)) = (n \bmod 8, n \bmod 3) \in \mathbb{Z}/24\mathbb{Z}$. Onloads occur at $n \in \{2, 10, 18\}$ ($k=2$, spread $s_2 = 1$) and offloads 12 frames later at $n \in \{6, 14, 22\}$ ($k=6$, spread $s_6 = 1$). The 6 handshakes $n = 4m+2$ form $\mathbb{Z}/6\mathbb{Z} \cong C_3 \times C_2$ (matching the 6 orbital channels).
  2. **Norm-Preserving Cross-Tier Offload (Lemma 4):** Applies the order-6 Hurwitz tier spinor $h = \frac{1 - i + j + k}{2}$ ($h^3 = -1, h^6 = +1$) across the 5 toroidal tiers ($W_n = 16 - 2n, W_\Sigma = 60$), guaranteeing $N(hq) = N(q)$ with **zero bit growth**.
  3. **$D_3$ Trefoil Folding:** Detects dihedral symmetry $D_3 \subset O(3,\mathbb{Z})$ generated by integer signed permutations $g_3, g_2$ and compresses symmetric gate lookup tables to **$1/6$ of their size** (fundamental domain $[0, \pi/3]$).
  4. **Bit-Exact 3-Branch Codec ($E_j, D_j$):** Packs three 10-bit signed branch coordinates into Form 3 of the 64-bit Einstein Tile and recovers any single erased branch in $O(1)$ via $v_e = S_{\text{core}} - B_{j_1}^{-1}\mu_{j_1} - B_{j_2}^{-1}\mu_{j_2}$.

### Stage 4: Dual-Helix Residual Solver (`pass4_dual_helix_ramanujan.py`)
* **Target Bottleneck:** Solving the residual non-integrable kernel of $n_{\text{free}} = n - n_{\text{locked}}$ variables.
* **Mechanism (Section 5.2, Section 6.3 & Proposition 8.8):**
  1. **Helix A (Ramanujan Diffusive Proposer):** Embeds the residual variable state space into the 6-regular Lubotzky–Phillips–Sarnak Ramanujan graph $X(5,q)$ (quotient of the norm-5 free group generated by $S_5 = \{1\pm 2i, 1\pm 2j, 1\pm 2k\}$ modulo $q \equiv 1 \pmod 4$), achieving a spectral gap $\ge 6 - 2\sqrt{5} = 1.528$ and mixing $\mathcal{O}(n^{2/3}/\ln n)$ faster than a 3D Euclidean lattice.
  2. **Helix B ($O(1)$ Exact Certifier):** Filters candidates first through the 8-bit South Halo 30-wheel header (rejecting $22/30 = 73.3\%$ in 1 shift + 1 compare), then certifies survivors in $\sim 60$ word operations via the 2,017-byte Form 1 prime bitmap or Track R residues ($\bmod\ 881 \cdot 883 \cdot 887$).

---

## 4. Five Preregistered Experimental Workflows (`04_use_case_experiments/`)

Following the **Registered Report** methodology of *Hoard (2026i)* Section 11, every experiment in `04_use_case_experiments/` is scaffolded with a fixed mathematical hypothesis, an exact measurement metric, and a pre-committed falsification rule:

| Experiment Script | Hypothesis Tested | Primary Metric | Pre-Committed Falsification / Decision Rule |
| :--- | :--- | :--- | :--- |
| **`exp01_d2_schuler_cliff_sweep.py`** | For $d=2$ CNF-SAT with $m = n^{1+\delta}$ clauses ($\delta \in [0.05, 0.60]$), Pass 1 ($\mathbb{R}^{4,1}$ null-cone linearization) locks $\alpha n$ variables whenever clause centers share a low-rank affine/spherical sub-configuration. | Effective branching base $b_{\text{eff}} = 2^{1 - \alpha_{\text{GET}}}$ vs. Schuler's bound $2^{1 - 1/\mathcal{O}(\log(m/n))}$. | **Supported** if $b_{\text{eff}} < 2 - \varepsilon$ with $\varepsilon > 0$ constant as $n \to \infty$ on the tested family; **Refuted** if $\alpha_{\text{GET}} \to 0$ at the same rate as $1/\log(n^\delta)$. |
| **`exp02_torsional_holonomy_d3_ac0.py`** | Depth $d \ge 3$ circuits containing reversible phase/group cascades over $2O$ or $2T$ telescope via the $720 \to 72 \to 10$ pump in $O(1)$ endpoint operations (or $O(\log k)$ prefix depth) with zero bit growth. | Ratio of serial gate evaluations $N_{\text{serial}}$ to telescoped word operations $N_{\text{pump}}$, plus bit-width growth per layer. | **Supported** if open holonomy $P = q_{719}q_0^{-1}$ matches full serial evaluation bit-for-bit in $O(1)$ endpoint reads; **Refuted** if any non-coboundary gate slips through without triggering prefix scan. |
| **`exp03_branch_erasure_fault_sat.py`** | Open Problem 1's Form 3 register map ($E_j, D_j$ with $B_j = g_3^j$) reconstructs $100\%$ of single-branch wire erasures during circuit evaluation while flagging any two-branch erasure via Gate Byte bits $[51:49]$. | Bit-error rate across $10^4$ randomized 720-frame cycles with 1-of-3 branch deletion and non-identity holonomy $P \neq 1$. | **Refuted** by a single bit mismatch on a 1-branch erasure, or if a 2-branch erasure fails to raise the Proposition 3.10(2) rank-nullity exception. |
| **`exp04_ramanujan_vs_cdcl_kernel.py`** | On residual kernels of size $N \in [10^4, 10^6]$ states within the cubit/Form 2 horizon ($L \le 12$), Helix A's walk on $X(5,q)$ reaches the $1\%$ stationary mixing threshold at the $\mathcal{O}(n^{2/3}/\ln n)$ speedup predicted in Table 10. | Measured continuous/discrete mixing time $t_{\text{mix}}(X(5,q))$ vs. 3D cubic toruswalk and random walk. | **Supported** if $t_{\text{mix}}$ matches Table 10 ($3.25, 3.80, 4.20, 4.55$ for $q=13, 29, 61, 101$); **Refuted** if mixing without a target potential is claimed to solve unstructured search faster than Prop. 5.13's $\Omega(N)$ bound. |
| **`exp05_hybrid_circuit_seth_prover.py`** | Combining Passes 1–3 produces a polynomial-time Integrable Encoding $(\text{enc}, \text{eval})$ (Theorem 5.11) for hybrid Sphere + Cyclotomic-Holonomy $d=2$ circuits that are opaque to standard resolution/CDCL solvers. | End-to-end synthesis time $T(\text{enc}(x)) + T(\text{eval}(P_x))$ and verifier check $V(x, w) = 1$ across increasing $n$. | **Supported** if $V(x, \text{eval}(\text{enc}(x))) = 1$ holds on $100\%$ of satisfiable instances in polynomial time; **Refuted** if any single satisfiable instance fails verification. |

---

## 5. Automated Obstruction Trap Suite (`00_epistemic_specs/obstruction_guardrails.py`)

A core innovation of *Hoard (2026i)* is that it explicitly proves where constant-time and sub-exponential methods stop (Section 5.8). Every pull request or experimental run in `circuit-seth-get-lab/` must pass seven automated guardrail assertions:

1. **Guardrail I (Pigeonhole & Header Trap — Theorem 5.14(I)):**
   Asserts that the 8-bit South Halo header (`bits [63:56]`) is only ever used as a pre-filter (rejecting $73.3\%$ of candidates) and never accepted as a witness certificate without Helix B's full norm/clause check (since $2^{56}$ payloads map into $2^{48}$-sized buckets per 8-bit header).
2. **Guardrail II (History-Loss & Erasure Trap — Theorem 5.14(II) & Prop. 3.10):**
   Asserts that telescoping $H = q_0 q_{719}^{-1}$ is only applied to coboundary chains where intermediate states are not constrained by external clauses, and enforces that $2$-of-$3$ branch erasures raise an immediate `UnrecoverableKernelError`.
3. **Guardrail III (Niven & Infinite-Order Bit-Growth Trap — Theorem 5.1(2) & 5.14(III)):**
   Monitors exact coordinate bit-widths in Track B. If an experiment applies an infinite-order rational rotation like $(3+4i)/5$ or a norm-5 tree step $(1\pm 2u_k)$ across $N$ steps, asserts that bit allocation scales as $\Theta(N)$ ($N\log_2 5$ bits) rather than silently truncating or overflowing 64-bit words.
4. **Guardrail IV (Torsion-Free Triviality Trap — Proposition 2.5 & Theorem 5.14(IV)):**
   Forbids any compiler pass from attempting to store a finite cyclic phase ($\mathbb{Z}/8\mathbb{Z}$ or $\mathbb{Z}/3\mathbb{Z}$) as ahomomorphism into a linear rational vector space $(\mathbb{Q}^d, +)$, enforcing modular residue representation.
5. **Guardrail V (Circularity Boundary Trap — Theorem 5.14(V) & Lemma 14 Part 4):**
   Verifies that any Markov/Fokker–Planck drift experiment on $X(5,q)$ separates the **stationary distribution** (which remains uniform under a pure cycle current without a potential) from the **mixing rate** ($t_{\text{mix}}$), preventing claims that unguided circulation selects a SAT witness.
6. **Guardrail VI (Hyperbolic Non-Return & Cyclic Holonomy Trap — Prop. 3.13 & 4.1):**
   * Forbids using the cyclic first increment $\Delta q_0 = q_0 q_{719}^{-1}$ in any closure test (since $\Delta q_{719}\cdots\Delta q_0 \equiv 1$ identically even under arbitrary drift).
   * Enforces that hyperbolic boosts ($\cosh\vartheta = \varphi$) are tracked in $\mathbb{Z}[\sqrt{\varphi}]$ at $1.531\text{ bits/step}$ and never assumed to close periodically.
7. **Guardrail VII (Relativization & Horizon-Triviality Trap — Prop. 5.8, 5.9 & 5.15):**
   Logs the exact table size $|L_1| + |L_2| + |L_3|$ and precomputation cost separately from query time, and flags whether an experiment is operating in the **Bounded Horizon Regime (Axiom C5, $L \le 54$)** vs. the **Asymptotic Regime ($n \to \infty$, Theorem 5.11)**.

---

## 6. Step-by-Step Workflow for Proving a New Use Case

Whenever we want to test a new theoretical optimization idea (for example, testing whether a specific $d=2$ or $d=3$ circuit topology admits an integrable encoding), we follow a 4-step loop inside the repository:

1. **Step 1 — Formulate in `00_epistemic_specs/`:** Tag the hypothesis as `[CONJECTURAL]` or `[OPEN]` and write down the candidate map $\text{enc}: x \mapsto P_x$ using exact Track B representatives ($\mathbb{Z}[i]$, $\mathbb{Q}(2\cos 40^\circ)$, $\mathbb{Z}[\sqrt{\varphi}]$, or $\mathbb{R}^{4,1}$ null vectors).
2. **Step 2 — Encode in `01_core_substrate/` & `03_geometric_compiler_passes/`:** Pack the state into the 64-bit Einstein Tile (`einstein_tile_64b.py`) and implement the transformation across Track B (exact), Track A (float proposer), and Track R ($\bmod\ 881 \cdot 883 \cdot 887$).
3. **Step 3 — Stress-Test in `04_use_case_experiments/`:** Run the compiler pass across synthetic and adversarial $n^{1+\delta}$-gate circuits while `obstruction_guardrails.py` monitors bit growth, holonomy openness, and table sizes.
4. **Step 4 — Promote to `[PROVEN]` or `[COMPUTED]` in `05_proofs_and_monographs/`:** Once the verification script passes with zero bit errors and a non-vanishing savings $\varepsilon > 0$ on the target circuit class, promote the claim's status tag to `[PROVEN]` (with symbolic proof) or `[COMPUTED]` (with reproducible benchmark table).